#! /usr/local/bin/python3
"""Factory class for creating TableIO instances."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from typing import Optional, NamedTuple
from functools import total_ordering
from mformat.mformat import PathLike
from tableio.tableio import TableIO, Descriptor, FileAccess
from tableio.capability import Capabilities, capability_match
from tableio.reg_pkg_formats import register_formats_in_pkg
from tableio.optional_args import OptionalArgs, OptionalArgsDict


_the_factory: Optional['TableIOFactory'] = None  # pylint: disable=invalid-name # noqa: E501


COMMON_ARGS = ['file_exists_callback']


class TableIOFactoryConflictError(ValueError):
    """Raised when trying to register conflicting class.

    Error raised when a format is registered with the factory
    that conflicts with an existing format or existing implementation.
    The conflict may be that user is trying to register the same
    class twice, or that another class has the same format name or
    implementation name when comparing case insensitively.
    """


class TableIOFactoryNoSuchError(KeyError):
    """Raised when requesting a format/implementation that is not registered.

    Error raised when requesting a format or implementation with a
    format name or implementation name that is not registered.
    """


class TableIOFactoryNoCapabilityMatch(ValueError):
    """Raised when requested capabilities cannot be matched.

    Error raised when requested capabilities cannot be matched to any
    available implementation. This can be that the requester is requesting
    capabilities that are not supported by any available format or
    implementation, or that the requester is requesting a specific
    format name or implementation name, and the implementation(s)
    with those name(s) do not support the requested capabilities.
    """


class InsufficientCapabilities(ValueError):
    """Raised when requested capabilities contradict requested file access.

    Error raised when the caller supplies both file access and an explicit
    Capabilities object, but the requested capabilities do not include the
    capability implied by that access mode. For example, READ requires
    can_read, CREATE requires can_write, and UPDATE requires both.
    """


def _check_capabilities_for_file_access(
        file_access: FileAccess,
        capabilities: Optional[Capabilities]) -> None:
    """Raise if explicit capabilities not enough for requested access mode."""
    if capabilities is None:
        return
    if file_access == FileAccess.READ and not capabilities.can_read.supported:
        msg = 'FileAccess.READ requires can_read capability.'
        raise InsufficientCapabilities(msg)
    if file_access == FileAccess.CREATE and \
            not capabilities.can_write.supported:
        msg = 'FileAccess.CREATE requires can_write capability.'
        raise InsufficientCapabilities(msg)
    if file_access == FileAccess.UPDATE and (
            not capabilities.can_write.supported or
            not capabilities.can_read.supported):
        msg = 'FileAccess.UPDATE requires both can_read and '
        msg += 'can_write capabilities.'
        raise InsufficientCapabilities(msg)


@total_ordering
class ImplPrio(NamedTuple):
    """Priority of an implementation."""

    format_name: str
    """The name of the format."""

    implementation: str
    """The name of the implementation."""

    priority: int
    """The priority of the implementation."""

    def __lt__(self, other: object) -> bool:
        """Compare two implementation priorities."""
        if not isinstance(other, ImplPrio):
            return NotImplemented
        if self.priority < other.priority:
            return True
        if self.priority > other.priority:
            return False
        if self.format_name < other.format_name:
            return True
        if self.format_name > other.format_name:
            return False
        return self.implementation < other.implementation

    def __eq__(self, other: object) -> bool:
        """Compare two implementation priorities."""
        if not isinstance(other, ImplPrio):
            return NotImplemented
        return not self < other and not other < self


class BestMatch(NamedTuple):
    """Best matches for requested capabilities.

    This is used to store the best matches for requested capabilities.
    The best matches are stored in tuples of ImplPrio objects.
    The tuples are sorted by priority, from highest to lowest.
    The first tuple strictly matches the requested capabilities
    (that is the class can achieve all of the requested capabilities).
    The second tuple contains implementations that can tolerate
    all of the requested capabilities, but may ignore some of
    the requested capabilities.
    """

    strict_matches: tuple[ImplPrio, ...]
    """The implementations that strictly match the requested capabilities."""

    nonstrict_matches: tuple[ImplPrio, ...]
    """Implementations that tolerate but may ignore some capabilities."""

    @staticmethod
    def from_lists(strict_matches: list[ImplPrio],
                   nonstrict_matches: list[ImplPrio]) -> 'BestMatch':
        """Initialize a BestMatch object."""
        strict_m = sorted(strict_matches, reverse=True)
        nonstrict_m = sorted(nonstrict_matches, reverse=True)
        return BestMatch(strict_matches=tuple(strict_m),
                         nonstrict_matches=tuple(nonstrict_m))

    def __len__(self) -> int:
        """Get the number of best matches."""
        return len(self.strict_matches) + len(self.nonstrict_matches)

    def combined(self) -> list[ImplPrio]:
        """Get the combined list of best matches."""
        return list(self.strict_matches + self.nonstrict_matches)

    @staticmethod
    def add(first: 'BestMatch', second: 'BestMatch') -> 'BestMatch':
        """Add two best matches."""
        return BestMatch.from_lists(
            strict_matches=list(first.strict_matches) +
            list(second.strict_matches),
            nonstrict_matches=list(first.nonstrict_matches) +
            list(second.nonstrict_matches))

    @staticmethod
    def add_list(best_matches: list['BestMatch']) -> 'BestMatch':
        """Add a list of best matches."""
        if not best_matches:
            return BestMatch(strict_matches=(), nonstrict_matches=())
        ret = best_matches[0]
        for best_match in best_matches[1:]:
            ret = BestMatch.add(ret, best_match)
        return ret


class FactoryFormatInfo:
    """Information about a format registered with the factory.

    This is used to store the information about a format registered with the
    factory. For each format there may be several implementations, each with
    different capabilities.
    The TableIOFactory class will store the information about the formats in a
    dictionary, with the format name as the key, and objects of this class as
    the values.
    Objects of this class will store the information about the different
    implementations of the format.
    """

    def __init__(self, format_class: Optional[type[TableIO]] = None) -> None:
        """Initialize the FactoryFormatInfo object."""
        self._registry: dict[str, type[TableIO]] = {}
        self._usage: dict[str, Descriptor] = {}
        self._lower2correct: dict[str, str] = {}  # Lower case to correct case
        if format_class is not None:
            self.add_implementation(format_class)

    def add_implementation(self, format_class: type[TableIO]) -> None:
        """Add an implementation of a format to the factory."""
        desc: Descriptor = format_class.get_description()
        if desc.implementation in self._registry:
            kmsg = f'Implementation "{desc.implementation}" '
            kmsg += 'is already registered.'
            raise TableIOFactoryConflictError(kmsg)
        if desc.implementation.lower() in self._lower2correct:
            msg = f'Cannot register implementation "{desc.implementation}" ' +\
                f'as "{self._lower2correct[desc.implementation.lower()]}" ' + \
                'is already registered.'
            raise TableIOFactoryConflictError(msg)
        self._registry[desc.implementation] = format_class
        self._usage[desc.implementation] = desc
        self._lower2correct[desc.implementation.lower()] = desc.implementation

    def best_match_names(self, capabilities: Optional[Capabilities] = None,
                         empty_is_ok: bool = False) -> BestMatch:
        """Get the best matching implementation names for the capabilities.

        Args:
            capabilities: The capabilities to match. If not specified,
                          all implementations are included in the return
                          value.
            empty_is_ok: If True, an empty list is returned if no
                         implementations match the capabilities.
                         If False, a TableIOFactoryNoCapabilityMatch
                         error is raised.
        Raises:
            TableIOFactoryNoCapabilityMatch: If empty_is_ok is False and
                                             no implementations match the
                                             capabilities.
        Returns:
            A BestMatch object containing the matching implementations.
            The strict_matches are implementations that support all
            of the requested capabilities. The nonstrict_matches are
            implementations that tolerate all of the requested
            capabilities but may ignore some. Within each group the
            implementations are sorted by priority, from highest to
            lowest. (A higher priority means that the resulting output
            more strictly follows the file format specification and
            is compatible with more software.)
            If no implementations match and empty_is_ok is True, an
            empty BestMatch is returned.
        """
        if capabilities is None:
            ret1: list[ImplPrio] = [
                ImplPrio(format_name=impl_class.get_description().format_name,
                         implementation=impl_name,
                         priority=impl_class.get_description().priority)
                for impl_name, impl_class in self._registry.items()
            ]
            return BestMatch.from_lists(strict_matches=ret1,
                                        nonstrict_matches=[])
        assert capabilities is not None
        strict_matches: list[ImplPrio] = [
            ImplPrio(format_name=impl_class.get_description().format_name,
                     implementation=impl_name,
                     priority=impl_class.get_description().priority)
            for impl_name, impl_class in self._registry.items()
            if capability_match(impl_class.get_capabilities(), capabilities,
                                ignore_allowed=False)
        ]
        tolerant_matches: list[ImplPrio] = [
            ImplPrio(format_name=impl_class.get_description().format_name,
                     implementation=impl_name,
                     priority=impl_class.get_description().priority)
            for impl_name, impl_class in self._registry.items()
            if capability_match(impl_class.get_capabilities(), capabilities,
                                ignore_allowed=True)
        ]
        nonstrict_matches: list[ImplPrio] = [
            impl for impl in tolerant_matches if impl not in strict_matches
        ]
        ret = BestMatch.from_lists(strict_matches=strict_matches,
                                   nonstrict_matches=nonstrict_matches)
        if not empty_is_ok and len(ret) == 0:
            msg = 'No implementation matches the capabilities.'
            raise TableIOFactoryNoCapabilityMatch(msg)
        return ret

    def correct_implementation_name(self, implementation_name: str) -> str:
        """Correct the implementation name to the correct case."""
        if implementation_name in self._registry:
            return implementation_name
        if implementation_name.lower() in self._lower2correct:
            return self._lower2correct[implementation_name.lower()]
        raise TableIOFactoryNoSuchError(
            f'Implementation "{implementation_name}" is not registered. ' +
            'Available implementations: ' +
            f'{", ".join(list(self._registry.keys()))}')


class TableIOFactory:
    """Factory class for creating instances of TableIO subclasses.

    TableIO subclasses are registered with the factory, and the factory can
    create instances of the registered TableIO subclasses.
    There may be several registered classes for the same format name,
    as long as they have different implementation names.
    The format names and implementation names are stored case preserving,
    but the lookup for format names and implementation names are case
    insensitive.
    Each implementation of a format name may have the same or different
    capabilities. When creating an instance of a TableIO subclass or when
    asking for a list of the registered formats or implementations, the
    requester can specify the capabilities that are required, and the factory
    will limit the return value to only include classes that match the
    requested capabilities.
    """

    def __init__(self) -> None:
        """Initialize the factory with an empty registry."""
        self._formats: dict[str, FactoryFormatInfo] = {}
        self._lower2correct: dict[str, str] = {}  # Lower case to correct case
        formats: list[type[TableIO]] = register_formats_in_pkg()
        for format_class in formats:
            self.i_register(format_class)

    @staticmethod
    def i_get_factory() -> 'TableIOFactory':
        """Internally get the factory instance."""
        global _the_factory  # pylint: disable=global-statement # noqa: E501
        if _the_factory is None:
            _the_factory = TableIOFactory()
        return _the_factory

    @staticmethod
    def register(format_class: type[TableIO]) -> None:
        """Register a TableIO subclass with the factory.

        Several implementations of the same format may be registered.
        Each implementation may have different capabilities.
        Args:
            format_class: The TableIO subclass to register.
        Raises:
            ValueError: If the format_class is not a subclass of TableIO.
            TableIOFactoryConflictError: If the format_class is already
                                         registered, or the names conflict
                                         with another registered format.
        """
        factory = TableIOFactory.i_get_factory()
        factory.i_register(format_class=format_class)

    def i_register(self, format_class: type[TableIO]) -> None:
        """Internally register a TableIO subclass with the factory."""
        if not issubclass(format_class, TableIO):
            err = f'{format_class.__name__} must be a subclass of TableIO'
            raise ValueError(err)
        desc: Descriptor = format_class.get_description()
        if desc.format_name in self._formats:
            self._formats[desc.format_name].add_implementation(format_class)
            return
        if desc.format_name.lower() in self._lower2correct:
            msg2 = f'Cannot register format "{desc.format_name}" as ' + \
                f'"{self._lower2correct[desc.format_name.lower()]}" ' + \
                'is already registered.'
            raise TableIOFactoryConflictError(msg2)
        self._formats[desc.format_name] = \
            FactoryFormatInfo(format_class=format_class)
        self._lower2correct[desc.format_name.lower()] = desc.format_name

    @staticmethod
    def create(format_name: str,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
               file_name: PathLike,
               file_access: FileAccess, args: OptionalArgs = None,
               implementation: Optional[str] = None,
               capabilities: Optional[Capabilities] = None) -> TableIO:
        """Create an instance of a registered TableIO subclass.

        Args:
            format_name: The name identifier of the format class to create.
            file_name: The file path to pass to the TableIO constructor.
            file_access: The file access to pass to the TableIO constructor.
            args: additional arguments to pass to the TableIO constructor.
            implementation: The implementation name to use. If not specified,
                            the matching implementation with the highest
                            priority is used.
            capabilities: The capabilities to match. If not specified,
                          the implementation matching the format name (and
                          if specified the implementation name) is used.
                          If several implementations match, the
                          implementation with the highest priority
                          is used.
        Returns:
            An instance of the requested TableIO subclass.
            Intended to be used as context manager, using a with statement.
        Raises:
            InsufficientCapabilities: If capabilities contradict file_access.
            TableIOFactoryNoSuchError: If the format_name is not registered
                                        or the implementation name is not
                                        registered.
            TableIOFactoryNoCapabilityMatch: If the capabilities cannot be
                                              matched to any implementation.
        """
        factory = TableIOFactory.i_get_factory()
        return factory.i_create(format_name=format_name,
                                file_name=file_name,
                                file_access=file_access,
                                args=args, implementation=implementation,
                                capabilities=capabilities)

    def i_create(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 format_name: str, file_name: PathLike,
                 file_access: FileAccess, args: OptionalArgs = None,
                 implementation: Optional[str] = None,
                 capabilities: Optional[Capabilities] = None) -> TableIO:
        """Internally create an instance of a registered subclass.

        Raises:
            InsufficientCapabilities: If capabilities contradict file_access.
            TableIOFactoryNoSuchError: If the format_name is not registered
                                       or the implementation name is not
                                       registered.
            TableIOFactoryNoCapabilityMatch: If the capabilities cannot be
                                             matched to any implementation.
        """
        _check_capabilities_for_file_access(file_access, capabilities)
        correct_name: Optional[str] = None
        if format_name in self._formats:
            correct_name = format_name
        elif format_name.lower() in self._lower2correct:
            correct_name = self._lower2correct[format_name.lower()]
        else:
            raise TableIOFactoryNoSuchError(
                f'Format "{format_name}" is not registered. ' +
                'Available formats: ' +
                f'{", ".join(sorted(list(self._formats.keys())))}'
            )
        assert correct_name is not None
        format_info: FactoryFormatInfo = self._formats[correct_name]
        best_matches = format_info.best_match_names(
            capabilities=capabilities, empty_is_ok=False)
        if implementation is not None:
            corrected_implementation = \
                format_info.correct_implementation_name(implementation)
            bmatches_impls = [impl.implementation
                              for impl in best_matches.combined()]
            if corrected_implementation not in bmatches_impls:
                msg3 = f'Implementation "{implementation}" '
                msg3 += 'does not match the capabilities. Available matches: '
                msg3 += f'{", ".join(bmatches_impls)}'
                raise TableIOFactoryNoCapabilityMatch(msg3)
            chosen_impl = corrected_implementation
        else:
            chosen_impl = best_matches.combined()[0].implementation
        format_class = format_info._registry[chosen_impl]  # pylint: disable=protected-access # noqa: E501
        if args is None:
            return format_class(file_name=file_name, file_access=file_access)
        return format_class(file_name=file_name,  # type: ignore[misc]
                            file_access=file_access, **args)
        # mypy cannot see which TableIO subclass is being created, so it
        # cannot know which arguments are valid.

    @staticmethod
    def filter_args(args: OptionalArgs, format_name: str,
                    implementation: str) -> OptionalArgs:
        """Filter the arguments for a registered format.

        Filter the arguments to only include the arguments that are valid for
        the given format name and implementation. This is useful when the args
        dictionary includes arguments for several formats, and not all of
        them are valid for the given format name and implementation.
        (The risk of using this function is that a misspelled argument will
        be silently ignored, and the programming error will not be detected.)
        Args:
            args: The arguments to filter.
            format_name: The name identifier of the format class to filter the
                         arguments for.
            implementation: The implementation name to use.
        Returns:
            The filtered arguments.
        Raises:
            TableIOFactoryNoSuchError: If the format_name is not registered
                                       or the implementation name is not
                                       registered.
        """
        factory = TableIOFactory.i_get_factory()
        return factory.i_filter_args(args=args, format_name=format_name,
                                     implementation=implementation)

    def i_filter_args(self, args: OptionalArgs, format_name: str,
                      implementation: str) -> OptionalArgs:
        """Internally filter the arguments for a registered format."""
        format_usage = self.i_get_usage(format_name=format_name,
                                        implementation=implementation)
        if args is None:
            return None
        assert args is not None
        ret: OptionalArgsDict = {}
        for arg_name in args:
            if arg_name in format_usage.mandatory_args:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
            elif arg_name in format_usage.optional_args:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
            elif arg_name in COMMON_ARGS:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
        return ret

    @staticmethod
    def get_registered_formats(lower: bool = False,
                               upper: bool = False,
                               capabilities: Optional[Capabilities] = None,
                               empty_is_ok: bool = False) -> list[str]:
        """Get a list of all registered format names.

        The list includes all registered format names optionally filtered
        to only include formats that offer the requested capabilities.
        Always includes the correct case for the format names in the returned
        list. If lower or upper is True, also includes those cases of the
        format names in the returned list. (Including lower case and upper
        case variants is probably not a good idea when printing the list
        for a human user, but it is useful when checking if a format name
        is in the allowed list of format names.)
        Args:
            lower: If True, also include the format name in lower case.
            upper: If True, also include the format name in upper case.
            capabilities: The capabilities to match. If not specified,
                          all formats are included in the return value.
                          If specified, only formats that offer the requested
                          capabilities are included in the return value.
            empty_is_ok: If True, an empty list is returned if no
                         formats match the capabilities.
                         If False, a TableIOFactoryNoCapabilityMatch
                         error is raised if no formats match the capabilities.
        Returns:
            A list of registered format name strings optionally filtered
            to only include formats that offer the requested capabilities.
        Raises:
            TableIOFactoryNoCapabilityMatch: If empty_is_ok is False and
                                             no formats match the
                                             capabilities.
        """
        factory = TableIOFactory.i_get_factory()
        return factory.i_get_registered_formats(lower=lower, upper=upper,
                                                capabilities=capabilities,
                                                empty_is_ok=empty_is_ok)

    def i_get_registered_formats(self, lower: bool = False,
                                 upper: bool = False,
                                 capabilities: Optional[Capabilities] = None,
                                 empty_is_ok: bool = False) -> list[str]:
        """Internally get a list of registered format names."""
        if capabilities is not None:
            filtered_names = sorted([
                name for name, format_info in self._formats.items()
                if format_info.best_match_names(capabilities=capabilities,
                                                empty_is_ok=True).combined()
            ])
            if not filtered_names and not empty_is_ok:
                msg = 'No formats match the capabilities.'
                raise TableIOFactoryNoCapabilityMatch(msg)
        else:
            filtered_names = sorted(list(self._formats.keys()))
        ret: list[str] = []
        for name in filtered_names:
            ret.append(name)
            if lower and name != name.lower():
                ret.append(name.lower())
            if upper and name != name.upper():
                ret.append(name.upper())
        return ret

    @staticmethod
    def get_registered_implementations(format_name: Optional[str] = None,
                                       lower: bool = False,
                                       upper: bool = False,
                                       capabilities: Optional[Capabilities]
                                       = None,
                                       empty_is_ok: bool = False) -> list[str]:
        """Get a list of all registered implementation names.

        The list includes all registered implementation names optionally
        filtered to only include implementations for the specified format
        name and optionally filtered to only include implementations that
        offer the requested capabilities.
        Always includes the correct case for the implementation names in the
        returned list. If lower or upper is True, also includes those cases
        of the implementation names in lower case and upper case.
        (Including lower case and upper case variants is probably not a good
        idea when printing the list for a human user, but it is useful when
        checking if a implementation name is in the allowed list of
        implementation names.)

        Args:
            format_name: The name identifier of the format to get the
                         implementation names for. If not specified, all
                         implementations are included in the return value.
            lower: If True, also include the implementation name in lower case.
            upper: If True, also include the implementation name in upper case.
            capabilities: The capabilities to match. If not specified,
                          all implementations are included in the return value.
            empty_is_ok: If True, an empty list is returned if no
                         implementations match the capabilities.
                         If False, a TableIOFactoryNoCapabilityMatch
                         error is raised if no implementations match the
                         capabilities.
        Returns:
            A list of registered implementation name strings optionally
            filtered to only include implementations that offer the
            requested capabilities.
        Raises:
            TableIOFactoryNoCapabilityMatch: If empty_is_ok is False and
                                             no implementations match the
                                             capabilities.
        """
        factory = TableIOFactory.i_get_factory()
        return factory.i_get_registered_implementations(
            format_name=format_name, lower=lower, upper=upper,
            capabilities=capabilities, empty_is_ok=empty_is_ok)

    def i_get_registered_implementations(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
            self, format_name: Optional[str] = None,
            lower: bool = False, upper: bool = False,
            capabilities: Optional[Capabilities] = None,
            empty_is_ok: bool = False) -> list[str]:
        """Internally get a list of registered implementation names."""
        fmtkeys: list[str] = list(self._formats.keys())
        if format_name is not None:
            fmtkeys = [format_name]
        implkeys: set[str] = set()
        if capabilities is not None:
            implmatches: list[BestMatch] = []
            for fmtkey in fmtkeys:
                format_info: FactoryFormatInfo = self._formats[fmtkey]
                implmatches.append(
                    format_info.best_match_names(capabilities=capabilities,
                                                 empty_is_ok=True))
            implkeys = {
                impl.implementation for impl in
                BestMatch.add_list(implmatches).combined()
              }  # several format names may have the same implementation name
            if not implkeys and not empty_is_ok:
                msg = 'No implementations match the capabilities.'
                raise TableIOFactoryNoCapabilityMatch(msg)
        else:
            implkeys = {
                implkey
                for fmtkey in fmtkeys
                for implkey in self._formats[fmtkey]._registry.keys()  # pylint: disable=protected-access # noqa: E501
            }
        ret: list[str] = []
        for implkey in sorted(implkeys):  # order was lost using a set
            ret.append(implkey)
            if lower and implkey != implkey.lower():
                ret.append(implkey.lower())
            if upper and implkey != implkey.upper():
                ret.append(implkey.upper())
        return ret

    @staticmethod
    def get_usage(format_name: str, implementation: str) -> Descriptor:
        """Get the usage information for a registered format.

        Args:
            format_name: The name identifier of the format class to get
                         the usage information for.
            implementation: The implementation name to use.
        Returns:
            The usage information for the requested format.
        Raises:
            TableIOFactoryNoSuchError: If the format_name is not registered
                                        or the implementation name is not
                                        registered.
        """
        factory = TableIOFactory.i_get_factory()
        return factory.i_get_usage(format_name=format_name,
                                   implementation=implementation)

    def i_get_usage(self, format_name: str, implementation: str) -> Descriptor:
        """Internally get the usage information for a registered format."""
        format_info: Optional[FactoryFormatInfo] = None
        if format_name in self._formats:
            format_info = self._formats[format_name]
        elif format_name.lower() not in self._lower2correct:
            msg1 = f'Format "{format_name}" is not registered. '
            msg1 += 'Available formats: '
            msg1 += f'{", ".join(sorted(list(self._formats.keys())))}'
            raise TableIOFactoryNoSuchError(msg1)
        else:
            format_info = self._formats[self._lower2correct[format_name.lower()]]  # pylint: disable=protected-access # noqa: E501
        assert format_info is not None
        fusage = format_info._usage  # pylint: disable=protected-access # noqa: E501
        if implementation in fusage:
            return fusage[implementation]
        l2correct = format_info._lower2correct  # pylint: disable=protected-access # noqa: E501
        if implementation.lower() not in l2correct:
            msg2 = f'Implementation "{implementation}" is not registered. '
            msg2 += 'Available implementations: '
            msg2 += f'{", ".join(list(format_info._registry.keys()))}'  # pylint: disable=protected-access # noqa: E501
            raise TableIOFactoryNoSuchError(msg2)
        correct_name = l2correct[implementation.lower()]
        return format_info._usage[correct_name]  # pylint: disable=protected-access # noqa: E501


def create_tableio(format_name: str,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                   file_name: PathLike,
                   file_access: FileAccess,
                   args: OptionalArgs = None,
                   implementation: Optional[str] = None,
                   capabilities: Optional[Capabilities] = None) -> TableIO:
    """Create an instance of a registered TableIO subclass.

    Intended to be used as context manager, using a with statement.
    This is a shortcut for TableIOFactory.create().
    Args:
        format_name: The name identifier of the format class to create.
        file_name: The file path to pass to the TableIO constructor.
        file_access: The file access to pass to the TableIO constructor.
        args: additional arguments to pass to the TableIO constructor.
        implementation: The implementation name to use. If not specified,
                        the matching implementation with the highest
                        priority is used.
        capabilities: The capabilities to match. If not specified,
                      the implementation matching the format name (and
                      if specified the implementation name) is used.
                      If several implementations match, the implementation
                      with the highest priority is used.
    Returns:
        An instance of the requested TableIO subclass.
    Raises:
        InsufficientCapabilities: If capabilities contradict file_access.
        TableIOFactoryNoSuchError: If the format_name or implementation
                                   name is not registered.
        TableIOFactoryNoCapabilityMatch: If the capabilities cannot be
                                          matched to any implementation.
    """
    return TableIOFactory.create(format_name=format_name,
                                 file_name=file_name,
                                 file_access=file_access,
                                 args=args,
                                 implementation=implementation,
                                 capabilities=capabilities)


def filter_args_tableio(args: OptionalArgs, format_name: str,
                        implementation: str) -> OptionalArgs:
    """Filter the arguments for a registered format.

    This is a shortcut for TableIOFactory.filter_args().
    Filter the arguments to only include the arguments that are valid for
    the given format name and implementation. This is useful when the args
    dictionary includes arguments for several formats, and not all of them
    are valid for the given format name and implementation. (The risk of
    using this function is that a misspelled argument will be silently
    ignored, and the programming error will not be detected.)
    Args:
        args: The arguments to filter.
        format_name: The name identifier of the format class to filter
                     the arguments for.
        implementation: The implementation name to use.
    Returns:
        The filtered arguments.
    Raises:
        TableIOFactoryNoSuchError: If the format_name or implementation
                                   name is not registered.
    """
    return TableIOFactory.filter_args(args=args, format_name=format_name,
                                      implementation=implementation)


def list_registered_tableio(lower: bool = False,
                            upper: bool = False,
                            capabilities: Optional[Capabilities] = None,
                            empty_is_ok: bool = False) -> list[str]:
    """Get a list of all registered format names.

    This is a shortcut for TableIOFactory.get_registered_formats().
    Always includes the correct case for the format names in the returned
    list. If lower or upper is True, also includes those cases of the
    format names in the returned list. (Including lower case and upper
    case variants is probably not a good idea when printing the list
    for a human user, but it is useful when checking if a format name
    is in the allowed list of format names.)
    Args:
        lower: If True, also include the format name in lower case.
        upper: If True, also include the format name in upper case.
        capabilities: The capabilities to match. If not specified,
                      all formats are included in the return value.
                      If specified, only formats that offer the requested
                      capabilities are included in the return value.
        empty_is_ok: If True, an empty list is returned if no
                     formats match the capabilities.
                     If False, a TableIOFactoryNoCapabilityMatch
                     error is raised if no formats match the capabilities.
    Returns:
        A list of registered format name strings.
    """
    return TableIOFactory.get_registered_formats(lower=lower,
                                                 upper=upper,
                                                 capabilities=capabilities,
                                                 empty_is_ok=empty_is_ok)


def list_implementations_tableio(format_name: Optional[str] = None,
                                 lower: bool = False,
                                 upper: bool = False,
                                 capabilities: Optional[Capabilities] = None,
                                 empty_is_ok: bool = False) -> list[str]:
    """Get a list of all registered implementation names.

    This is a shortcut for TableIOFactory.get_registered_implementations().
    Args:
        format_name: The name identifier of the format to get the
                     implementation names for. If not specified, all
                     implementations are included in the return value.
        lower: If True, also include the implementation name in lower case.
        upper: If True, also include the implementation name in upper case.
        capabilities: The capabilities to match. If not specified,
                      all implementations are included in the return value.
                      If specified, only implementations that offer the
                      requested capabilities are included in the return value.
        empty_is_ok: If True, an empty list is returned if no
                     implementations match the capabilities.
                     If False, a TableIOFactoryNoCapabilityMatch
                     error is raised if no implementations match the
                     capabilities.
    Returns:
        A list of registered implementation name strings optionally
        filtered to only include implementations that offer the
        requested capabilities.
    Raises:
        TableIOFactoryNoCapabilityMatch: If empty_is_ok is False and
                                         no implementations match the
                                         capabilities.
    """
    return TableIOFactory.get_registered_implementations(
        format_name=format_name, lower=lower, upper=upper,
        capabilities=capabilities, empty_is_ok=empty_is_ok)


def usage_tableio(format_name: str, implementation: str) -> Descriptor:
    """Get the usage information for a registered format.

    This is a shortcut for TableIOFactory.get_usage().
    Args:
        format_name: The name identifier of the format class to get the
                     usage information for.
        implementation: The implementation name to use.
    Returns:
        The usage information for the requested format.
    Raises:
        TableIOFactoryNoSuchError: If the format_name or implementation
                                   name is not registered.
    """
    return TableIOFactory.get_usage(format_name=format_name,
                                    implementation=implementation)


def register_tableio(format_class: type[TableIO]) -> None:
    """Register a TableIO subclass with the factory.

    This is a shortcut for TableIOFactory.register().
    Args:
        format_class: The TableIO subclass to register.
    Raises:
        ValueError: If the format_class is not a subclass of TableIO.
        TableIOFactoryConflictError: If the format_name or implementation
                                    name is already registered.
    """
    TableIOFactory.register(format_class=format_class)
