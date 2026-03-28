#! /usr/bin/env python3
"""TableIO writer classes based on MultiFormat."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Callable
from mformat.mformat import PathLike
from mformat.mformat_md import MultiFormatMd
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat_txt import MultiFormatTxt
from mformat.mformat_latex import MultiFormatLatex
from mformat.mformat_rst import MultiFormatRst
from mformat.paper_size import PaperSize, PaperSizeInput
from mformat.document_class import DocumentClassInput
from mformat.plain_text_table import TableAlignment, TableAlignmentSpec
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat_ext.mformat_odt import MultiFormatOdt
from mformat_ext.mformat_pdf import MultiFormatPdf
from mformat_ext.mformat_rtf import MultiFormatRtf
from tableio.tableio_mformatbased import TableIOMformatBased, \
    _allow_overwrite
from tableio.tableio import FileAccess, Descriptor
from tableio.capability import SingleCapability


class TableIOMformatMd(TableIOMformatBased):
    """TableIO writer class for Markdown, based on MultiFormat."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8'):
        """Initialize the TableIOMformatMd writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            character_encoding: The character encoding to use.
        """
        super().__init__(file_name, file_access, file_exists_callback)
        self.mformat = MultiFormatMd(
            file_name, file_exists_callback=_allow_overwrite,
            character_encoding=character_encoding)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.md'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatMd writer class."""
        return Descriptor(format_name='md', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'character_encoding'])


class TableIOMformatHtml(TableIOMformatBased):
    """TableIO writer class for HTML, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 character_encoding: str = 'utf-8',
                 title: str = 'HTML file',
                 css_file: Optional[str] = None,
                 lang: str = 'en'):
        """Initialize the TableIOMformatHtml writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            character_encoding: The character encoding to use.
            title: The title of the HTML file.
            css_file: The CSS file to use.
            lang: The language of the HTML file.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatHtml(
            file_name,
            file_exists_callback=_allow_overwrite,
            character_encoding=character_encoding,
            title=title, css_file=css_file, lang=lang)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.html'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatHtml writer class."""
        return Descriptor(format_name='HTML', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'character_encoding',
                                         'title', 'css_file', 'lang'])


class TableIOMformatTxt(TableIOMformatBased):
    """TableIO writer class for plain text, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 character_encoding: str = 'utf-8',
                 line_length: int = 79,
                 table_max_line_length: Optional[int] = None,
                 table_alignment: TableAlignmentSpec =
                 TableAlignment.CENTER_BUT_DIGITS_RIGHT):
        """Initialize the TableIOMformatTxt writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            character_encoding: The character encoding to use.
            line_length: The maximum length of a line.
            table_max_line_length: The maximum length of a line when
                                   writing a table. If None,
                                   line_length is used.
            table_alignment: The alignment of cell values in tables.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatTxt(
            file_name,
            file_exists_callback=_allow_overwrite,
            character_encoding=character_encoding,
            line_length=line_length,
            table_max_line_length=table_max_line_length,
            table_alignment=table_alignment)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=False)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.txt'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatTxt writer class."""
        return Descriptor(format_name='txt', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'character_encoding',
                                         'line_length',
                                         'table_max_line_length',
                                         'table_alignment'])


class TableIOMformatLatex(TableIOMformatBased):
    """TableIO writer class for LaTeX, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 character_encoding: str = 'utf-8',
                 document_class: Optional[DocumentClassInput] = None,
                 paper_size: Optional[PaperSizeInput] = None,
                 title: Optional[str] = None,
                 latex_preamble: str = '',
                 latex_heading_levels: Optional[dict[int, str]]
                 = None,
                 latex_replacements:
                 Optional[list[dict[str, str]]] = None):
        """Initialize the TableIOMformatLatex writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            character_encoding: The character encoding to use.
            document_class: The LaTeX document class to use.
            paper_size: The paper size to use.
            title: The title of the LaTeX document.
            latex_preamble: Extra LaTeX preamble text.
            latex_heading_levels: Override heading level commands.
            latex_replacements: Custom text replacement stages.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatLatex(
            file_name,
            file_exists_callback=_allow_overwrite,
            character_encoding=character_encoding,
            document_class=document_class,
            paper_size=paper_size, title=title,
            latex_preamble=latex_preamble,
            latex_heading_levels=latex_heading_levels,
            latex_replacements=latex_replacements)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.tex'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatLatex writer class."""
        return Descriptor(format_name='LaTeX', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'character_encoding',
                                         'document_class',
                                         'paper_size',
                                         'title',
                                         'latex_preamble',
                                         'latex_heading_levels',
                                         'latex_replacements'])


