# Table of Contents

* [tableio.tableio](#tableio.tableio)
  * [TableIO](#tableio.tableio.TableIO)
    * [\_\_init\_\_](#tableio.tableio.TableIO.__init__)
    * [get\_description](#tableio.tableio.TableIO.get_description)
    * [get\_capabilities](#tableio.tableio.TableIO.get_capabilities)
    * [file\_name\_with\_extension](#tableio.tableio.TableIO.file_name_with_extension)
    * [file\_name\_extension](#tableio.tableio.TableIO.file_name_extension)
    * [\_\_enter\_\_](#tableio.tableio.TableIO.__enter__)
    * [\_\_exit\_\_](#tableio.tableio.TableIO.__exit__)
    * [write\_heading](#tableio.tableio.TableIO.write_heading)
    * [ImplMetaForWrite](#tableio.tableio.TableIO.ImplMetaForWrite)
    * [ImplMetaForDictWrite](#tableio.tableio.TableIO.ImplMetaForDictWrite)
    * [write\_table\_listdata](#tableio.tableio.TableIO.write_table_listdata)
    * [write\_table\_fmtlistdata](#tableio.tableio.TableIO.write_table_fmtlistdata)
    * [write\_table\_dictdata](#tableio.tableio.TableIO.write_table_dictdata)
    * [write\_table\_fmtdictdata](#tableio.tableio.TableIO.write_table_fmtdictdata)
    * [read\_table\_listdata](#tableio.tableio.TableIO.read_table_listdata)
    * [read\_table\_dictdata](#tableio.tableio.TableIO.read_table_dictdata)
    * [list\_sheets](#tableio.tableio.TableIO.list_sheets)
    * [select\_sheet](#tableio.tableio.TableIO.select_sheet)
    * [current\_sheet\_name](#tableio.tableio.TableIO.current_sheet_name)
    * [find\_value](#tableio.tableio.TableIO.find_value)
    * [read\_cells](#tableio.tableio.TableIO.read_cells)
    * [write\_cells](#tableio.tableio.TableIO.write_cells)
    * [open](#tableio.tableio.TableIO.open)
    * [close](#tableio.tableio.TableIO.close)
* [tableio.color](#tableio.color)
  * [Color](#tableio.color.Color)
    * [NONE](#tableio.color.Color.NONE)
    * [RED](#tableio.color.Color.RED)
    * [GREEN](#tableio.color.Color.GREEN)
    * [YELLOW](#tableio.color.Color.YELLOW)
* [tableio.tableio\_ods\_odfdo](#tableio.tableio_ods_odfdo)
  * [TableIOOdsOdfdo](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo)
    * [\_\_init\_\_](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.__init__)
    * [get\_capabilities](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_capabilities)
    * [get\_description](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_description)
    * [file\_name\_extension](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.file_name_extension)
    * [open](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.open)
* [tableio.tableio\_mformat](#tableio.tableio_mformat)
  * [TableIOMformatMd](#tableio.tableio_mformat.TableIOMformatMd)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatMd.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatMd.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatMd.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatMd.get_description)
  * [TableIOMformatHtml](#tableio.tableio_mformat.TableIOMformatHtml)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatHtml.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatHtml.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatHtml.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatHtml.get_description)
  * [TableIOMformatTxt](#tableio.tableio_mformat.TableIOMformatTxt)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatTxt.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatTxt.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatTxt.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatTxt.get_description)
  * [TableIOMformatLatex](#tableio.tableio_mformat.TableIOMformatLatex)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatLatex.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatLatex.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatLatex.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatLatex.get_description)
  * [TableIOMformatRst](#tableio.tableio_mformat.TableIOMformatRst)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatRst.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatRst.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatRst.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatRst.get_description)
  * [TableIOMformatDocx](#tableio.tableio_mformat.TableIOMformatDocx)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatDocx.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatDocx.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatDocx.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatDocx.get_description)
  * [TableIOMformatOdt](#tableio.tableio_mformat.TableIOMformatOdt)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatOdt.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatOdt.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatOdt.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatOdt.get_description)
  * [TableIOMformatPdf](#tableio.tableio_mformat.TableIOMformatPdf)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatPdf.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatPdf.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatPdf.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatPdf.get_description)
  * [TableIOMformatRtf](#tableio.tableio_mformat.TableIOMformatRtf)
    * [\_\_init\_\_](#tableio.tableio_mformat.TableIOMformatRtf.__init__)
    * [get\_row\_format\_capability](#tableio.tableio_mformat.TableIOMformatRtf.get_row_format_capability)
    * [file\_name\_extension](#tableio.tableio_mformat.TableIOMformatRtf.file_name_extension)
    * [get\_description](#tableio.tableio_mformat.TableIOMformatRtf.get_description)
* [tableio.tableio\_textbased](#tableio.tableio_textbased)
  * [TableIOTextBased](#tableio.tableio_textbased.TableIOTextBased)
    * [\_\_init\_\_](#tableio.tableio_textbased.TableIOTextBased.__init__)
    * [open](#tableio.tableio_textbased.TableIOTextBased.open)
* [tableio.tableio\_excel\_pylightxl](#tableio.tableio_excel_pylightxl)
  * [\_WorksheetLike](#tableio.tableio_excel_pylightxl._WorksheetLike)
    * [update\_address](#tableio.tableio_excel_pylightxl._WorksheetLike.update_address)
  * [TableIOExcelPylightxl](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl)
    * [\_\_init\_\_](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.__init__)
    * [get\_description](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_description)
    * [get\_capabilities](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_capabilities)
    * [open](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.open)
* [tableio.optional\_args](#tableio.optional_args)
  * [CsvDialect](#tableio.optional_args.CsvDialect)
    * [EXCEL](#tableio.optional_args.CsvDialect.EXCEL)
    * [UNIX](#tableio.optional_args.CsvDialect.UNIX)
  * [OptionalArgsDict](#tableio.optional_args.OptionalArgsDict)
    * [csv\_type](#tableio.optional_args.OptionalArgsDict.csv_type)
    * [csv\_delimiter](#tableio.optional_args.OptionalArgsDict.csv_delimiter)
    * [csv\_quoting](#tableio.optional_args.OptionalArgsDict.csv_quoting)
    * [csv\_quotechar](#tableio.optional_args.OptionalArgsDict.csv_quotechar)
    * [csv\_lineterminator](#tableio.optional_args.OptionalArgsDict.csv_lineterminator)
    * [csv\_escapechar](#tableio.optional_args.OptionalArgsDict.csv_escapechar)
  * [mformat\_optargs\_from\_optionalargs](#tableio.optional_args.mformat_optargs_from_optionalargs)
* [tableio.factory](#tableio.factory)
  * [TableIOFactoryConflictError](#tableio.factory.TableIOFactoryConflictError)
  * [TableIOFactoryNoSuchError](#tableio.factory.TableIOFactoryNoSuchError)
  * [TableIOFactoryNoCapabilityMatch](#tableio.factory.TableIOFactoryNoCapabilityMatch)
  * [InsufficientCapabilities](#tableio.factory.InsufficientCapabilities)
  * [ImplPrio](#tableio.factory.ImplPrio)
    * [format\_name](#tableio.factory.ImplPrio.format_name)
    * [implementation](#tableio.factory.ImplPrio.implementation)
    * [priority](#tableio.factory.ImplPrio.priority)
    * [\_\_lt\_\_](#tableio.factory.ImplPrio.__lt__)
    * [\_\_eq\_\_](#tableio.factory.ImplPrio.__eq__)
  * [BestMatch](#tableio.factory.BestMatch)
    * [strict\_matches](#tableio.factory.BestMatch.strict_matches)
    * [nonstrict\_matches](#tableio.factory.BestMatch.nonstrict_matches)
    * [from\_lists](#tableio.factory.BestMatch.from_lists)
    * [\_\_len\_\_](#tableio.factory.BestMatch.__len__)
    * [combined](#tableio.factory.BestMatch.combined)
    * [add](#tableio.factory.BestMatch.add)
    * [add\_list](#tableio.factory.BestMatch.add_list)
  * [FactoryFormatInfo](#tableio.factory.FactoryFormatInfo)
    * [\_\_init\_\_](#tableio.factory.FactoryFormatInfo.__init__)
    * [add\_implementation](#tableio.factory.FactoryFormatInfo.add_implementation)
    * [best\_match\_names](#tableio.factory.FactoryFormatInfo.best_match_names)
    * [correct\_implementation\_name](#tableio.factory.FactoryFormatInfo.correct_implementation_name)
  * [TableIOFactory](#tableio.factory.TableIOFactory)
    * [\_\_init\_\_](#tableio.factory.TableIOFactory.__init__)
    * [i\_get\_factory](#tableio.factory.TableIOFactory.i_get_factory)
    * [register](#tableio.factory.TableIOFactory.register)
    * [i\_register](#tableio.factory.TableIOFactory.i_register)
    * [create](#tableio.factory.TableIOFactory.create)
    * [i\_create](#tableio.factory.TableIOFactory.i_create)
    * [filter\_args](#tableio.factory.TableIOFactory.filter_args)
    * [i\_filter\_args](#tableio.factory.TableIOFactory.i_filter_args)
    * [get\_registered\_formats](#tableio.factory.TableIOFactory.get_registered_formats)
    * [i\_get\_registered\_formats](#tableio.factory.TableIOFactory.i_get_registered_formats)
    * [get\_registered\_implementations](#tableio.factory.TableIOFactory.get_registered_implementations)
    * [i\_get\_registered\_implementations](#tableio.factory.TableIOFactory.i_get_registered_implementations)
    * [get\_usage](#tableio.factory.TableIOFactory.get_usage)
    * [i\_get\_usage](#tableio.factory.TableIOFactory.i_get_usage)
  * [create\_tableio](#tableio.factory.create_tableio)
  * [filter\_args\_tableio](#tableio.factory.filter_args_tableio)
  * [list\_registered\_tableio](#tableio.factory.list_registered_tableio)
  * [list\_implementations\_tableio](#tableio.factory.list_implementations_tableio)
  * [usage\_tableio](#tableio.factory.usage_tableio)
  * [register\_tableio](#tableio.factory.register_tableio)
* [tableio.value\_type](#tableio.value_type)
  * [Fmt](#tableio.value_type.Fmt)
    * [bold](#tableio.value_type.Fmt.bold)
    * [italic](#tableio.value_type.Fmt.italic)
    * [highlight](#tableio.value_type.Fmt.highlight)
  * [ValueFmt](#tableio.value_type.ValueFmt)
    * [value](#tableio.value_type.ValueFmt.value)
    * [fmt](#tableio.value_type.ValueFmt.fmt)
  * [FmtListRow](#tableio.value_type.FmtListRow)
    * [values](#tableio.value_type.FmtListRow.values)
    * [fmt](#tableio.value_type.FmtListRow.fmt)
  * [FmtDictRow](#tableio.value_type.FmtDictRow)
    * [values](#tableio.value_type.FmtDictRow.values)
    * [fmt](#tableio.value_type.FmtDictRow.fmt)
  * [ReadResult](#tableio.value_type.ReadResult)
    * [data](#tableio.value_type.ReadResult.data)
    * [headings](#tableio.value_type.ReadResult.headings)
    * [last\_read\_row](#tableio.value_type.ReadResult.last_read_row)
  * [fmt\_set\_in\_both](#tableio.value_type.fmt_set_in_both)
  * [fmt\_set\_in\_all](#tableio.value_type.fmt_set_in_all)
  * [get\_plain\_value](#tableio.value_type.get_plain_value)
  * [value\_to\_str](#tableio.value_type.value_to_str)
  * [list\_row\_to\_str\_list](#tableio.value_type.list_row_to_str_list)
  * [dict\_row\_to\_str\_dict](#tableio.value_type.dict_row_to_str_dict)
  * [str\_list\_to\_list\_row](#tableio.value_type.str_list_to_list_row)
  * [get\_checked\_type](#tableio.value_type.get_checked_type)
  * [has\_format\_list](#tableio.value_type.has_format_list)
  * [is\_plain\_list\_data](#tableio.value_type.is_plain_list_data)
  * [strip\_format\_list](#tableio.value_type.strip_format_list)
  * [has\_format\_dict](#tableio.value_type.has_format_dict)
  * [is\_plain\_dict\_data](#tableio.value_type.is_plain_dict_data)
  * [strip\_format\_dict](#tableio.value_type.strip_format_dict)
  * [row\_strip\_format\_list](#tableio.value_type.row_strip_format_list)
  * [row\_strip\_format\_dict](#tableio.value_type.row_strip_format_dict)
  * [row\_format\_each\_cell\_list](#tableio.value_type.row_format_each_cell_list)
  * [row\_format\_each\_cell\_dict](#tableio.value_type.row_format_each_cell_dict)
  * [format\_each\_cell\_list](#tableio.value_type.format_each_cell_list)
  * [format\_each\_cell\_dict](#tableio.value_type.format_each_cell_dict)
  * [row\_fmt\_from\_cell\_fmt\_list](#tableio.value_type.row_fmt_from_cell_fmt_list)
  * [row\_fmt\_from\_cell\_fmt\_dict](#tableio.value_type.row_fmt_from_cell_fmt_dict)
  * [MissingDataForColumn](#tableio.value_type.MissingDataForColumn)
    * [\_\_init\_\_](#tableio.value_type.MissingDataForColumn.__init__)
  * [DataForExtraColumn](#tableio.value_type.DataForExtraColumn)
    * [\_\_init\_\_](#tableio.value_type.DataForExtraColumn.__init__)
  * [normalize\_dict\_data](#tableio.value_type.normalize_dict_data)
* [tableio.\_archive\_rewrite](#tableio._archive_rewrite)
  * [temporary\_output\_path](#tableio._archive_rewrite.temporary_output_path)
  * [rewrite\_zip\_archive](#tableio._archive_rewrite.rewrite_zip_archive)
* [tableio.valueconversion](#tableio.valueconversion)
  * [UnreasonableTypeConversion](#tableio.valueconversion.UnreasonableTypeConversion)
    * [\_\_init\_\_](#tableio.valueconversion.UnreasonableTypeConversion.__init__)
  * [UnreasonableValueConversion](#tableio.valueconversion.UnreasonableValueConversion)
    * [\_\_init\_\_](#tableio.valueconversion.UnreasonableValueConversion.__init__)
  * [value2str](#tableio.valueconversion.value2str)
  * [value2bool](#tableio.valueconversion.value2bool)
  * [value2int](#tableio.valueconversion.value2int)
  * [value2float](#tableio.valueconversion.value2float)
  * [value2datetime](#tableio.valueconversion.value2datetime)
  * [value2date](#tableio.valueconversion.value2date)
  * [value2time](#tableio.valueconversion.value2time)
  * [value2none](#tableio.valueconversion.value2none)
  * [value2type](#tableio.valueconversion.value2type)
  * [value2type\_of](#tableio.valueconversion.value2type_of)
* [tableio.tableio\_types](#tableio.tableio_types)
  * [Descriptor](#tableio.tableio_types.Descriptor)
    * [format\_name](#tableio.tableio_types.Descriptor.format_name)
    * [implementation](#tableio.tableio_types.Descriptor.implementation)
    * [capabilities](#tableio.tableio_types.Descriptor.capabilities)
    * [mandatory\_args](#tableio.tableio_types.Descriptor.mandatory_args)
    * [optional\_args](#tableio.tableio_types.Descriptor.optional_args)
    * [priority](#tableio.tableio_types.Descriptor.priority)
  * [Box](#tableio.tableio_types.Box)
  * [Position](#tableio.tableio_types.Position)
  * [FileAccess](#tableio.tableio_types.FileAccess)
    * [READ](#tableio.tableio_types.FileAccess.READ)
    * [CREATE](#tableio.tableio_types.FileAccess.CREATE)
    * [UPDATE](#tableio.tableio_types.FileAccess.UPDATE)
* [tableio.capability](#tableio.capability)
  * [Strictness](#tableio.capability.Strictness)
    * [STRICT](#tableio.capability.Strictness.STRICT)
    * [IGNORE](#tableio.capability.Strictness.IGNORE)
  * [SingleCapability](#tableio.capability.SingleCapability)
    * [supported](#tableio.capability.SingleCapability.supported)
    * [strictness](#tableio.capability.SingleCapability.strictness)
  * [Capabilities](#tableio.capability.Capabilities)
    * [can\_write](#tableio.capability.Capabilities.can_write)
    * [can\_read](#tableio.capability.Capabilities.can_read)
    * [can\_fmt\_row](#tableio.capability.Capabilities.can_fmt_row)
    * [can\_fmt\_value](#tableio.capability.Capabilities.can_fmt_value)
    * [filtered\_data\_range](#tableio.capability.Capabilities.filtered_data_range)
    * [can\_write\_box](#tableio.capability.Capabilities.can_write_box)
    * [can\_read\_box](#tableio.capability.Capabilities.can_read_box)
    * [can\_write\_highlight](#tableio.capability.Capabilities.can_write_highlight)
    * [multi\_sheet](#tableio.capability.Capabilities.multi_sheet)
    * [can\_find\_value\_position](#tableio.capability.Capabilities.can_find_value_position)
  * [single\_capability\_match](#tableio.capability.single_capability_match)
  * [capability\_match](#tableio.capability.capability_match)
  * [CapabilityNotSupported](#tableio.capability.CapabilityNotSupported)
    * [\_\_init\_\_](#tableio.capability.CapabilityNotSupported.__init__)
  * [capability\_to\_str](#tableio.capability.capability_to_str)
  * [CAP\_NOT\_USED](#tableio.capability.CAP_NOT_USED)
  * [CAP\_NEEDED](#tableio.capability.CAP_NEEDED)
  * [CAP\_IGNORABLE](#tableio.capability.CAP_IGNORABLE)
  * [CAP\_IMPLEMENTED](#tableio.capability.CAP_IMPLEMENTED)
  * [CAP\_IGNORED](#tableio.capability.CAP_IGNORED)
  * [CAP\_UNSUPPORTED](#tableio.capability.CAP_UNSUPPORTED)
* [tableio.tableio\_excel\_xlsxwriter](#tableio.tableio_excel_xlsxwriter)
  * [\_WorksheetLike](#tableio.tableio_excel_xlsxwriter._WorksheetLike)
    * [add\_table](#tableio.tableio_excel_xlsxwriter._WorksheetLike.add_table)
    * [set\_column](#tableio.tableio_excel_xlsxwriter._WorksheetLike.set_column)
    * [write](#tableio.tableio_excel_xlsxwriter._WorksheetLike.write)
    * [write\_blank](#tableio.tableio_excel_xlsxwriter._WorksheetLike.write_blank)
  * [\_WorkbookLike](#tableio.tableio_excel_xlsxwriter._WorkbookLike)
    * [add\_worksheet](#tableio.tableio_excel_xlsxwriter._WorkbookLike.add_worksheet)
    * [add\_format](#tableio.tableio_excel_xlsxwriter._WorkbookLike.add_format)
    * [close](#tableio.tableio_excel_xlsxwriter._WorkbookLike.close)
  * [TableIOExcelXlsxWriter](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter)
    * [\_\_init\_\_](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.__init__)
    * [get\_capabilities](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_capabilities)
    * [get\_description](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_description)
    * [open](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.open)
* [tableio.tableio\_csv](#tableio.tableio_csv)
  * [CsvDefinitions](#tableio.tableio_csv.CsvDefinitions)
    * [type](#tableio.tableio_csv.CsvDefinitions.type)
    * [delimiter](#tableio.tableio_csv.CsvDefinitions.delimiter)
    * [quoting](#tableio.tableio_csv.CsvDefinitions.quoting)
    * [quotechar](#tableio.tableio_csv.CsvDefinitions.quotechar)
    * [lineterminator](#tableio.tableio_csv.CsvDefinitions.lineterminator)
    * [escapechar](#tableio.tableio_csv.CsvDefinitions.escapechar)
  * [TableIOCsv](#tableio.tableio_csv.TableIOCsv)
    * [\_\_init\_\_](#tableio.tableio_csv.TableIOCsv.__init__)
    * [file\_name\_extension](#tableio.tableio_csv.TableIOCsv.file_name_extension)
    * [get\_description](#tableio.tableio_csv.TableIOCsv.get_description)
    * [get\_capabilities](#tableio.tableio_csv.TableIOCsv.get_capabilities)
* [tableio.tableio\_spreadsheetbased](#tableio.tableio_spreadsheetbased)
  * [excel\_column\_name](#tableio.tableio_spreadsheetbased.excel_column_name)
  * [TableIOSpreadsheetBased](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased)
    * [\_\_init\_\_](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased.__init__)
* [tableio.tableio\_mformatbased](#tableio.tableio_mformatbased)
  * [TableIOMformatBased](#tableio.tableio_mformatbased.TableIOMformatBased)
    * [\_\_init\_\_](#tableio.tableio_mformatbased.TableIOMformatBased.__init__)
    * [get\_capabilities](#tableio.tableio_mformatbased.TableIOMformatBased.get_capabilities)
    * [get\_row\_format\_capability](#tableio.tableio_mformatbased.TableIOMformatBased.get_row_format_capability)
    * [open](#tableio.tableio_mformatbased.TableIOMformatBased.open)
* [tableio.tableio\_excelbased](#tableio.tableio_excelbased)
  * [TableIOExcelBased](#tableio.tableio_excelbased.TableIOExcelBased)
    * [\_\_init\_\_](#tableio.tableio_excelbased.TableIOExcelBased.__init__)
    * [file\_name\_extension](#tableio.tableio_excelbased.TableIOExcelBased.file_name_extension)
* [tableio.reg\_pkg\_formats](#tableio.reg_pkg_formats)
  * [register\_formats\_in\_pkg](#tableio.reg_pkg_formats.register_formats_in_pkg)
* [tableio.tableio\_excel\_openpyxl](#tableio.tableio_excel_openpyxl)
  * [TableIOExcelOpenPyXL](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL)
    * [\_\_init\_\_](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.__init__)
    * [get\_capabilities](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_capabilities)
    * [get\_description](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_description)
    * [open](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.open)

<a id="tableio.tableio"></a>

# tableio.tableio

Reader/writer base class for a file format.

<a id="tableio.tableio.TableIO"></a>

## TableIO Objects

```python
class TableIO()
```

File format reader/writer base class for table data.

<a id="tableio.tableio.TableIO.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the TableIO reader/writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if the file
  already exists when file_access is CREATE.
  Return to allow the file to be overwritten.
  Raise an exception to prevent the file from
  being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="tableio.tableio.TableIO.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the reader/writer class.

Must be overridden by subclasses.
An implementation that produce the same file format but with
stricter adherance to the file format specification or
better compatibitity with other software should have
a higher priority (even it has fewer capabilities).

<a id="tableio.tableio.TableIO.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the capabilities of the reader/writer class.

Must be overridden by subclasses.

<a id="tableio.tableio.TableIO.file_name_with_extension"></a>

#### file\_name\_with\_extension

```python
@staticmethod
def file_name_with_extension(file_name: PathLike, extension: str) -> str
```

Return the file name with the extension.

<a id="tableio.tableio.TableIO.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Return the extension of the file name.

<a id="tableio.tableio.TableIO.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__() -> 'TableIO'
```

Enter the context manager.

<a id="tableio.tableio.TableIO.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type: type[BaseException] | None,
             exc_value: BaseException | None,
             traceback: TracebackType | None) -> bool
```

Exit the context manager.

Closes the file. If the with block raised an exception,
close errors are noted on it to preserve it as primary.

**Arguments**:

- `exc_type` - The type of the exception.
- `exc_value` - The value of the exception.
- `traceback` - The traceback of the exception.

**Returns**:

  False if an exception should propagate, True otherwise.

<a id="tableio.tableio.TableIO.write_heading"></a>

#### write\_heading

```python
def write_heading(heading: str, level: Optional[int] = None) -> Position
```

Write a heading to the file.

Write a heading to the file. Headings are a line between tables.
For example in CSV format the heading has an empty line before and
after and it starts with one or more '#' characters.
Do not confuse the heading with the first row of a table,
with the names of the columns.

**Arguments**:

- `heading` - The heading text to write.
- `level` - The level of the heading. 1 = highest, 3 = lowest.
  If level is None and it is first heading in the sheet,
  level 1 is used.
  If level is None and it is not first heading in the sheet,
  level 2 is used.

**Raises**:

- `ValueError` - If level is outside the range 1 to 3.
- `io.UnsupportedOperation` - If the file is opened for reading.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO.ImplMetaForWrite"></a>

## ImplMetaForWrite Objects

```python
class ImplMetaForWrite(NamedTuple)
```

Meta data for writing table to pass to implementation.

<a id="tableio.tableio.TableIO.ImplMetaForWrite.filtered_data_range"></a>

#### filtered\_data\_range

If True, data will be written as a range that can be filtered.

<a id="tableio.tableio.TableIO.ImplMetaForWrite.box"></a>

#### box

The box to write the data into.

<a id="tableio.tableio.TableIO.ImplMetaForDictWrite"></a>

## ImplMetaForDictWrite Objects

```python
class ImplMetaForDictWrite(NamedTuple)
```

Meta data for writing dict table to pass to implementation.

<a id="tableio.tableio.TableIO.ImplMetaForDictWrite.common_impl"></a>

#### common\_impl

Common meta data for writing dict/list to pass to implementation.

<a id="tableio.tableio.TableIO.ImplMetaForDictWrite.column_order"></a>

#### column\_order

The order of the columns.

<a id="tableio.tableio.TableIO.ImplMetaForDictWrite.first_row_format"></a>

#### first\_row\_format

The format specification for the first row.

<a id="tableio.tableio.TableIO.write_table_listdata"></a>

#### write\_table\_listdata

```python
def write_table_listdata(data: ListDataSeq[CellT],
                         filtered_data_range: bool = False,
                         box: Optional[Box] = None) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when spefifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The list data to write.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.

**Raises**:

- `ValueError` - If the data shape is invalid or does not fit in box.
- `CapabilityNotSupported` - If a requested capability is unsupported
  and strict.
- `io.UnsupportedOperation` - If the file is opened for reading.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO.write_table_fmtlistdata"></a>

#### write\_table\_fmtlistdata

```python
def write_table_fmtlistdata(data: FmtListData,
                            filtered_data_range: bool = False,
                            box: Optional[Box] = None) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when spefifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The list data to write.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.

**Raises**:

- `ValueError` - If the data shape is invalid or does not fit in box.
- `CapabilityNotSupported` - If a requested capability is unsupported
  and strict.
- `io.UnsupportedOperation` - If the file is opened for reading.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO.write_table_dictdata"></a>

#### write\_table\_dictdata

```python
def write_table_dictdata(data: DictDataMap[CellT],
                         column_order: list[str],
                         first_row_format: Optional[Fmt] = None,
                         missing_ok: bool = False,
                         extra_ok: bool = False,
                         filtered_data_range: bool = False,
                         box: Optional[Box] = None) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when spefifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The dict data to write.
- `column_order` - The order of the columns.
- `first_row_format` - The format specification for the first row.
  The table will get a first row with the names
  of the columns. This format specification will
  be applied to the first row. If None, no format
  will be applied to the first row.
- `missing_ok` - If True, None is inserted for missing column data.
  If False, an exception is raised.
- `extra_ok` - If True, data for extra columns are ignored.
  If False, an exception is raised if data for extra
  columns are present.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.

**Raises**:

- `ValueError` - If missing_ok is False and data is missing for a
  column in the column_order.
- `ValueError` - If extra_ok is False and data is present for a
  key not in the column_order.
- `ValueError` - If the data shape is invalid or does not fit in box.
- `CapabilityNotSupported` - If a requested capability is unsupported
  and strict.
- `io.UnsupportedOperation` - If the file is opened for reading.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO.write_table_fmtdictdata"></a>

#### write\_table\_fmtdictdata

```python
def write_table_fmtdictdata(data: FmtDictData,
                            column_order: list[str],
                            first_row_format: Optional[Fmt] = None,
                            missing_ok: bool = False,
                            extra_ok: bool = False,
                            filtered_data_range: bool = False,
                            box: Optional[Box] = None) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when spefifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The dict data to write.
- `column_order` - The order of the columns.
- `first_row_format` - The format specification for the first row.
  The table will get a first row with the names
  of the columns. This format specification will
  be applied to the first row. If None, no format
  will be applied to the first row.
- `missing_ok` - If True, None is inserted for missing column data.
  If False, an exception is raised.
- `extra_ok` - If True, data for extra columns are ignored.
  If False, an exception is raised if data for extra
  columns are present.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.

**Raises**:

- `ValueError` - If missing_ok is False and data is missing for a
  column in the column_order.
- `ValueError` - If extra_ok is False and data is present for a
  key not in the column_order.
- `ValueError` - If the data shape is invalid or does not fit in box.
- `CapabilityNotSupported` - If a requested capability is unsupported
  and strict.
- `io.UnsupportedOperation` - If the file is opened for reading.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO.read_table_listdata"></a>

#### read\_table\_listdata

```python
def read_table_listdata(
        box: Optional[Box] = None) -> ReadResult[ListData[Value]]
```

Read a table of list data from the file.

If a box is provided the data will be read from the box, and the
reading is restricted to the box.
Anything found in the leftmost column that does form a table of at
least 2 cells in size is considered to be a heading and is returned
as a list of headings.

**Arguments**:

- `box` - The box to read the data from.

**Raises**:

- `CapabilityNotSupported` - If reading from a box is unsupported and
  strict.

**Returns**:

  The data read from the table and the headings before the table.

<a id="tableio.tableio.TableIO.read_table_dictdata"></a>

#### read\_table\_dictdata

```python
def read_table_dictdata(
        box: Optional[Box] = None) -> ReadResult[DictData[Value]]
```

Read a table of dict data from the file.

If a box is provided the data will be read from the box, and the
reading is restricted to the box.
Anything found in the leftmost column that does form a table of
at least 2 cells in size is considered to be a heading and is
returned as a list of headings.

**Arguments**:

- `box` - The box to read the data from.

**Raises**:

- `CapabilityNotSupported` - If reading from a box is unsupported and
  strict.

**Returns**:

  The data read from the table and the headings before the table.

<a id="tableio.tableio.TableIO.list_sheets"></a>

#### list\_sheets

```python
def list_sheets() -> list[str]
```

List the sheets in the file.

**Returns**:

  A list of the sheet names. Sheet names are case preserving,
  but compared case insensitively.

**Raises**:

- `CapabilityNotSupported` - If multiple sheets are not supported.

<a id="tableio.tableio.TableIO.select_sheet"></a>

#### select\_sheet

```python
def select_sheet(sheet_name: str, create: bool = False) -> None
```

Select a sheet in the file.

Select a sheet in the file that will be used for subsequent writes
and reads. Cursor positions (read and write positions) are per sheet.

**Arguments**:

- `sheet_name` - The name of the sheet to select. Sheet names are
  case preserving, but compared case insensitively.
- `create` - If True, create the sheet if it does not exist.

**Raises**:

- `CapabilityNotSupported` - If multiple sheets are not supported.
- `KeyError` - If the sheet name is not found and create is False.
- `io.UnsupportedOperation` - If create is True, the sheet does not
  exist, and the file is opened for
  reading.

<a id="tableio.tableio.TableIO.current_sheet_name"></a>

#### current\_sheet\_name

```python
def current_sheet_name() -> str
```

Return the name of the current sheet.

**Returns**:

  The name of the current sheet. Sheet names are case preserving,
  but compared case insensitively.

**Raises**:

- `CapabilityNotSupported` - If multiple sheets are not supported.

<a id="tableio.tableio.TableIO.find_value"></a>

#### find\_value

```python
def find_value(find_value: Value | ListDataSeq[Value],
               type_conversion: bool = True,
               box: Optional[Box] = None) -> Optional[Box]
```

Find the position of a value or values in the file.

Search for a position of a value or values in the current sheet of
the file. The first position found is returned.
If several matching values are present, the first found is returned.
Here "first" means on a lower row index, and if row indices are equal,
on a lower column index.
For comparison the value in a cell is first compared without type
conversion, mismatching if types differ.
Then type conversion to each corresponding find_value cell is
attempted using value2type_of(...), if allowed by type_conversion.

**Arguments**:

- `find_value` - The value or values to find. A rectangular area of
  values to find. A single value is used as a 1x1 area.
- `type_conversion` - If True, each cell value in the searched area is
  also converted to the type of the corresponding
  find_value cell for comparison. If False, no type
  conversion is attempted.
- `box` - Search within this box. If None, the entire current sheet is
  searched.

**Raises**:

- `CapabilityNotSupported` - If find_value_position capability is not
  supported.

**Returns**:

  A box tightly fitting around the first found value or values.
  None if no matching value is found.

<a id="tableio.tableio.TableIO.read_cells"></a>

#### read\_cells

```python
def read_cells(box: Box) -> ListData[Value]
```

Read the cells in the current sheet of the file.

Read cells from the box position in the current sheet of the file.
The cell reading is independent of the table positions in the file.
This call does not affect the cursor position.

**Arguments**:

- `box` - The box to read the cells from. Neither of box.bottom or
  box.right may be None.

**Raises**:

- `ValueError` - If box.bottom or box.right is None.
- `CapabilityNotSupported` - If reading from a box is unsupported.

**Returns**:

  The values of the cells read from the file.

<a id="tableio.tableio.TableIO.write_cells"></a>

#### write\_cells

```python
def write_cells(data: ListDataSeq[CellT], box: Box) -> None
```

Write the cells to the current sheet of the file.

Write cells to the box position in the current sheet of the file.
The cell writing is independent of the table positions in the file.
This call does not affect the cursor position.
Notice: This method allows writing of cells to arbitrary positions
in the file, which might destroy table and heading structures, and
may make it impossible to read the file back into a table. It is
the responsibility of the caller to ensure that the file keeps
a valid structure for whatever purpose the file is intended for.

**Arguments**:

- `data` - The data to write.
- `box` - The box to write the cells to. If box.bottom or box.right is
  not None, the data must fill the box.

**Raises**:

- `ValueError` - If box.bottom or box.right is not None and the data
  does not fit and fill the box.
- `CapabilityNotSupported` - If writing to a box is unsupported.
- `io.UnsupportedOperation` - If the file is opened for reading.

<a id="tableio.tableio.TableIO.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use derived class as a context manager instead, using a with statement.

<a id="tableio.tableio.TableIO.close"></a>

#### close

```python
def close() -> None
```

Close the file.

Avoid using this method directly.
Use derived class as a context manager instead, using a with statement.

<a id="tableio.color"></a>

# tableio.color

Highlight colors for the tableio package.

<a id="tableio.color.Color"></a>

## Color Objects

```python
class Color(IntEnum)
```

Highlight colors for the tableio package.

<a id="tableio.color.Color.NONE"></a>

#### NONE

No hightlight color.

<a id="tableio.color.Color.RED"></a>

#### RED

Red highlight color.

<a id="tableio.color.Color.GREEN"></a>

#### GREEN

Green highlight color.

<a id="tableio.color.Color.YELLOW"></a>

#### YELLOW

Yellow highlight color.

<a id="tableio.tableio_ods_odfdo"></a>

# tableio.tableio\_ods\_odfdo

TableIO class for OpenDocument Spreadsheet files using ODFdo.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo"></a>

## TableIOOdsOdfdo Objects

```python
class TableIOOdsOdfdo(TableIOSpreadsheetBased)
```

TableIO class for OpenDocument Spreadsheet ODS files using odfdo.

The implementation operates on one current sheet at a time.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             lang: str = 'en-UK')
```

Initialize the TableIOOdsOdfdo class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - Callback used when CREATE would overwrite.
- `lang` - The RFC3066 language code for newly created ODS files.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the standard spreadsheet backend capabilities.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOOdsOdfdo class.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension of the ODS implementation.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo.open"></a>

#### open

```python
def open() -> None
```

Open the ODS document.

<a id="tableio.tableio_mformat"></a>

# tableio.tableio\_mformat

TableIO writer classes based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatMd"></a>

## TableIOMformatMd Objects

```python
class TableIOMformatMd(TableIOMformatBased)
```

TableIO writer class for Markdown, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatMd.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8')
```

Initialize the TableIOMformatMd writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `character_encoding` - The character encoding to use.

<a id="tableio.tableio_mformat.TableIOMformatMd.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatMd.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatMd.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatMd writer class.

<a id="tableio.tableio_mformat.TableIOMformatHtml"></a>

## TableIOMformatHtml Objects

```python
class TableIOMformatHtml(TableIOMformatBased)
```

TableIO writer class for HTML, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatHtml.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8',
             title: str = 'HTML file',
             css_file: Optional[str] = None,
             lang: str = 'en')
```

Initialize the TableIOMformatHtml writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `character_encoding` - The character encoding to use.
- `title` - The title of the HTML file.
- `css_file` - The CSS file to use.
- `lang` - The language of the HTML file.

<a id="tableio.tableio_mformat.TableIOMformatHtml.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatHtml.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatHtml.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatHtml writer class.

<a id="tableio.tableio_mformat.TableIOMformatTxt"></a>

## TableIOMformatTxt Objects

```python
class TableIOMformatTxt(TableIOMformatBased)
```

TableIO writer class for plain text, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatTxt.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8',
             line_length: int = 79,
             table_max_line_length: Optional[int] = None,
             table_alignment: TableAlignmentSpec = TableAlignment.
             CENTER_BUT_DIGITS_RIGHT)
```

Initialize the TableIOMformatTxt writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `character_encoding` - The character encoding to use.
- `line_length` - The maximum length of a line.
- `table_max_line_length` - The maximum length of a line when
  writing a table. If None,
  line_length is used.
- `table_alignment` - The alignment of cell values in tables.

<a id="tableio.tableio_mformat.TableIOMformatTxt.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatTxt.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatTxt.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatTxt writer class.

<a id="tableio.tableio_mformat.TableIOMformatLatex"></a>

## TableIOMformatLatex Objects

```python
class TableIOMformatLatex(TableIOMformatBased)
```

TableIO writer class for LaTeX, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatLatex.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8',
             document_class: Optional[DocumentClassInput] = None,
             paper_size: Optional[PaperSizeInput] = None,
             title: Optional[str] = None,
             latex_preamble: str = '',
             latex_heading_levels: Optional[dict[int, str]] = None,
             latex_replacements: Optional[list[dict[str, str]]] = None)
```

Initialize the TableIOMformatLatex writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `character_encoding` - The character encoding to use.
- `document_class` - The LaTeX document class to use.
- `paper_size` - The paper size to use.
- `title` - The title of the LaTeX document.
- `latex_preamble` - Extra LaTeX preamble text.
- `latex_heading_levels` - Override heading level commands.
- `latex_replacements` - Custom text replacement stages.

<a id="tableio.tableio_mformat.TableIOMformatLatex.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatLatex.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatLatex.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatLatex writer class.

<a id="tableio.tableio_mformat.TableIOMformatRst"></a>

## TableIOMformatRst Objects

```python
class TableIOMformatRst(TableIOMformatBased)
```

TableIO writer class for reStructuredText, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatRst.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8',
             line_length: int = 79,
             table_max_line_length: Optional[int] = None,
             table_alignment: TableAlignmentSpec = TableAlignment.LEFT)
```

Initialize the TableIOMformatRst writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `character_encoding` - The character encoding to use.
- `line_length` - The maximum length of a line.
- `table_max_line_length` - The maximum length of a line when
  writing a table. If None,
  line_length is used.
- `table_alignment` - The alignment of cell values in tables.

<a id="tableio.tableio_mformat.TableIOMformatRst.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatRst.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatRst.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatRst writer class.

<a id="tableio.tableio_mformat.TableIOMformatDocx"></a>

## TableIOMformatDocx Objects

```python
class TableIOMformatDocx(TableIOMformatBased)
```

TableIO writer class for DOCX, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatDocx.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             paper_size: PaperSize = PaperSize.A4)
```

Initialize the TableIOMformatDocx writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `paper_size` - Paper size for the document.

<a id="tableio.tableio_mformat.TableIOMformatDocx.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatDocx.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatDocx.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatDocx writer class.

<a id="tableio.tableio_mformat.TableIOMformatOdt"></a>

## TableIOMformatOdt Objects

```python
class TableIOMformatOdt(TableIOMformatBased)
```

TableIO writer class for ODT, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatOdt.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             lang: str = 'en-UK',
             paper_size: PaperSize = PaperSize.A4)
```

Initialize the TableIOMformatOdt writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `lang` - The language of the document.
- `paper_size` - Paper size for the document.

<a id="tableio.tableio_mformat.TableIOMformatOdt.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatOdt.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatOdt.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatOdt writer class.

<a id="tableio.tableio_mformat.TableIOMformatPdf"></a>

## TableIOMformatPdf Objects

```python
class TableIOMformatPdf(TableIOMformatBased)
```

TableIO writer class for PDF, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatPdf.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             paper_size: PaperSize = PaperSize.A4,
             title: Optional[str] = None)
```

Initialize the TableIOMformatPdf writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `paper_size` - Paper size for the document.
- `title` - PDF document metadata title.

<a id="tableio.tableio_mformat.TableIOMformatPdf.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatPdf.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatPdf.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatPdf writer class.

<a id="tableio.tableio_mformat.TableIOMformatRtf"></a>

## TableIOMformatRtf Objects

```python
class TableIOMformatRtf(TableIOMformatBased)
```

TableIO writer class for RTF, based on MultiFormat.

<a id="tableio.tableio_mformat.TableIOMformatRtf.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             paper_size: PaperSize = PaperSize.A4)
```

Initialize the TableIOMformatRtf writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when
  file_access is CREATE.
  Return to allow the file to be
  overwritten. Raise an exception to
  prevent the file from being
  overwritten.
  (May for instance save existing file
  as backup.)
  (Default is to raise an exception.)
- `paper_size` - Paper size for the document.

<a id="tableio.tableio_mformat.TableIOMformatRtf.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Get the row format capability.

<a id="tableio.tableio_mformat.TableIOMformatRtf.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension.

<a id="tableio.tableio_mformat.TableIOMformatRtf.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOMformatRtf writer class.

<a id="tableio.tableio_textbased"></a>

# tableio.tableio\_textbased

Reader/writer base class for a text-based file format.

<a id="tableio.tableio_textbased.TableIOTextBased"></a>

## TableIOTextBased Objects

```python
class TableIOTextBased(TableIO)
```

Reader/writer base class for a text-based file format.

This intermediate base class for text-based formats exists
so that common functionality for text-based formats can be implemented
in a single place.

<a id="tableio.tableio_textbased.TableIOTextBased.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8')
```

Initialize the TableIOTextBased reader/writer class.

<a id="tableio.tableio_textbased.TableIOTextBased.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use derived class as a context manager instead, using a with statement.

<a id="tableio.tableio_excel_pylightxl"></a>

# tableio.tableio\_excel\_pylightxl

TableIO reader/writer class for Excel files using pylightxl.

<a id="tableio.tableio_excel_pylightxl._WorksheetLike"></a>

## \_WorksheetLike Objects

```python
class _WorksheetLike(Protocol)
```

Typed subset of the pylightxl worksheet API used here.

<a id="tableio.tableio_excel_pylightxl._WorksheetLike.update_address"></a>

#### update\_address

```python
def update_address(address: str, val: object) -> None
```

Update one worksheet cell by Excel address.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl"></a>

## TableIOExcelPylightxl Objects

```python
class TableIOExcelPylightxl(TableIOExcelBased)
```

TableIO reader/writer class for Excel files using pylightxl.

The backend uses pylightxl for workbook IO and keeps the public
spreadsheet semantics from TableIOSpreadsheetBased. Cell formatting and
filtered ranges are ignored because pylightxl does not write those Excel
features, but core data reads and writes, multi-sheet handling, boxed
operations and value search are supported.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
        file_name: PathLike,
        file_access: FileAccess,
        file_exists_callback: Optional[Callable[[str], None]] = None) -> None
```

Initialize the pylightxl-backed Excel reader/writer.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Return the descriptor for the pylightxl Excel backend.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the honest capabilities of the pylightxl backend.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.open"></a>

#### open

```python
def open() -> None
```

Open the workbook.

<a id="tableio.optional_args"></a>

# tableio.optional\_args

Optional arguments for the tableio package.

<a id="tableio.optional_args.CsvDialect"></a>

## CsvDialect Objects

```python
class CsvDialect(IntEnum)
```

The type of CSV file to write.

<a id="tableio.optional_args.CsvDialect.EXCEL"></a>

#### EXCEL

Excel CSV file type.

<a id="tableio.optional_args.CsvDialect.UNIX"></a>

#### UNIX

Unix CSV file type.

<a id="tableio.optional_args.OptionalArgsDict"></a>

## OptionalArgsDict Objects

```python
class OptionalArgsDict(OptArgsDict)
```

Optional arguments for the tableio package.

This is a TypedDict that describes the optional arguments that can be
passed to the factory in the tableio package.
For description of the arguments, see the class derived from TableIO
that uses the arguments.
The possible optional arguments includ the arguments in
mformat.factory.OptArgsDict plus the arguments specific to the tableio
package.

<a id="tableio.optional_args.OptionalArgsDict.csv_type"></a>

#### csv\_type

The type of CSV file to write. None for default type.

<a id="tableio.optional_args.OptionalArgsDict.csv_delimiter"></a>

#### csv\_delimiter

The delimiter to use for CSV files. None for default delimiter.

<a id="tableio.optional_args.OptionalArgsDict.csv_quoting"></a>

#### csv\_quoting

The quoting style to use for CSV files.

Allowed values (case-insensitive): 'all', 'minimal',
'nonnumeric', 'none', 'strings', 'notnull'.
None for default quoting.

<a id="tableio.optional_args.OptionalArgsDict.csv_quotechar"></a>

#### csv\_quotechar

The quote character to use for CSV files. None for default.

<a id="tableio.optional_args.OptionalArgsDict.csv_lineterminator"></a>

#### csv\_lineterminator

The line terminator to use for CSV files. None for default.

<a id="tableio.optional_args.OptionalArgsDict.csv_escapechar"></a>

#### csv\_escapechar

The escape character to use for CSV files. None for default.

<a id="tableio.optional_args.mformat_optargs_from_optionalargs"></a>

#### mformat\_optargs\_from\_optionalargs

```python
def mformat_optargs_from_optionalargs(
        optional_args: OptionalArgs) -> Optional[OptArgsDict]
```

Convert the optional arguments to a dictionary of arguments for mformat.

**Arguments**:

- `optional_args` - The optional arguments to convert.

**Returns**:

  A dictionary of arguments for mformat.

<a id="tableio.factory"></a>

# tableio.factory

Factory class for creating TableIO instances.

<a id="tableio.factory.TableIOFactoryConflictError"></a>

## TableIOFactoryConflictError Objects

```python
class TableIOFactoryConflictError(ValueError)
```

Raised when trying to register conflicting class.

Error raised when a format is registered with the factory
that conflicts with an existing format or existing implementation.
The conflict may be that user is trying to register the same
class twice, or that another class has the same format name or
implementation name when comparing case insensitively.

<a id="tableio.factory.TableIOFactoryNoSuchError"></a>

## TableIOFactoryNoSuchError Objects

```python
class TableIOFactoryNoSuchError(KeyError)
```

Raised when requesting a format/implementation that is not registered.

Error raised when requesting a format or implementation with a
format name or implementation name that is not registered.

<a id="tableio.factory.TableIOFactoryNoCapabilityMatch"></a>

## TableIOFactoryNoCapabilityMatch Objects

```python
class TableIOFactoryNoCapabilityMatch(ValueError)
```

Raised when requested capabilities cannot be matched.

Error raised when requested capabilities cannot be matched to any
available implementation. This can be that the requester is requesting
capabilities that are not supported by any available format or
implementation, or that the requester is requesting a specific
format name or implementation name, and the implementation(s)
with those name(s) do not support the requested capabilities.

<a id="tableio.factory.InsufficientCapabilities"></a>

## InsufficientCapabilities Objects

```python
class InsufficientCapabilities(ValueError)
```

Raised when requested capabilities contradict requested file access.

Error raised when the caller supplies both file access and an explicit
Capabilities object, but the requested capabilities do not include the
capability implied by that access mode. For example, READ requires
can_read, CREATE requires can_write, and UPDATE requires both.

<a id="tableio.factory.ImplPrio"></a>

## ImplPrio Objects

```python
@total_ordering
class ImplPrio(NamedTuple)
```

Priority of an implementation.

<a id="tableio.factory.ImplPrio.format_name"></a>

#### format\_name

The name of the format.

<a id="tableio.factory.ImplPrio.implementation"></a>

#### implementation

The name of the implementation.

<a id="tableio.factory.ImplPrio.priority"></a>

#### priority

The priority of the implementation.

<a id="tableio.factory.ImplPrio.__lt__"></a>

#### \_\_lt\_\_

```python
def __lt__(other: object) -> bool
```

Compare two implementation priorities.

<a id="tableio.factory.ImplPrio.__eq__"></a>

#### \_\_eq\_\_

```python
def __eq__(other: object) -> bool
```

Compare two implementation priorities.

<a id="tableio.factory.BestMatch"></a>

## BestMatch Objects

```python
class BestMatch(NamedTuple)
```

Best matches for requested capabilities.

This is used to store the best matches for requested capabilities.
The best matches are stored in tuples of ImplPrio objects.
The tuples are sorted by priority, from highest to lowest.
The first tuple strictly matches the requested capabilities
(that is the class can achieve all of the requested capabilities).
The second tuple contains implementations that can tolerate
all of the requested capabilities, but may ignore some of
the requested capabilities.

<a id="tableio.factory.BestMatch.strict_matches"></a>

#### strict\_matches

The implementations that strictly match the requested capabilities.

<a id="tableio.factory.BestMatch.nonstrict_matches"></a>

#### nonstrict\_matches

Implementations that tolerate but may ignore some capabilities.

<a id="tableio.factory.BestMatch.from_lists"></a>

#### from\_lists

```python
@staticmethod
def from_lists(strict_matches: list[ImplPrio],
               nonstrict_matches: list[ImplPrio]) -> 'BestMatch'
```

Initialize a BestMatch object.

<a id="tableio.factory.BestMatch.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Get the number of best matches.

<a id="tableio.factory.BestMatch.combined"></a>

#### combined

```python
def combined() -> list[ImplPrio]
```

Get the combined list of best matches.

<a id="tableio.factory.BestMatch.add"></a>

#### add

```python
@staticmethod
def add(first: 'BestMatch', second: 'BestMatch') -> 'BestMatch'
```

Add two best matches.

<a id="tableio.factory.BestMatch.add_list"></a>

#### add\_list

```python
@staticmethod
def add_list(best_matches: list['BestMatch']) -> 'BestMatch'
```

Add a list of best matches.

<a id="tableio.factory.FactoryFormatInfo"></a>

## FactoryFormatInfo Objects

```python
class FactoryFormatInfo()
```

Information about a format registered with the factory.

This is used to store the information about a format registered with the
factory. For each format there may be several implementations, each with
different capabilities.
The TableIOFactory class will store the information about the formats in a
dictionary, with the format name as the key, and objects of this class as
the values.
Objects of this class will store the information about the different
implementations of the format.

<a id="tableio.factory.FactoryFormatInfo.__init__"></a>

#### \_\_init\_\_

```python
def __init__(format_class: Optional[type[TableIO]] = None) -> None
```

Initialize the FactoryFormatInfo object.

<a id="tableio.factory.FactoryFormatInfo.add_implementation"></a>

#### add\_implementation

```python
def add_implementation(format_class: type[TableIO]) -> None
```

Add an implementation of a format to the factory.

<a id="tableio.factory.FactoryFormatInfo.best_match_names"></a>

#### best\_match\_names

```python
def best_match_names(capabilities: Optional[Capabilities] = None,
                     empty_is_ok: bool = False) -> BestMatch
```

Get the best matching implementation names for the capabilities.

**Arguments**:

- `capabilities` - The capabilities to match. If not specified,
  all implementations are included in the return
  value.
- `empty_is_ok` - If True, an empty list is returned if no
  implementations match the capabilities.
  If False, a TableIOFactoryNoCapabilityMatch
  error is raised.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - If empty_is_ok is False and
  no implementations match the
  capabilities.

**Returns**:

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

<a id="tableio.factory.FactoryFormatInfo.correct_implementation_name"></a>

#### correct\_implementation\_name

```python
def correct_implementation_name(implementation_name: str) -> str
```

Correct the implementation name to the correct case.

<a id="tableio.factory.TableIOFactory"></a>

## TableIOFactory Objects

```python
class TableIOFactory()
```

Factory class for creating instances of TableIO subclasses.

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

<a id="tableio.factory.TableIOFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize the factory with an empty registry.

<a id="tableio.factory.TableIOFactory.i_get_factory"></a>

#### i\_get\_factory

```python
@staticmethod
def i_get_factory() -> 'TableIOFactory'
```

Internally get the factory instance.

<a id="tableio.factory.TableIOFactory.register"></a>

#### register

```python
@staticmethod
def register(format_class: type[TableIO]) -> None
```

Register a TableIO subclass with the factory.

Several implementations of the same format may be registered.
Each implementation may have different capabilities.

**Arguments**:

- `format_class` - The TableIO subclass to register.

**Raises**:

- `ValueError` - If the format_class is not a subclass of TableIO.
- `TableIOFactoryConflictError` - If the format_class is already
  registered, or the names conflict
  with another registered format.

<a id="tableio.factory.TableIOFactory.i_register"></a>

#### i\_register

```python
def i_register(format_class: type[TableIO]) -> None
```

Internally register a TableIO subclass with the factory.

<a id="tableio.factory.TableIOFactory.create"></a>

#### create

```python
@staticmethod
def create(format_name: str,
           file_name: PathLike,
           file_access: FileAccess,
           args: OptionalArgs = None,
           implementation: Optional[str] = None,
           capabilities: Optional[Capabilities] = None) -> TableIO
```

Create an instance of a registered TableIO subclass.

**Arguments**:

- `format_name` - The name identifier of the format class to create.
- `file_name` - The file path to pass to the TableIO constructor.
- `file_access` - The file access to pass to the TableIO constructor.
- `args` - additional arguments to pass to the TableIO constructor.
- `implementation` - The implementation name to use. If not specified,
  the matching implementation with the highest
  priority is used.
- `capabilities` - The capabilities to match. If not specified,
  the implementation matching the format name (and
  if specified the implementation name) is used.
  If several implementations match, the
  implementation with the highest priority
  is used.

**Returns**:

  An instance of the requested TableIO subclass.
  Intended to be used as context manager, using a with statement.

**Raises**:

- `InsufficientCapabilities` - If capabilities contradict file_access.
- `TableIOFactoryNoSuchError` - If the format_name is not registered
  or the implementation name is not
  registered.
- `TableIOFactoryNoCapabilityMatch` - If the capabilities cannot be
  matched to any implementation.

<a id="tableio.factory.TableIOFactory.i_create"></a>

#### i\_create

```python
def i_create(format_name: str,
             file_name: PathLike,
             file_access: FileAccess,
             args: OptionalArgs = None,
             implementation: Optional[str] = None,
             capabilities: Optional[Capabilities] = None) -> TableIO
```

Internally create an instance of a registered subclass.

**Raises**:

- `InsufficientCapabilities` - If capabilities contradict file_access.
- `TableIOFactoryNoSuchError` - If the format_name is not registered
  or the implementation name is not
  registered.
- `TableIOFactoryNoCapabilityMatch` - If the capabilities cannot be
  matched to any implementation.

<a id="tableio.factory.TableIOFactory.filter_args"></a>

#### filter\_args

```python
@staticmethod
def filter_args(args: OptionalArgs, format_name: str,
                implementation: str) -> OptionalArgs
```

Filter the arguments for a registered format.

Filter the arguments to only include the arguments that are valid for
the given format name and implementation. This is useful when the args
dictionary includes arguments for several formats, and not all of
them are valid for the given format name and implementation.
(The risk of using this function is that a misspelled argument will
be silently ignored, and the programming error will not be detected.)

**Arguments**:

- `args` - The arguments to filter.
- `format_name` - The name identifier of the format class to filter the
  arguments for.
- `implementation` - The implementation name to use.

**Returns**:

  The filtered arguments.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name is not registered
  or the implementation name is not
  registered.

<a id="tableio.factory.TableIOFactory.i_filter_args"></a>

#### i\_filter\_args

```python
def i_filter_args(args: OptionalArgs, format_name: str,
                  implementation: str) -> OptionalArgs
```

Internally filter the arguments for a registered format.

<a id="tableio.factory.TableIOFactory.get_registered_formats"></a>

#### get\_registered\_formats

```python
@staticmethod
def get_registered_formats(lower: bool = False,
                           upper: bool = False,
                           capabilities: Optional[Capabilities] = None,
                           empty_is_ok: bool = False) -> list[str]
```

Get a list of all registered format names.

The list includes all registered format names optionally filtered
to only include formats that offer the requested capabilities.
Always includes the correct case for the format names in the returned
list. If lower or upper is True, also includes those cases of the
format names in the returned list. (Including lower case and upper
case variants is probably not a good idea when printing the list
for a human user, but it is useful when checking if a format name
is in the allowed list of format names.)

**Arguments**:

- `lower` - If True, also include the format name in lower case.
- `upper` - If True, also include the format name in upper case.
- `capabilities` - The capabilities to match. If not specified,
  all formats are included in the return value.
  If specified, only formats that offer the requested
  capabilities are included in the return value.
- `empty_is_ok` - If True, an empty list is returned if no
  formats match the capabilities.
  If False, a TableIOFactoryNoCapabilityMatch
  error is raised if no formats match the capabilities.

**Returns**:

  A list of registered format name strings optionally filtered
  to only include formats that offer the requested capabilities.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - If empty_is_ok is False and
  no formats match the
  capabilities.

<a id="tableio.factory.TableIOFactory.i_get_registered_formats"></a>

#### i\_get\_registered\_formats

```python
def i_get_registered_formats(lower: bool = False,
                             upper: bool = False,
                             capabilities: Optional[Capabilities] = None,
                             empty_is_ok: bool = False) -> list[str]
```

Internally get a list of registered format names.

<a id="tableio.factory.TableIOFactory.get_registered_implementations"></a>

#### get\_registered\_implementations

```python
@staticmethod
def get_registered_implementations(format_name: Optional[str] = None,
                                   lower: bool = False,
                                   upper: bool = False,
                                   capabilities: Optional[Capabilities] = None,
                                   empty_is_ok: bool = False) -> list[str]
```

Get a list of all registered implementation names.

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

**Arguments**:

- `format_name` - The name identifier of the format to get the
  implementation names for. If not specified, all
  implementations are included in the return value.
- `lower` - If True, also include the implementation name in lower case.
- `upper` - If True, also include the implementation name in upper case.
- `capabilities` - The capabilities to match. If not specified,
  all implementations are included in the return value.
- `empty_is_ok` - If True, an empty list is returned if no
  implementations match the capabilities.
  If False, a TableIOFactoryNoCapabilityMatch
  error is raised if no implementations match the
  capabilities.

**Returns**:

  A list of registered implementation name strings optionally
  filtered to only include implementations that offer the
  requested capabilities.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - If empty_is_ok is False and
  no implementations match the
  capabilities.

<a id="tableio.factory.TableIOFactory.i_get_registered_implementations"></a>

#### i\_get\_registered\_implementations

```python
def i_get_registered_implementations(
        format_name: Optional[str] = None,
        lower: bool = False,
        upper: bool = False,
        capabilities: Optional[Capabilities] = None,
        empty_is_ok: bool = False) -> list[str]
```

Internally get a list of registered implementation names.

<a id="tableio.factory.TableIOFactory.get_usage"></a>

#### get\_usage

```python
@staticmethod
def get_usage(format_name: str, implementation: str) -> Descriptor
```

Get the usage information for a registered format.

**Arguments**:

- `format_name` - The name identifier of the format class to get
  the usage information for.
- `implementation` - The implementation name to use.

**Returns**:

  The usage information for the requested format.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name is not registered
  or the implementation name is not
  registered.

<a id="tableio.factory.TableIOFactory.i_get_usage"></a>

#### i\_get\_usage

```python
def i_get_usage(format_name: str, implementation: str) -> Descriptor
```

Internally get the usage information for a registered format.

<a id="tableio.factory.create_tableio"></a>

#### create\_tableio

```python
def create_tableio(format_name: str,
                   file_name: PathLike,
                   file_access: FileAccess,
                   args: OptionalArgs = None,
                   implementation: Optional[str] = None,
                   capabilities: Optional[Capabilities] = None) -> TableIO
```

Create an instance of a registered TableIO subclass.

Intended to be used as context manager, using a with statement.
This is a shortcut for TableIOFactory.create().

**Arguments**:

- `format_name` - The name identifier of the format class to create.
- `file_name` - The file path to pass to the TableIO constructor.
- `file_access` - The file access to pass to the TableIO constructor.
- `args` - additional arguments to pass to the TableIO constructor.
- `implementation` - The implementation name to use. If not specified,
  the matching implementation with the highest
  priority is used.
- `capabilities` - The capabilities to match. If not specified,
  the implementation matching the format name (and
  if specified the implementation name) is used.
  If several implementations match, the implementation
  with the highest priority is used.

**Returns**:

  An instance of the requested TableIO subclass.

**Raises**:

- `InsufficientCapabilities` - If capabilities contradict file_access.
- `TableIOFactoryNoSuchError` - If the format_name or implementation
  name is not registered.
- `TableIOFactoryNoCapabilityMatch` - If the capabilities cannot be
  matched to any implementation.

<a id="tableio.factory.filter_args_tableio"></a>

#### filter\_args\_tableio

```python
def filter_args_tableio(args: OptionalArgs, format_name: str,
                        implementation: str) -> OptionalArgs
```

Filter the arguments for a registered format.

This is a shortcut for TableIOFactory.filter_args().
Filter the arguments to only include the arguments that are valid for
the given format name and implementation. This is useful when the args
dictionary includes arguments for several formats, and not all of them
are valid for the given format name and implementation. (The risk of
using this function is that a misspelled argument will be silently
ignored, and the programming error will not be detected.)

**Arguments**:

- `args` - The arguments to filter.
- `format_name` - The name identifier of the format class to filter
  the arguments for.
- `implementation` - The implementation name to use.

**Returns**:

  The filtered arguments.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name or implementation
  name is not registered.

<a id="tableio.factory.list_registered_tableio"></a>

#### list\_registered\_tableio

```python
def list_registered_tableio(lower: bool = False,
                            upper: bool = False,
                            capabilities: Optional[Capabilities] = None,
                            empty_is_ok: bool = False) -> list[str]
```

Get a list of all registered format names.

This is a shortcut for TableIOFactory.get_registered_formats().
Always includes the correct case for the format names in the returned
list. If lower or upper is True, also includes those cases of the
format names in the returned list. (Including lower case and upper
case variants is probably not a good idea when printing the list
for a human user, but it is useful when checking if a format name
is in the allowed list of format names.)

**Arguments**:

- `lower` - If True, also include the format name in lower case.
- `upper` - If True, also include the format name in upper case.
- `capabilities` - The capabilities to match. If not specified,
  all formats are included in the return value.
  If specified, only formats that offer the requested
  capabilities are included in the return value.
- `empty_is_ok` - If True, an empty list is returned if no
  formats match the capabilities.
  If False, a TableIOFactoryNoCapabilityMatch
  error is raised if no formats match the capabilities.

**Returns**:

  A list of registered format name strings.

<a id="tableio.factory.list_implementations_tableio"></a>

#### list\_implementations\_tableio

```python
def list_implementations_tableio(format_name: Optional[str] = None,
                                 lower: bool = False,
                                 upper: bool = False,
                                 capabilities: Optional[Capabilities] = None,
                                 empty_is_ok: bool = False) -> list[str]
```

Get a list of all registered implementation names.

This is a shortcut for TableIOFactory.get_registered_implementations().

**Arguments**:

- `format_name` - The name identifier of the format to get the
  implementation names for. If not specified, all
  implementations are included in the return value.
- `lower` - If True, also include the implementation name in lower case.
- `upper` - If True, also include the implementation name in upper case.
- `capabilities` - The capabilities to match. If not specified,
  all implementations are included in the return value.
  If specified, only implementations that offer the
  requested capabilities are included in the return value.
- `empty_is_ok` - If True, an empty list is returned if no
  implementations match the capabilities.
  If False, a TableIOFactoryNoCapabilityMatch
  error is raised if no implementations match the
  capabilities.

**Returns**:

  A list of registered implementation name strings optionally
  filtered to only include implementations that offer the
  requested capabilities.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - If empty_is_ok is False and
  no implementations match the
  capabilities.

<a id="tableio.factory.usage_tableio"></a>

#### usage\_tableio

```python
def usage_tableio(format_name: str, implementation: str) -> Descriptor
```

Get the usage information for a registered format.

This is a shortcut for TableIOFactory.get_usage().

**Arguments**:

- `format_name` - The name identifier of the format class to get the
  usage information for.
- `implementation` - The implementation name to use.

**Returns**:

  The usage information for the requested format.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name or implementation
  name is not registered.

<a id="tableio.factory.register_tableio"></a>

#### register\_tableio

```python
def register_tableio(format_class: type[TableIO]) -> None
```

Register a TableIO subclass with the factory.

This is a shortcut for TableIOFactory.register().

**Arguments**:

- `format_class` - The TableIO subclass to register.

**Raises**:

- `ValueError` - If the format_class is not a subclass of TableIO.
- `TableIOFactoryConflictError` - If the format_name or implementation
  name is already registered.

<a id="tableio.value_type"></a>

# tableio.value\_type

Value types for the tableio package.

<a id="tableio.value_type.Fmt"></a>

## Fmt Objects

```python
class Fmt(NamedTuple)
```

Format specification for value(s).

<a id="tableio.value_type.Fmt.bold"></a>

#### bold

If the value(s) should be bold.

<a id="tableio.value_type.Fmt.italic"></a>

#### italic

If the value(s) should be italic.

<a id="tableio.value_type.Fmt.highlight"></a>

#### highlight

The highlight color.

<a id="tableio.value_type.ValueFmt"></a>

## ValueFmt Objects

```python
class ValueFmt(NamedTuple)
```

Value with format specification.

<a id="tableio.value_type.ValueFmt.value"></a>

#### value

The value.

<a id="tableio.value_type.ValueFmt.fmt"></a>

#### fmt

The format specification.

<a id="tableio.value_type.FmtListRow"></a>

## FmtListRow Objects

```python
class FmtListRow(NamedTuple)
```

Formatted Listber row.

<a id="tableio.value_type.FmtListRow.values"></a>

#### values

The sequence of values in the row.

<a id="tableio.value_type.FmtListRow.fmt"></a>

#### fmt

The format specification for the row.

<a id="tableio.value_type.FmtDictRow"></a>

## FmtDictRow Objects

```python
class FmtDictRow(NamedTuple)
```

Formatted Dict row.

<a id="tableio.value_type.FmtDictRow.values"></a>

#### values

The mapping of value names to values in the row.

<a id="tableio.value_type.FmtDictRow.fmt"></a>

#### fmt

The format specification for the row.

<a id="tableio.value_type.ReadResult"></a>

## ReadResult Objects

```python
class ReadResult(NamedTuple, Generic[DataT])
```

Result of reading data from a file.

<a id="tableio.value_type.ReadResult.data"></a>

#### data

The data read from the table in the file.

<a id="tableio.value_type.ReadResult.headings"></a>

#### headings

The headings read from the file before the table with the data.

<a id="tableio.value_type.ReadResult.last_read_row"></a>

#### last\_read\_row

The index of the last row read from the file. 0-based.

<a id="tableio.value_type.fmt_set_in_both"></a>

#### fmt\_set\_in\_both

```python
def fmt_set_in_both(fmt1: Fmt, fmt2: Fmt) -> Fmt
```

Return the format attributes that are set the same in both formats.

Bold and italic remain enabled only when they are enabled in both input
formats. Highlight is preserved only when both input formats use the same
highlight color; otherwise the result uses Color.NONE.

**Arguments**:

- `fmt1` - The first argument format.
- `fmt2` - The second argument format.

**Returns**:

  The format that is set in both argument formats.

<a id="tableio.value_type.fmt_set_in_all"></a>

#### fmt\_set\_in\_all

```python
def fmt_set_in_all(fmts: Sequence[Fmt]) -> Fmt
```

Return a new format that is set in all argument formats.

Bold and italic remain enabled only when they are enabled in every input
format. Highlight is preserved only when every input format uses the same
highlight color; otherwise the result uses Color.NONE.

**Arguments**:

- `fmts` - The sequence of formats to merge.

**Returns**:

  The format that is set in all argument formats.

**Raises**:

- `ValueError` - If the sequence is empty.

<a id="tableio.value_type.get_plain_value"></a>

#### get\_plain\_value

```python
def get_plain_value(cell: CellT) -> Value
```

Return the plain value stored in a cell.

<a id="tableio.value_type.value_to_str"></a>

#### value\_to\_str

```python
def value_to_str(value: Value, none_is_empty: bool = False) -> str
```

Convert a plain value to its string representation.

**Arguments**:

- `value` - The value to convert.
- `none_is_empty` - If True, None values are converted to empty strings.
  If False, None values will raise ValueError.

**Raises**:

- `ValueError` - If none_is_empty is False and value is None.

**Returns**:

  The converted value.

<a id="tableio.value_type.list_row_to_str_list"></a>

#### list\_row\_to\_str\_list

```python
def list_row_to_str_list(row: ListRowSeq[CellT],
                         none_is_empty: bool = False) -> list[str]
```

Convert ListRow to list of str.

**Arguments**:

- `row` - The row to convert.
- `none_is_empty` - If True, None values are converted to empty strings.
  If False, None values will raise ValueError.

**Raises**:

- `ValueError` - If none_is_empty is False and a None value is found.

**Returns**:

  The converted row.

<a id="tableio.value_type.dict_row_to_str_dict"></a>

#### dict\_row\_to\_str\_dict

```python
def dict_row_to_str_dict(row: DictRowMap[CellT],
                         none_is_empty: bool = False) -> dict[str, str]
```

Convert DictRow to dict of str.

**Arguments**:

- `row` - The row to convert.
- `none_is_empty` - If True, None values are converted to empty strings.
  If False, None values will raise ValueError.

**Raises**:

- `ValueError` - If none_is_empty is False and a None value is found.

**Returns**:

  The converted row.

<a id="tableio.value_type.str_list_to_list_row"></a>

#### str\_list\_to\_list\_row

```python
def str_list_to_list_row(row: list[str]) -> ListRow[Value]
```

Convert list of str to ListRow.

<a id="tableio.value_type.get_checked_type"></a>

#### get\_checked\_type

```python
def get_checked_type(value: Optional[object], expected_type: type[T]) -> T
```

Return value unchanged while narrowing it to the expected type.

This helper is a non-raising cast for code that has already established
the runtime type by other means. The expected_type argument exists so
static type checkers can infer the target type.
Any runtime mismatch will raise an AssertionError as this will be
an internal programming error.

**Arguments**:

- `value` - The value to check. Must not be None.
- `expected_type` - The expected type.

**Returns**:

  The value unchanged, narrowed to the expected type.

<a id="tableio.value_type.has_format_list"></a>

#### has\_format\_list

```python
def has_format_list(data: ListDataSeq[CellT]) -> bool
```

Return whether any cell in the list data carries formatting.

<a id="tableio.value_type.is_plain_list_data"></a>

#### is\_plain\_list\_data

```python
def is_plain_list_data(
        data: ListDataSeq[CellT]) -> TypeGuard[ListDataSeq[Value]]
```

Return whether the list data contains plain values only.

<a id="tableio.value_type.strip_format_list"></a>

#### strip\_format\_list

```python
def strip_format_list(data: ListDataSeq[CellT]) -> ListDataSeq[Value]
```

Return list data with any cell formatting removed.

If the input already contains plain values only, the original data object
is returned unchanged. Formatted data is converted to a new list of lists
containing the plain values.

**Arguments**:

- `data` - The list data to convert.

**Returns**:

  The plain-value list data.

<a id="tableio.value_type.has_format_dict"></a>

#### has\_format\_dict

```python
def has_format_dict(data: DictDataMap[CellT]) -> bool
```

Return whether any cell in the dict data carries formatting.

<a id="tableio.value_type.is_plain_dict_data"></a>

#### is\_plain\_dict\_data

```python
def is_plain_dict_data(
        data: DictDataMap[CellT]) -> TypeGuard[DictDataMap[Value]]
```

Return whether the dict data contains plain values only.

<a id="tableio.value_type.strip_format_dict"></a>

#### strip\_format\_dict

```python
def strip_format_dict(data: DictDataMap[CellT]) -> DictDataMap[Value]
```

Return dict data with any cell formatting removed.

If the input already contains plain values only, the original data object
is returned unchanged. Formatted data is converted to a new list of dicts
containing the plain values.

**Arguments**:

- `data` - The dict data to convert.

**Returns**:

  The plain-value dict data.

<a id="tableio.value_type.row_strip_format_list"></a>

#### row\_strip\_format\_list

```python
def row_strip_format_list(data: FmtListData) -> ListDataSeq[Value]
```

Return list row data without the row format wrappers.

**Arguments**:

- `data` - The list data to strip.

**Returns**:

  A new outer list containing the original row value sequences.

<a id="tableio.value_type.row_strip_format_dict"></a>

#### row\_strip\_format\_dict

```python
def row_strip_format_dict(data: FmtDictData) -> DictDataMap[Value]
```

Return dict row data without the row format wrappers.

**Arguments**:

- `data` - The dict data to strip.

**Returns**:

  A new outer list containing the original row value mappings.

<a id="tableio.value_type.row_format_each_cell_list"></a>

#### row\_format\_each\_cell\_list

```python
def row_format_each_cell_list(data: FmtListData) -> ListData[ValueFmt]
```

Format each cell individually with the format of the row.

For each each row in the input data use the format of the row to format
the value of each cell in the row. Return the formatted data as a list of
lists of ValueFmt.

**Arguments**:

- `data` - The list data to format.

**Returns**:

  The formatted list data.

<a id="tableio.value_type.row_format_each_cell_dict"></a>

#### row\_format\_each\_cell\_dict

```python
def row_format_each_cell_dict(data: FmtDictData) -> DictData[ValueFmt]
```

Format each cell individually with the format of the row.

For each each row in the input data use the format of the row to format
the value of each cell in the row. Return the formatted data as a list of
dicts of ValueFmt.

**Arguments**:

- `data` - The dict data to format.

**Returns**:

  The formatted dict data.

<a id="tableio.value_type.format_each_cell_list"></a>

#### format\_each\_cell\_list

```python
def format_each_cell_list(
    data: ListDataSeq[Value], fmt: Fmt = Fmt()) -> ListData[ValueFmt]
```

Format each cell in the list data with the specified format.

**Arguments**:

- `data` - The list data to format.
- `fmt` - The format to apply to the cells.

**Returns**:

  The formatted list data.

<a id="tableio.value_type.format_each_cell_dict"></a>

#### format\_each\_cell\_dict

```python
def format_each_cell_dict(
    data: DictDataMap[Value], fmt: Fmt = Fmt()) -> DictData[ValueFmt]
```

Format each cell in the dict data with the specified format.

**Arguments**:

- `data` - The dict data to format.
- `fmt` - The format to apply to the cells.

**Returns**:

  The formatted dict data.

<a id="tableio.value_type.row_fmt_from_cell_fmt_list"></a>

#### row\_fmt\_from\_cell\_fmt\_list

```python
def row_fmt_from_cell_fmt_list(data: ListDataSeq[CellT]) -> FmtListData
```

Create a list of formatted rows from list data.

Each row gets a format that is the merge of the formats of all
its cells: a formatting attribute is applied to the row only
if that attribute is set in every cell. Plain value cells are
treated as having the default format Fmt().

**Arguments**:

- `data` - List data with plain values or ValueFmt cells.

**Returns**:

  A list of formatted rows.

**Raises**:

- `ValueError` - If any row is empty.

<a id="tableio.value_type.row_fmt_from_cell_fmt_dict"></a>

#### row\_fmt\_from\_cell\_fmt\_dict

```python
def row_fmt_from_cell_fmt_dict(data: DictDataMap[CellT]) -> FmtDictData
```

Create formatted dict rows from dict data.

Each row gets a format that is the merge of the formats of all
its cells: a formatting attribute is applied to the row only
if that attribute is set in every cell. Plain value cells are
treated as having the default format Fmt().

**Arguments**:

- `data` - Dict data with plain values or ValueFmt cells.

**Returns**:

  A list of formatted dict rows.

**Raises**:

- `ValueError` - If any row is empty.

<a id="tableio.value_type.MissingDataForColumn"></a>

## MissingDataForColumn Objects

```python
class MissingDataForColumn(ValueError)
```

Exception for when data is missing for a needed key (column name).

<a id="tableio.value_type.MissingDataForColumn.__init__"></a>

#### \_\_init\_\_

```python
def __init__(key: str)
```

Initialize the exception.

<a id="tableio.value_type.DataForExtraColumn"></a>

## DataForExtraColumn Objects

```python
class DataForExtraColumn(ValueError)
```

Exception for when data is present for key not in the column_order.

<a id="tableio.value_type.DataForExtraColumn.__init__"></a>

#### \_\_init\_\_

```python
def __init__(key: str)
```

Initialize the exception.

<a id="tableio.value_type.normalize_dict_data"></a>

#### normalize\_dict\_data

```python
def normalize_dict_data(data: DictDataMap[CellT],
                        column_order: list[str],
                        missing_ok: bool = False,
                        extra_ok: bool = False) -> DictDataMap[CellT]
```

Check and normalize a dict data to have specified columns.

The column_order must not be empty.
Empty rows are not allowed.
If all columns in column_order are present as keys in every row,
and no other keys are present, the original data is returned unchanged.
If missing_ok is False and data is missing for a column in the
column_order then an exception is raised.
If extra_ok is False and data is present for a key not in the
column_order, an exception is raised.
The data is normalized by adding None values for missing columns if
missing_ok is True. For formatted data, missing cells are added as
ValueFmt(value=None, fmt=Fmt()).
The data is normalized by removing extra columns if extra_ok is True.
When normalizing the data, the order of the rows is preserved.
When data is added of removed, the modification are done on a copy of the
data and the original data object in argument list is not modified.

**Arguments**:

- `data` - The dict data to normalize.
- `column_order` - The order of the columns, that will be present in the
  keys of the normalized data. Must not be empty.
- `missing_ok` - If True, missing data for a column in the column_order
  is OK, and None is added for the key (column name) in the
  row.
  If False, an exception is raised if data is missing for a
  key (column name) in the column_order in any row.
- `extra_ok` - If True, data for a key (column name) not in the column_order
  is OK, and the key (column name) is removed from the row.
  If False, an exception is raised if data is present for a
  key (column name) not in the column_order in any row.

**Raises**:

- `ValueError` - If column_order is empty, contains duplicate column
  names, or if any row is empty.
- `MissingDataForColumn` - If missing_ok is False and data is missing for a
  key (column name) in the column_order in any row.
- `DataForExtraColumn` - If extra_ok is False and data is present for a
  key (column name) not in the column_order in any
  row.
- `TypeError` - If plain and formatted cells are mixed in the same input.

**Returns**:

  The normalized data that may be the same object as the input data.

<a id="tableio._archive_rewrite"></a>

# tableio.\_archive\_rewrite

Helpers for rewriting spreadsheet ZIP archives safely.

Spreadsheet writers first save library output to a temporary archive.
These helpers then build a rewritten copy in a second temporary archive
and replace the first archive only after both ZIP files are closed.

<a id="tableio._archive_rewrite.temporary_output_path"></a>

#### temporary\_output\_path

```python
def temporary_output_path(source_path: Path, suffix: str) -> Path
```

Return one missing temporary path next to ``source_path``.

The temporary file is created in the same directory as
``source_path`` so a later ``Path.replace()`` stays on the same
filesystem. The file name uses ``suffix`` and the returned path does
not exist when this function returns.

<a id="tableio._archive_rewrite.rewrite_zip_archive"></a>

#### rewrite\_zip\_archive

```python
def rewrite_zip_archive(
        archive_path: Path,
        rewrite_entry: Callable[[ZipInfo, bytes], Optional[bytes]],
        extra_entries: Optional[dict[str, bytes]] = None) -> None
```

Rewrite one ZIP archive by copying it into a new archive.

The original archive at ``archive_path`` is read entry by entry and
a rewritten archive is written to a sibling temporary file. The
callback receives each original ``ZipInfo`` together with its bytes.
Returning ``None`` drops the entry. Any mapping passed in
``extra_entries`` is appended after copied entries, except for names
that were already written.

The original archive is replaced only after both ZIP files have been
closed. This avoids replacing an archive while it is still open,
which is a safer pattern on Windows as well as on Unix-like systems.

**Arguments**:

- `archive_path` - Path to the archive to rewrite in place.
- `rewrite_entry` - Callback invoked once for each original ZIP entry.
  The callback receives the original ``ZipInfo`` together with
  the entry bytes. It returns replacement bytes for the output
  archive, or ``None`` to drop the entry completely.
- `extra_entries` - Optional mapping of extra archive members to add
  after copying rewritten entries. Names that were already
  written are left unchanged.

<a id="tableio.valueconversion"></a>

# tableio.valueconversion

Helpers for converting one stored ``Value`` to an expected type.

When a ``Value`` is stored in a file format with weaker typing, the original
type may be lost. A ``datetime`` written to CSV, for example, is usually read
back as a string. These helpers perform explicit and predictable conversions
from one public ``Value`` representation to another expected concrete type.

<a id="tableio.valueconversion.UnreasonableTypeConversion"></a>

## UnreasonableTypeConversion Objects

```python
class UnreasonableTypeConversion(TypeError)
```

Exception for when a value's conversion types are unreasonable.

<a id="tableio.valueconversion.UnreasonableTypeConversion.__init__"></a>

#### \_\_init\_\_

```python
def __init__(value: Value, expected_type: type[object])
```

Initialize the exception.

<a id="tableio.valueconversion.UnreasonableValueConversion"></a>

## UnreasonableValueConversion Objects

```python
class UnreasonableValueConversion(ValueError)
```

Exception for when a value's conversion values are unreasonable.

<a id="tableio.valueconversion.UnreasonableValueConversion.__init__"></a>

#### \_\_init\_\_

```python
def __init__(value: Value, expected_type: type[object])
```

Initialize the exception.

<a id="tableio.valueconversion.value2str"></a>

#### value2str

```python
def value2str(value: Value, none_is_empty: bool = False) -> str
```

Convert a value to a string.

Datetime values are converted with ``isoformat()`` so the result remains
easy to parse back to a datetime when needed.

**Arguments**:

- `value` - The value to convert.
- `none_is_empty` - If True, None values are converted to empty strings.
  If False, None values raise
  UnreasonableValueConversion.

**Raises**:

- `UnreasonableValueConversion` - If none_is_empty is False and value is
  None.

**Returns**:

  The converted value.

<a id="tableio.valueconversion.value2bool"></a>

#### value2bool

```python
def value2bool(value: Value, none_is_false: bool = False) -> bool
```

Convert a value to a boolean.

Strings are accepted only when they match one of the documented boolean
spellings, case-insensitively and with surrounding whitespace ignored.
Integer values are accepted only when they are exactly 0 or 1.

**Arguments**:

- `value` - The value to convert.
- `none_is_false` - If True, None values are converted to False.
  If False, None values raise UnreasonableValueConversion.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to bool.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent a boolean.

**Returns**:

  The converted boolean value.

<a id="tableio.valueconversion.value2int"></a>

#### value2int

```python
def value2int(value: Value,
              none_is_zero: bool = False,
              format_string: Optional[str] = None) -> int
```

Convert a value to an integer.

Strings are parsed with ``int()``. When ``format_string`` is provided, the
parsed integer must reproduce the original string with ``format()``. This
keeps parsing deterministic while supporting common integer formats such as
zero-padded decimal strings.

**Arguments**:

- `value` - The value to convert.
- `none_is_zero` - If True, None values are converted to 0.
  If False, None values raise
  UnreasonableValueConversion.
- `format_string` - Optional Python integer format specification used to
  validate string input after parsing.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to int.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent an integer.

**Returns**:

  The converted integer value.

<a id="tableio.valueconversion.value2float"></a>

#### value2float

```python
def value2float(value: Value, none_is_zero: bool = False) -> float
```

Convert a value to a float.

**Arguments**:

- `value` - The value to convert.
- `none_is_zero` - If True, None values are converted to 0.0.
  If False, None values raise
  UnreasonableValueConversion.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to float.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent a float.

**Returns**:

  The converted float value.

<a id="tableio.valueconversion.value2datetime"></a>

#### value2datetime

```python
def value2datetime(value: Value,
                   format_string: Optional[str] = None) -> datetime
```

Convert a value to a datetime.

Without ``format_string``, string input must use one of the formats
accepted by ``datetime.fromisoformat()``. With ``format_string``, parsing
is delegated to ``datetime.strptime()``.

**Arguments**:

- `value` - The value to convert.
- `format_string` - Optional ``strptime`` format for string input.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to datetime.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent a datetime.

**Returns**:

  The converted datetime value.

<a id="tableio.valueconversion.value2date"></a>

#### value2date

```python
def value2date(value: Value, format_string: Optional[str] = None) -> date
```

Convert a value to a date.

Datetime values are reduced to their calendar date. Without
``format_string``, string input is parsed first as an ISO date and then as
an ISO datetime if needed. With ``format_string``, parsing is delegated to
``datetime.strptime()`` and the date part is returned.

**Arguments**:

- `value` - The value to convert.
- `format_string` - Optional ``strptime`` format for string input.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to date.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent a date.

**Returns**:

  The converted date value.

<a id="tableio.valueconversion.value2time"></a>

#### value2time

```python
def value2time(value: Value, format_string: Optional[str] = None) -> time
```

Convert a value to a time.

Datetime values are reduced to their time-of-day. Without
``format_string``, string input is parsed first as an ISO time and then as
an ISO datetime if needed. With ``format_string``, parsing is delegated to
``datetime.strptime()`` and the time part is returned.

**Arguments**:

- `value` - The value to convert.
- `format_string` - Optional ``strptime`` format for string input.

**Raises**:

- `UnreasonableTypeConversion` - If the source type cannot reasonably be
  converted to time.
- `UnreasonableValueConversion` - If the source value is of a reasonable
  type but does not represent a time.

**Returns**:

  The converted time value.

<a id="tableio.valueconversion.value2none"></a>

#### value2none

```python
def value2none(value: Value) -> None
```

Convert a value to None.

**Arguments**:

- `value` - The value to convert.

**Returns**:

  The converted value.

<a id="tableio.valueconversion.value2type"></a>

#### value2type

```python
def value2type(value: Value,
               to_type: type[T],
               accept_none: bool = False,
               datetime_format_string: Optional[str] = None,
               int_format_string: Optional[str] = None) -> T
```

Convert a value to a type.

This is a convenience function that calls the appropriate value conversion
function based on the type.

**Arguments**:

- `value` - The value to convert.
- `to_type` - The type to convert to. Can be NoneType, datetime, int, str,
  bool, or float.
- `accept_none` - If True, None values are accepted.
- `datetime_format_string` - Optional ``strptime`` format for string input.
- `int_format_string` - Optional Python integer format specification used to
  validate string input after parsing.

**Returns**:

  The converted value.

<a id="tableio.valueconversion.value2type_of"></a>

#### value2type\_of

```python
def value2type_of(value: Value,
                  to_type_of: T,
                  accept_none: bool = False,
                  datetime_format_string: Optional[str] = None,
                  int_format_string: Optional[str] = None) -> T
```

Convert a value to a type of the given variable.

This is a convenience function that calls the appropriate value conversion
function based on the type.

**Arguments**:

- `value` - The value to convert.
- `to_type_of` - The a variable of the type to convert to. The value of
  this variable will not be used, only its type. Can be of
  type NoneType, datetime, int, str, bool, or float.
- `accept_none` - If True, None values are accepted.
- `datetime_format_string` - Optional ``strptime`` format for string input.
- `int_format_string` - Optional Python integer format specification used to
  validate string input after parsing.

**Returns**:

  The converted value.

<a id="tableio.tableio_types"></a>

# tableio.tableio\_types

Shared public types used by the tableio package.

<a id="tableio.tableio_types.Descriptor"></a>

## Descriptor Objects

```python
class Descriptor(NamedTuple)
```

Metadata describing one TableIO implementation.

<a id="tableio.tableio_types.Descriptor.format_name"></a>

#### format\_name

The name of the file format.

<a id="tableio.tableio_types.Descriptor.implementation"></a>

#### implementation

The implementation name for the file format.

<a id="tableio.tableio_types.Descriptor.capabilities"></a>

#### capabilities

The capabilities of the reader/writer class.

<a id="tableio.tableio_types.Descriptor.mandatory_args"></a>

#### mandatory\_args

Mandatory constructor arguments besides file name and access.

<a id="tableio.tableio_types.Descriptor.optional_args"></a>

#### optional\_args

Optional constructor arguments.

<a id="tableio.tableio_types.Descriptor.priority"></a>

#### priority

The implementation priority. Higher means more preferred.

<a id="tableio.tableio_types.Box"></a>

## Box Objects

```python
class Box(NamedTuple)
```

A rectangular area in a sheet or file.

<a id="tableio.tableio_types.Position"></a>

## Position Objects

```python
class Position(NamedTuple)
```

A zero-based row and column position in one sheet.

<a id="tableio.tableio_types.FileAccess"></a>

## FileAccess Objects

```python
class FileAccess(IntEnum)
```

What access is requested to a file.

<a id="tableio.tableio_types.FileAccess.READ"></a>

#### READ

The file must exist and is opened for reading.

<a id="tableio.tableio_types.FileAccess.CREATE"></a>

#### CREATE

The file is created and opened for writing and reading.

<a id="tableio.tableio_types.FileAccess.UPDATE"></a>

#### UPDATE

The file must exist and is opened for reading and writing.

<a id="tableio.capability"></a>

# tableio.capability

Capabilities of the reader/writer class for a file format.

<a id="tableio.capability.Strictness"></a>

## Strictness Objects

```python
class Strictness(IntEnum)
```

Strictness of a capability.

<a id="tableio.capability.Strictness.STRICT"></a>

#### STRICT

Strictly enforce, raise if not supported.

<a id="tableio.capability.Strictness.IGNORE"></a>

#### IGNORE

Ignored if not supported.

<a id="tableio.capability.SingleCapability"></a>

## SingleCapability Objects

```python
class SingleCapability(NamedTuple)
```

Single capability of aspect of reader/writer class.

Describes if a reader/writer class for a file format can handle a
specific aspect when reading or writing a file.

A reader/writer class will provide information about its capabilities in a
Capabilities object. For the single capability this says if it is
supported, but also how the class behaves if it is requested and not
supported.
If supported is True, the strictness is not used.
If supported is False, and the strictness is STRICT, an exception is raised
when a call to the reader/writer class is made that requires the
capability.
If supported is False, and the strictness is IGNORE, the call is ignored.

When requesting reader/writer class from the factory, the requester can
specify that only reader/writer classes that support the requested
capabilities are returned.
If the requester sets supported to True for a capability, it means that
the requester will be making calls to the reader/writer class that requires
the capability.
If the requester sets supported to False for a capability, it means that
the requester will not be making calls to the reader/writer class that
requires the capability. (If the requester sets supported to false, the
strictness will not be used.)
If the requester sets supported to True and strictness to STRICT, it means
that the requester is only accepting reader/writer classes that support
the capability.
If the requester sets supported to True and strictness to IGNORE, it means
that the requester is accepting reader/writer classes that may ignore
calls using the capability.

<a id="tableio.capability.SingleCapability.supported"></a>

#### supported

If the capability is supported.

<a id="tableio.capability.SingleCapability.strictness"></a>

#### strictness

How the capability is handled if not supported. Default is to ignore.

<a id="tableio.capability.Capabilities"></a>

## Capabilities Objects

```python
class Capabilities(NamedTuple)
```

Capabilities of a reader/writer class for a file format.

<a id="tableio.capability.Capabilities.can_write"></a>

#### can\_write

The reader/writer class can write to the file format.

<a id="tableio.capability.Capabilities.can_read"></a>

#### can\_read

The reader/writer class can read from the file format.

<a id="tableio.capability.Capabilities.can_fmt_row"></a>

#### can\_fmt\_row

The writer class can apply a format to a row.

<a id="tableio.capability.Capabilities.can_fmt_value"></a>

#### can\_fmt\_value

The writer class can apply a format to a value.

<a id="tableio.capability.Capabilities.filtered_data_range"></a>

#### filtered\_data\_range

The writer class can mark a table as a filterable data range.

<a id="tableio.capability.Capabilities.can_write_box"></a>

#### can\_write\_box

The writer class can write to position given by a box.

<a id="tableio.capability.Capabilities.can_read_box"></a>

#### can\_read\_box

The reader class can read from position given by a box.

<a id="tableio.capability.Capabilities.can_write_highlight"></a>

#### can\_write\_highlight

The writer class can write highlight according to format.

<a id="tableio.capability.Capabilities.multi_sheet"></a>

#### multi\_sheet

The reader/writer class can read from or write to multiple sheets.

<a id="tableio.capability.Capabilities.can_find_value_position"></a>

#### can\_find\_value\_position

The reader/writer class can find the position of a value.

<a id="tableio.capability.single_capability_match"></a>

#### single\_capability\_match

```python
def single_capability_match(offered: SingleCapability,
                            will_use: SingleCapability,
                            ignore_allowed: bool = True) -> bool
```

Check if the offered single capability matches the will use.

**Arguments**:

- `offered` - The offered single capability. Does the reader/writer
  class support this capability?
- `will_use` - The will use single capability. Does the requester intend to
  use this capability?
- `ignore_allowed` - If False: when the offered single capability would
  ignore the will use single capability it is
  considered a mismatch, and will return False.
  If True: when the offered single capability would
  ignore the will use single capability it is
  considered a match, and will return True.

**Returns**:

  True if the offered single capability matches the will use,
  False otherwise.

<a id="tableio.capability.capability_match"></a>

#### capability\_match

```python
def capability_match(offered: Capabilities,
                     will_use: Capabilities,
                     ignore_allowed: bool = False) -> bool
```

Check if the offered capabilities match the required capabilities.

**Arguments**:

- `offered` - The offered capabilities. What capabilities does the
  reader/writer class support?
- `will_use` - The recuested capabilities. What capabilities
  does the requester intend to use?
- `ignore_allowed` - If False: when an offered capability would ignore a
  will use capability it is considered a mismatch, and
  considered a mismatch, and will return False.
  If True: when an offered capability would ignore a
  will use capability it is considered a match, and
  will return True.

**Returns**:

  True if the offered capabilities match the will_use capabilities,
  False otherwise.

<a id="tableio.capability.CapabilityNotSupported"></a>

## CapabilityNotSupported Objects

```python
class CapabilityNotSupported(ValueError)
```

Exception raised when a capability is not supported.

<a id="tableio.capability.CapabilityNotSupported.__init__"></a>

#### \_\_init\_\_

```python
def __init__(action: str)
```

Initialize the exception.

**Arguments**:

- `action` - The requested action that is not supported.

<a id="tableio.capability.capability_to_str"></a>

#### capability\_to\_str

```python
def capability_to_str(capability: SingleCapability) -> str
```

Convert a single capability to a string.

**Arguments**:

- `capability` - The single capability to convert.

**Returns**:

  A string representation of the single capability.

<a id="tableio.capability.CAP_NOT_USED"></a>

#### CAP\_NOT\_USED

A capability that is not used.

The requester promises to not use this capability, so it does not
matter if the implementation supports it or not.

<a id="tableio.capability.CAP_NEEDED"></a>

#### CAP\_NEEDED

A capability that is used and must be supported.

In the selection of reader/writer class it is a must that the selected
class supports this capability. If no matching reader/writer class is
found to fulfill the request, an exception is raised.

<a id="tableio.capability.CAP_IGNORABLE"></a>

#### CAP\_IGNORABLE

A capability that can be ignored if not supported.

An example might be that prefer to be able to write a value in bold,
but the request can accept that the implementation ignores the bold
formatting.

<a id="tableio.capability.CAP_IMPLEMENTED"></a>

#### CAP\_IMPLEMENTED

A capability that is fully implemented and supported.

<a id="tableio.capability.CAP_IGNORED"></a>

#### CAP\_IGNORED

A capability that is not supported and will be ignored if requested.

The implementation cannot fulfill the request, but it makes sense to
ignore this feature and continue anyway. A typical example would be
a request to format a written value in bold. Here ignoring the bold
formatting makes sense as there is still a value written to the file.

<a id="tableio.capability.CAP_UNSUPPORTED"></a>

#### CAP\_UNSUPPORTED

A capability that is not supported and will raise an exception if requested.

This is a for a feature that cannot be supported but it would not make
sense to ignore. A typical example would be a request to write
a value in a specific location in the file. Writing the value to a
different location would not make sense. Thus the only sensible thing
to do is to raise an exception.

<a id="tableio.tableio_excel_xlsxwriter"></a>

# tableio.tableio\_excel\_xlsxwriter

TableIO writer class for Excel files using XlsxWriter.

<a id="tableio.tableio_excel_xlsxwriter._WorksheetLike"></a>

## \_WorksheetLike Objects

```python
class _WorksheetLike(Protocol)
```

Protocol for the subset of Worksheet methods used here.

<a id="tableio.tableio_excel_xlsxwriter._WorksheetLike.add_table"></a>

#### add\_table

```python
def add_table(*args: object, **kwargs: object) -> int
```

Add one table to the worksheet.

<a id="tableio.tableio_excel_xlsxwriter._WorksheetLike.set_column"></a>

#### set\_column

```python
def set_column(*args: object, **kwargs: object) -> object
```

Set one worksheet column width.

<a id="tableio.tableio_excel_xlsxwriter._WorksheetLike.write"></a>

#### write

```python
def write(row: int, col: int, *args: object) -> object
```

Write one cell value.

<a id="tableio.tableio_excel_xlsxwriter._WorksheetLike.write_blank"></a>

#### write\_blank

```python
def write_blank(row: int,
                col: int,
                blank: object,
                cell_format: Optional[object] = None) -> object
```

Write one blank cell.

<a id="tableio.tableio_excel_xlsxwriter._WorkbookLike"></a>

## \_WorkbookLike Objects

```python
class _WorkbookLike(Protocol)
```

Protocol for the subset of Workbook methods used here.

<a id="tableio.tableio_excel_xlsxwriter._WorkbookLike.add_worksheet"></a>

#### add\_worksheet

```python
def add_worksheet(name: Optional[str] = None) -> _WorksheetLike
```

Add one worksheet to the workbook.

<a id="tableio.tableio_excel_xlsxwriter._WorkbookLike.add_format"></a>

#### add\_format

```python
def add_format(properties: Optional[dict[str, object]] = None) -> object
```

Create one format in the workbook.

<a id="tableio.tableio_excel_xlsxwriter._WorkbookLike.close"></a>

#### close

```python
def close() -> None
```

Close the workbook and write it to disk.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter"></a>

## TableIOExcelXlsxWriter Objects

```python
class TableIOExcelXlsxWriter(TableIOExcelBased)
```

TableIO writer class for Excel files using XlsxWriter.

XlsxWriter is a creation-only backend. It can create `.xlsx` files with
multiple sheets, formatting, filtered table ranges and boxed writes, but
it cannot read or modify an existing workbook. This implementation keeps
an in-memory sheet model so the shared spreadsheet writing logic can still
manage cursor positions, boxed overwrites and filtered-range metadata
during one open CREATE session.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
        file_name: PathLike,
        file_access: FileAccess,
        file_exists_callback: Optional[Callable[[str], None]] = None) -> None
```

Initialize the XlsxWriter-backed Excel writer.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the capabilities for the XlsxWriter Excel backend.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Return the descriptor for the XlsxWriter Excel backend.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.open"></a>

#### open

```python
def open() -> None
```

Open one workbook for CREATE access.

<a id="tableio.tableio_csv"></a>

# tableio.tableio\_csv

Reader/writer for CSV files.

<a id="tableio.tableio_csv.CsvDefinitions"></a>

## CsvDefinitions Objects

```python
class CsvDefinitions(NamedTuple)
```

Definitions of the CSV file format.

<a id="tableio.tableio_csv.CsvDefinitions.type"></a>

#### type

The type of CSV file to write.

<a id="tableio.tableio_csv.CsvDefinitions.delimiter"></a>

#### delimiter

The delimiter to use for CSV files.

<a id="tableio.tableio_csv.CsvDefinitions.quoting"></a>

#### quoting

The quoting style to use for CSV files.

Allowed values (case-insensitive): 'all', 'minimal',
'nonnumeric', 'none', 'strings', 'notnull'.

<a id="tableio.tableio_csv.CsvDefinitions.quotechar"></a>

#### quotechar

The quote character to use for CSV files.

<a id="tableio.tableio_csv.CsvDefinitions.lineterminator"></a>

#### lineterminator

The line terminator to use for CSV files.

<a id="tableio.tableio_csv.CsvDefinitions.escapechar"></a>

#### escapechar

The escape character to use for CSV files.

<a id="tableio.tableio_csv.TableIOCsv"></a>

## TableIOCsv Objects

```python
class TableIOCsv(TableIOTextBased)
```

Reader/writer for CSV files.

This is a TableIO reader/writer class for Comma Separated Value (CSV)
files.
A strict CSV file format includes only one table of data in a file.
This means that on each row there is a list of values, that are usually
read into a list of lists, or into a list of dicts using the values on
the first line as the keys.
This class adds extensions to the CSV format to support several tables in
a file (separated by empty lines), and optional headings (lines starting
with #) before each table.
Notice: For best compatibility with other software use the strict CSV
format by only writing a single table in a file and not using headings.

<a id="tableio.tableio_csv.TableIOCsv.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             character_encoding: str = 'utf-8',
             csv_dialect: CsvDialect = CsvDialect.UNIX,
             csv_delimiter: Optional[str] = None,
             csv_quoting: Optional[str] = None,
             csv_quotechar: Optional[str] = None,
             csv_lineterminator: Optional[str] = None,
             csv_escapechar: Optional[str] = None)
```

Initialize the TableIOCsv reader/writer class.

<a id="tableio.tableio_csv.TableIOCsv.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Return the file name extension for CSV files.

<a id="tableio.tableio_csv.TableIOCsv.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOCsv reader/writer class.

<a id="tableio.tableio_csv.TableIOCsv.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the capabilities of the TableIOCsv reader/writer class.

<a id="tableio.tableio_spreadsheetbased"></a>

# tableio.tableio\_spreadsheetbased

Intermediate base class for spreadsheet-based file formats.

<a id="tableio.tableio_spreadsheetbased.excel_column_name"></a>

#### excel\_column\_name

```python
def excel_column_name(column: int) -> str
```

Return the Excel-style A1 column name for one zero-based column.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased"></a>

## TableIOSpreadsheetBased Objects

```python
class TableIOSpreadsheetBased(TableIO)
```

Intermediate TableIO base class for spreadsheet-based file formats.

This class holds the public spreadsheet semantics shared between Excel
and ODS backends: sequential reads, boxed reads and writes, headings,
filtered ranges, and the conversion between list or dict tables and the
rectangular grid stored in the document.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the spreadsheet-based TableIO class.

<a id="tableio.tableio_mformatbased"></a>

# tableio.tableio\_mformatbased

TableIO reader/writer class for a file format based on mformat.

<a id="tableio.tableio_mformatbased.TableIOMformatBased"></a>

## TableIOMformatBased Objects

```python
class TableIOMformatBased(TableIO)
```

TableIO reader/writer class for a file format based on mformat.

This is intermediate base for reader/writer classes based on mformat.
It provides the common functionality for reader/writer classes based on
different concrete mformat classes for output in different formats.
The functionality common to all TableIO_mformatbased subclasses is
collected here.

The mformat class does not support reading, so reading is not supported
for this class. Writing is supported, but not all features are supported.
For example, box and filtered data range are not supported.
Row formatting is supported, but value formatting is not.

Returned position is not reliable, as different MultiFormat derived
classes have different behavior. Returned position is not useful, as
neither reading nor boxed writing is supported, it is returned only
to satisfy the type hints of the TableIO class.

<a id="tableio.tableio_mformatbased.TableIOMformatBased.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the TableIOMformatBased reader/writer class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if
  the file already exists when file_access
  is CREATE.
  Return to allow the file to be overwritten.
  Raise an exception to prevent the file from
  being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="tableio.tableio_mformatbased.TableIOMformatBased.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the capabilities of the reader/writer class.

<a id="tableio.tableio_mformatbased.TableIOMformatBased.get_row_format_capability"></a>

#### get\_row\_format\_capability

```python
@classmethod
def get_row_format_capability(cls) -> SingleCapability
```

Return the capability for row formatting.

<a id="tableio.tableio_mformatbased.TableIOMformatBased.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Open the file. Avoid calling this method directly,
use the context manager instead.

<a id="tableio.tableio_excelbased"></a>

# tableio.tableio\_excelbased

Intermediate base class for Excel-based file formats.

<a id="tableio.tableio_excelbased.TableIOExcelBased"></a>

## TableIOExcelBased Objects

```python
class TableIOExcelBased(TableIOSpreadsheetBased)
```

Intermediate TableIO base class for Excel-based file formats.

This class is used to provide a base class for Excel-based
file formats. It is not intended to be used directly, but rather
to be subclassed by a specific Excel-based file format
such as Excel or Open Document Spreadsheet.

The main purpose of this class is to provide a place where common
functionality for Excel-based file formats can be implemented.
This class starts out empty, but whenever common functionality
is detected it should be refactored into this class.

<a id="tableio.tableio_excelbased.TableIOExcelBased.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the TableIO_SpreadsheetBased class.

**Arguments**:

- `file_name` - The name of the file to open.
- `file_access` - What access is requested to the file.
- `file_exists_callback` - A callback function to call if the file
  already exists when file_access is CREATE.
  Return to allow the file to be overwritten.
  Raise an exception to prevent the file from
  being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="tableio.tableio_excelbased.TableIOExcelBased.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Return the standard file name extension for Excel files.

<a id="tableio.reg_pkg_formats"></a>

# tableio.reg\_pkg\_formats

Formats defined in the package for registration with the factory.

The function in this module returns a list of TableIO subclasses
defined in this package. The returned classes are registered with
the factory during the factory's initialization.

<a id="tableio.reg_pkg_formats.register_formats_in_pkg"></a>

#### register\_formats\_in\_pkg

```python
def register_formats_in_pkg() -> list[type[TableIO]]
```

Get formats defined in the package to register with the factory.

<a id="tableio.tableio_excel_openpyxl"></a>

# tableio.tableio\_excel\_openpyxl

TableIO reader/writer class for Excel files using OpenPyXL.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL"></a>

## TableIOExcelOpenPyXL Objects

```python
class TableIOExcelOpenPyXL(TableIOExcelBased)
```

TableIO reader/writer class for Excel files using OpenPyXL.

The implementation operates on one current worksheet at a time. In
UPDATE mode the default write position is after the last used row in
the selected worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: PathLike,
             file_access: FileAccess,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the TableIOExcelOpenPyXL class.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_capabilities"></a>

#### get\_capabilities

```python
@classmethod
def get_capabilities(cls) -> Capabilities
```

Return the standard spreadsheet backend capabilities.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_description"></a>

#### get\_description

```python
@classmethod
def get_description(cls) -> Descriptor
```

Get the description of the TableIOExcelOpenPyXL class.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.open"></a>

#### open

```python
def open() -> None
```

Open the Excel workbook.