class TableIOMformatRst(TableIOMformatBased):
    """TableIO writer class for reStructuredText, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 character_encoding: str = 'utf-8',
                 line_length: int = 79,
                 table_max_line_length: Optional[int] = None,
                 table_alignment: TableAlignmentSpec =
                 TableAlignment.LEFT):
        """Initialize the TableIOMformatRst writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            character_encoding: The character encoding to use.
            line_length: The maximum length of a line.
            table_max_line_length: The maximum length of a line when
                                   writing a table. If None,
                                   line_length is used.
            table_alignment: The alignment of cell values in tables.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatRst(
            file_name,
            file_exists_callback=_allow_overwrite,
            character_encoding=character_encoding,
            line_length=line_length,
            table_max_line_length=table_max_line_length,
            table_alignment=table_alignment)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=False)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.rst'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatRst writer class."""
        return Descriptor(format_name='reST', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'character_encoding',
                                         'line_length',
                                         'table_max_line_length',
                                         'table_alignment'])


class TableIOMformatDocx(TableIOMformatBased):
    """TableIO writer class for DOCX, based on MultiFormat."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 paper_size: PaperSize = PaperSize.A4):
        """Initialize the TableIOMformatDocx writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            paper_size: Paper size for the document.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatDocx(
            file_name,
            file_exists_callback=_allow_overwrite,
            paper_size=paper_size)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.docx'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatDocx writer class."""
        return Descriptor(format_name='docx', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'paper_size'])


class TableIOMformatOdt(TableIOMformatBased):
    """TableIO writer class for ODT, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 lang: str = 'en-UK',
                 paper_size: PaperSize = PaperSize.A4):
        """Initialize the TableIOMformatOdt writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            lang: The language of the document.
            paper_size: Paper size for the document.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatOdt(
            file_name,
            file_exists_callback=_allow_overwrite,
            lang=lang, paper_size=paper_size)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.odt'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatOdt writer class."""
        return Descriptor(format_name='odt', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'lang', 'paper_size'])


class TableIOMformatPdf(TableIOMformatBased):
    """TableIO writer class for PDF, based on MultiFormat."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 paper_size: PaperSize = PaperSize.A4,
                 title: Optional[str] = None):
        """Initialize the TableIOMformatPdf writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            paper_size: Paper size for the document.
            title: PDF document metadata title.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatPdf(
            file_name,
            file_exists_callback=_allow_overwrite,
            paper_size=paper_size, title=title)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.pdf'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatPdf writer class."""
        return Descriptor(format_name='pdf', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'paper_size', 'title'])


class TableIOMformatRtf(TableIOMformatBased):
    """TableIO writer class for RTF, based on MultiFormat."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 paper_size: PaperSize = PaperSize.A4):
        """Initialize the TableIOMformatRtf writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when
                                  file_access is CREATE.
                                  Return to allow the file to be
                                  overwritten. Raise an exception to
                                  prevent the file from being
                                  overwritten.
                                  (May for instance save existing file
                                  as backup.)
                                  (Default is to raise an exception.)
            paper_size: Paper size for the document.
        """
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.mformat = MultiFormatRtf(
            file_name,
            file_exists_callback=_allow_overwrite,
            paper_size=paper_size)

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Get the row format capability."""
        return SingleCapability(supported=True)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.rtf'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOMformatRtf writer class."""
        return Descriptor(format_name='rtf', implementation='mformat',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=['file_exists_callback',
                                         'paper_size'])
