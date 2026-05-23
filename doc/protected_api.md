# Table of Contents

* [tableio.config\_data\_apply](#tableio.config_data_apply)
  * [\_config\_error](#tableio.config_data_apply._config_error)
  * [\_check\_default\_input](#tableio.config_data_apply._check_default_input)
  * [\_registered\_formats\_by\_lower](#tableio.config_data_apply._registered_formats_by_lower)
  * [\_candidate\_formats](#tableio.config_data_apply._candidate_formats)
  * [\_candidate\_impls](#tableio.config_data_apply._candidate_impls)
  * [\_match\_group](#tableio.config_data_apply._match_group)
  * [\_best\_default\_names](#tableio.config_data_apply._best_default_names)
  * [\_base\_arg\_items](#tableio.config_data_apply._base_arg_items)
  * [\_csv\_arg\_items](#tableio.config_data_apply._csv_arg_items)
  * [\_html\_arg\_items](#tableio.config_data_apply._html_arg_items)
  * [\_latex\_arg\_items](#tableio.config_data_apply._latex_arg_items)
  * [\_arg\_items](#tableio.config_data_apply._arg_items)
  * [\_arg\_dict](#tableio.config_data_apply._arg_dict)
  * [\_filtered\_args](#tableio.config_data_apply._filtered_args)
  * [\_all\_option\_config](#tableio.config_data_apply._all_option_config)
  * [tio\_config\_default](#tableio.config_data_apply.tio_config_default)
  * [tio\_config\_optional\_args](#tableio.config_data_apply.tio_config_optional_args)
  * [tio\_config\_create](#tableio.config_data_apply.tio_config_create)
  * [tio\_config\_ignored\_names](#tableio.config_data_apply.tio_config_ignored_names)
  * [tio\_config\_trim](#tableio.config_data_apply.tio_config_trim)
  * [\_kept](#tableio.config_data_apply._kept)
  * [\_trim\_csv](#tableio.config_data_apply._trim_csv)
  * [\_trim\_html](#tableio.config_data_apply._trim_html)
  * [\_trim\_latex](#tableio.config_data_apply._trim_latex)
* [tableio.config\_data\_validate](#tableio.config_data_validate)
  * [\_add\_issue](#tableio.config_data_validate._add_issue)
  * [\_valid\_caps](#tableio.config_data_validate._valid_caps)
  * [\_valid\_file\_access](#tableio.config_data_validate._valid_file_access)
  * [\_choices\_text](#tableio.config_data_validate._choices_text)
  * [\_matches\_choice](#tableio.config_data_validate._matches_choice)
  * [\_choice\_issue](#tableio.config_data_validate._choice_issue)
  * [\_valid\_choice](#tableio.config_data_validate._valid_choice)
  * [\_validate\_str](#tableio.config_data_validate._validate_str)
  * [\_validate\_opt\_str](#tableio.config_data_validate._validate_opt_str)
  * [\_validate\_encoding](#tableio.config_data_validate._validate_encoding)
  * [\_validate\_int\_min](#tableio.config_data_validate._validate_int_min)
  * [\_validate\_one\_char](#tableio.config_data_validate._validate_one_char)
  * [\_validate\_nonempty\_str](#tableio.config_data_validate._validate_nonempty_str)
  * [\_validate\_top\_values](#tableio.config_data_validate._validate_top_values)
  * [\_validate\_csv](#tableio.config_data_validate._validate_csv)
  * [\_validate\_html](#tableio.config_data_validate._validate_html)
  * [\_validate\_latex](#tableio.config_data_validate._validate_latex)
  * [\_match\_caps](#tableio.config_data_validate._match_caps)
  * [\_backend\_can\_be\_checked](#tableio.config_data_validate._backend_can_be_checked)
  * [\_impl\_choices](#tableio.config_data_validate._impl_choices)
  * [\_impl\_matches\_format](#tableio.config_data_validate._impl_matches_format)
  * [\_validate\_impl\_for\_format](#tableio.config_data_validate._validate_impl_for_format)
  * [\_validate\_backend](#tableio.config_data_validate._validate_backend)
  * [tio\_config\_validate](#tableio.config_data_validate.tio_config_validate)
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
    * [\_end\_state](#tableio.tableio.TableIO._end_state)
    * [\_write\_file\_suffix](#tableio.tableio.TableIO._write_file_suffix)
    * [\_close](#tableio.tableio.TableIO._close)
    * [\_check\_listdimensions](#tableio.tableio.TableIO._check_listdimensions)
    * [\_value\_area](#tableio.tableio.TableIO._value_area)
    * [\_check\_dictdimensions](#tableio.tableio.TableIO._check_dictdimensions)
    * [\_check\_box\_write](#tableio.tableio.TableIO._check_box_write)
    * [\_check\_box\_read](#tableio.tableio.TableIO._check_box_read)
    * [\_check\_box\_impl](#tableio.tableio.TableIO._check_box_impl)
    * [\_check\_filtered\_data\_range](#tableio.tableio.TableIO._check_filtered_data_range)
    * [\_check\_border\_style](#tableio.tableio.TableIO._check_border_style)
    * [\_write\_heading](#tableio.tableio.TableIO._write_heading)
    * [\_write\_table\_listdata](#tableio.tableio.TableIO._write_table_listdata)
    * [\_write\_table\_fmtlistdata](#tableio.tableio.TableIO._write_table_fmtlistdata)
    * [\_write\_table\_dictdata](#tableio.tableio.TableIO._write_table_dictdata)
    * [\_write\_table\_fmtdictdata](#tableio.tableio.TableIO._write_table_fmtdictdata)
    * [\_read\_table\_listdata](#tableio.tableio.TableIO._read_table_listdata)
    * [\_read\_table\_dictdata](#tableio.tableio.TableIO._read_table_dictdata)
    * [\_file\_exists\_check](#tableio.tableio.TableIO._file_exists_check)
    * [\_check\_file\_is\_writable](#tableio.tableio.TableIO._check_file_is_writable)
    * [\_list\_sheets](#tableio.tableio.TableIO._list_sheets)
    * [\_select\_sheet](#tableio.tableio.TableIO._select_sheet)
    * [\_current\_sheet\_name](#tableio.tableio.TableIO._current_sheet_name)
    * [\_find\_value](#tableio.tableio.TableIO._find_value)
    * [\_read\_cells](#tableio.tableio.TableIO._read_cells)
    * [\_write\_cells](#tableio.tableio.TableIO._write_cells)
* [tableio.color](#tableio.color)
  * [Color](#tableio.color.Color)
    * [NONE](#tableio.color.Color.NONE)
    * [RED](#tableio.color.Color.RED)
    * [GREEN](#tableio.color.Color.GREEN)
    * [YELLOW](#tableio.color.Color.YELLOW)
* [tableio.tableio\_ods\_odfdo](#tableio.tableio_ods_odfdo)
  * [\_manifest\_xml\_without\_configuration\_entries](#tableio.tableio_ods_odfdo._manifest_xml_without_configuration_entries)
  * [\_referenced\_style\_names](#tableio.tableio_ods_odfdo._referenced_style_names)
  * [\_content\_xml\_without\_unused\_styles](#tableio.tableio_ods_odfdo._content_xml_without_unused_styles)
  * [\_styles\_xml\_with\_required\_defaults](#tableio.tableio_ods_odfdo._styles_xml_with_required_defaults)
  * [\_rewrite\_saved\_document](#tableio.tableio_ods_odfdo._rewrite_saved_document)
  * [TableIOOdsOdfdo](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo)
    * [\_\_init\_\_](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.__init__)
    * [get\_capabilities](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_capabilities)
    * [get\_description](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.get_description)
    * [file\_name\_extension](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.file_name_extension)
    * [open](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo.open)
    * [\_checked\_lang](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._checked_lang)
    * [\_split\_rfc3066\_language](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._split_rfc3066_language)
    * [\_set\_document\_language](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_document_language)
    * [\_end\_state](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_file_suffix)
    * [\_close](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._close)
    * [\_table\_name\_map](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._table_name_map)
    * [\_list\_sheets](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._list_sheets)
    * [\_select\_sheet](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._select_sheet)
    * [\_current\_sheet\_name](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._current_sheet_name)
    * [\_read\_sheet](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._read_sheet)
    * [\_write\_sheet](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_sheet)
    * [\_spreadsheet\_body](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._spreadsheet_body)
    * [\_database\_range\_container](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_container)
    * [\_database\_ranges](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_ranges)
    * [\_quoted\_table\_name](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._quoted_table_name)
    * [\_database\_range\_address](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_address)
    * [\_split\_range\_endpoint](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._split_range_endpoint)
    * [\_cell\_ref\_to\_position](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_ref_to_position)
    * [\_endpoint\_position](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._endpoint_position)
    * [\_database\_range\_bounds](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_bounds)
    * [\_write\_value\_to\_sheet](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_value_to_sheet)
    * [\_set\_cell\_format](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_cell_format)
    * [\_set\_cell\_borders](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_cell_borders)
    * [\_apply\_heading\_style](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._apply_heading_style)
    * [\_last\_used\_row](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._last_used_row)
    * [\_last\_used\_column](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._last_used_column)
    * [\_cell\_value](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_value)
    * [\_filtered\_range\_infos](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._filtered_range_infos)
    * [\_delete\_filtered\_range](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._delete_filtered_range)
    * [\_add\_filtered\_range](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._add_filtered_range)
    * [\_column\_width\_string](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_width_string)
    * [\_column\_width\_from\_text](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_width_from_text)
    * [\_current\_column\_width](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._current_column_width)
    * [\_set\_column\_width\_if\_wider](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_column_width_if_wider)
    * [\_next\_style\_name](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._next_style_name)
    * [\_cell\_style\_state\_key](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_state_key)
    * [\_cell\_style\_state](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_state)
    * [\_apply\_cell\_style](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._apply_cell_style)
    * [\_border\_property\_text](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._border_property_text)
    * [\_cell\_style\_name](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_name)
    * [\_column\_style\_name](#tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_style_name)
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
    * [\_close](#tableio.tableio_textbased.TableIOTextBased._close)
    * [\_get\_last\_chars\_written\_impl](#tableio.tableio_textbased.TableIOTextBased._get_last_chars_written_impl)
    * [\_get\_last\_chars\_written](#tableio.tableio_textbased.TableIOTextBased._get_last_chars_written)
    * [\_ensure\_empty\_line\_before](#tableio.tableio_textbased.TableIOTextBased._ensure_empty_line_before)
* [tableio.tableio\_excel\_pylightxl](#tableio.tableio_excel_pylightxl)
  * [\_WorksheetLike](#tableio.tableio_excel_pylightxl._WorksheetLike)
    * [\_calc\_size](#tableio.tableio_excel_pylightxl._WorksheetLike._calc_size)
    * [update\_address](#tableio.tableio_excel_pylightxl._WorksheetLike.update_address)
  * [\_worksheet\_names](#tableio.tableio_excel_pylightxl._worksheet_names)
  * [\_database\_worksheet](#tableio.tableio_excel_pylightxl._database_worksheet)
  * [\_worksheet\_cells](#tableio.tableio_excel_pylightxl._worksheet_cells)
  * [\_recalculate\_worksheet\_size](#tableio.tableio_excel_pylightxl._recalculate_worksheet_size)
  * [\_worksheet\_id\_attr](#tableio.tableio_excel_pylightxl._worksheet_id_attr)
  * [\_sheet\_xml\_targets](#tableio.tableio_excel_pylightxl._sheet_xml_targets)
  * [\_xml\_text](#tableio.tableio_excel_pylightxl._xml_text)
  * [\_inline\_string\_text](#tableio.tableio_excel_pylightxl._inline_string_text)
  * [\_number\_from\_cell\_text](#tableio.tableio_excel_pylightxl._number_from_cell_text)
  * [\_xml\_bytes](#tableio.tableio_excel_pylightxl._xml_bytes)
  * [\_datetime\_from\_excel\_number](#tableio.tableio_excel_pylightxl._datetime_from_excel_number)
  * [\_datetime\_to\_excel\_number](#tableio.tableio_excel_pylightxl._datetime_to_excel_number)
  * [\_sheet\_data\_from\_xml](#tableio.tableio_excel_pylightxl._sheet_data_from_xml)
  * [\_load\_named\_ranges](#tableio.tableio_excel_pylightxl._load_named_ranges)
  * [\_read\_database](#tableio.tableio_excel_pylightxl._read_database)
  * [\_style\_index\_for\_code](#tableio.tableio_excel_pylightxl._style_index_for_code)
  * [\_styles\_xml](#tableio.tableio_excel_pylightxl._styles_xml)
  * [\_theme\_xml](#tableio.tableio_excel_pylightxl._theme_xml)
  * [TableIOExcelPylightxl](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl)
    * [\_\_init\_\_](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.__init__)
    * [get\_description](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_description)
    * [get\_capabilities](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.get_capabilities)
    * [open](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl.open)
    * [\_initialize\_sheet\_style\_codes](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._initialize_sheet_style_codes)
    * [\_end\_state](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_file_suffix)
    * [\_close](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._close)
    * [\_temporary\_workbook\_path](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._temporary_workbook_path)
    * [\_invalid\_placeholder\_cell](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._invalid_placeholder_cell)
    * [\_normalize\_written\_bool\_cell](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._normalize_written_bool_cell)
    * [\_rewrite\_workbook\_xml](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._rewrite_workbook_xml)
    * [\_content\_types\_with\_required\_parts](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._content_types_with_required_parts)
    * [\_workbook\_rels\_with\_required\_parts](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._workbook_rels_with_required_parts)
    * [\_entry\_style\_codes](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._entry_style_codes)
    * [\_rewrite\_row\_xml](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._rewrite_row_xml)
    * [\_worksheet\_xml\_for\_output](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._worksheet_xml_for_output)
    * [\_current\_style\_codes](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._current_style_codes)
    * [\_list\_sheets](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._list_sheets)
    * [\_select\_sheet](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._select_sheet)
    * [\_current\_sheet\_name](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._current_sheet_name)
    * [\_read\_sheet](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._read_sheet)
    * [\_write\_sheet](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_sheet)
    * [\_write\_value\_to\_sheet](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_value_to_sheet)
    * [\_set\_cell\_format](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._set_cell_format)
    * [\_apply\_heading\_style](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._apply_heading_style)
    * [\_last\_used\_row](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._last_used_row)
    * [\_last\_used\_column](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._last_used_column)
    * [\_cell\_value](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._cell_value)
    * [\_parse\_typed\_cell\_value](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._parse_typed_cell_value)
    * [\_filtered\_range\_infos](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._filtered_range_infos)
    * [\_delete\_filtered\_range](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._delete_filtered_range)
    * [\_add\_filtered\_range](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._add_filtered_range)
    * [\_set\_column\_width\_if\_wider](#tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._set_column_width_if_wider)
* [tableio.optional\_args](#tableio.optional_args)
  * [CsvDialect](#tableio.optional_args.CsvDialect)
    * [EXCEL](#tableio.optional_args.CsvDialect.EXCEL)
    * [UNIX](#tableio.optional_args.CsvDialect.UNIX)
  * [OptionalArgsDict](#tableio.optional_args.OptionalArgsDict)
    * [csv\_dialect](#tableio.optional_args.OptionalArgsDict.csv_dialect)
    * [csv\_delimiter](#tableio.optional_args.OptionalArgsDict.csv_delimiter)
    * [csv\_quoting](#tableio.optional_args.OptionalArgsDict.csv_quoting)
    * [csv\_quotechar](#tableio.optional_args.OptionalArgsDict.csv_quotechar)
    * [csv\_lineterminator](#tableio.optional_args.OptionalArgsDict.csv_lineterminator)
    * [csv\_escapechar](#tableio.optional_args.OptionalArgsDict.csv_escapechar)
  * [mformat\_optargs\_from\_optionalargs](#tableio.optional_args.mformat_optargs_from_optionalargs)
* [tableio.access\_capability](#tableio.access_capability)
  * [NO\_ERROR\_OUTPUT](#tableio.access_capability.NO_ERROR_OUTPUT)
  * [InsufficientCapabilities](#tableio.access_capability.InsufficientCapabilities)
    * [\_\_init\_\_](#tableio.access_capability.InsufficientCapabilities.__init__)
  * [\_raise\_error](#tableio.access_capability._raise_error)
  * [\_check\_access\_value](#tableio.access_capability._check_access_value)
  * [\_check\_capabilities\_value](#tableio.access_capability._check_capabilities_value)
  * [access\_capabilities](#tableio.access_capability.access_capabilities)
  * [add\_access\_capabilities](#tableio.access_capability.add_access_capabilities)
  * [\_missing\_access\_caps](#tableio.access_capability._missing_access_caps)
  * [\_access\_error\_message](#tableio.access_capability._access_error_message)
  * [check\_access\_capabilities](#tableio.access_capability.check_access_capabilities)
* [tableio.config\_data](#tableio.config_data)
  * [CsvConfigData](#tableio.config_data.CsvConfigData)
    * [dialect](#tableio.config_data.CsvConfigData.dialect)
    * [delimiter](#tableio.config_data.CsvConfigData.delimiter)
    * [quoting](#tableio.config_data.CsvConfigData.quoting)
    * [quotechar](#tableio.config_data.CsvConfigData.quotechar)
    * [lineterminator](#tableio.config_data.CsvConfigData.lineterminator)
    * [escapechar](#tableio.config_data.CsvConfigData.escapechar)
  * [HtmlConfigData](#tableio.config_data.HtmlConfigData)
    * [css\_file](#tableio.config_data.HtmlConfigData.css_file)
  * [LatexConfigData](#tableio.config_data.LatexConfigData)
    * [document\_class](#tableio.config_data.LatexConfigData.document_class)
    * [preamble](#tableio.config_data.LatexConfigData.preamble)
  * [ConfigData](#tableio.config_data.ConfigData)
    * [format\_name](#tableio.config_data.ConfigData.format_name)
    * [implementation](#tableio.config_data.ConfigData.implementation)
    * [character\_encoding](#tableio.config_data.ConfigData.character_encoding)
    * [language](#tableio.config_data.ConfigData.language)
    * [title](#tableio.config_data.ConfigData.title)
    * [paper\_size](#tableio.config_data.ConfigData.paper_size)
    * [line\_length](#tableio.config_data.ConfigData.line_length)
    * [table\_max\_line\_length](#tableio.config_data.ConfigData.table_max_line_length)
    * [table\_alignment](#tableio.config_data.ConfigData.table_alignment)
    * [csv](#tableio.config_data.ConfigData.csv)
    * [html](#tableio.config_data.ConfigData.html)
    * [latex](#tableio.config_data.ConfigData.latex)
* [tableio.factory](#tableio.factory)
  * [\_the\_factory](#tableio.factory._the_factory)
  * [TableIOFactoryConflictError](#tableio.factory.TableIOFactoryConflictError)
  * [TableIOFactoryNoSuchError](#tableio.factory.TableIOFactoryNoSuchError)
  * [TableIOFactoryNoCapabilityMatch](#tableio.factory.TableIOFactoryNoCapabilityMatch)
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
    * [get\_usage](#tableio.factory.FactoryFormatInfo.get_usage)
  * [TableIOFactory](#tableio.factory.TableIOFactory)
    * [\_\_init\_\_](#tableio.factory.TableIOFactory.__init__)
    * [i\_get\_factory](#tableio.factory.TableIOFactory.i_get_factory)
    * [register](#tableio.factory.TableIOFactory.register)
    * [i\_register](#tableio.factory.TableIOFactory.i_register)
    * [create](#tableio.factory.TableIOFactory.create)
    * [i\_create](#tableio.factory.TableIOFactory.i_create)
    * [\_correct\_format\_name](#tableio.factory.TableIOFactory._correct_format_name)
    * [\_format\_info](#tableio.factory.TableIOFactory._format_info)
    * [\_select\_implementation\_name](#tableio.factory.TableIOFactory._select_implementation_name)
    * [filter\_args](#tableio.factory.TableIOFactory.filter_args)
    * [i\_filter\_args](#tableio.factory.TableIOFactory.i_filter_args)
    * [get\_registered\_formats](#tableio.factory.TableIOFactory.get_registered_formats)
    * [i\_get\_registered\_formats](#tableio.factory.TableIOFactory.i_get_registered_formats)
    * [get\_registered\_implementations](#tableio.factory.TableIOFactory.get_registered_implementations)
    * [i\_get\_registered\_implementations](#tableio.factory.TableIOFactory.i_get_registered_implementations)
    * [i\_get\_reg\_impls](#tableio.factory.TableIOFactory.i_get_reg_impls)
    * [\_implementation\_matches](#tableio.factory.TableIOFactory._implementation_matches)
    * [\_implementation\_names](#tableio.factory.TableIOFactory._implementation_names)
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
  * [\_validate\_column\_order](#tableio.value_type._validate_column_order)
  * [\_raise\_empty\_row\_error](#tableio.value_type._raise_empty_row_error)
  * [\_first\_row\_is\_plain\_dict\_data](#tableio.value_type._first_row_is_plain_dict_data)
  * [\_first\_row\_is\_formatted\_dict\_data](#tableio.value_type._first_row_is_formatted_dict_data)
  * [\_normalize\_dict\_data\_with\_missing\_cell](#tableio.value_type._normalize_dict_data_with_missing_cell)
  * [\_normalize\_dict\_data\_impl](#tableio.value_type._normalize_dict_data_impl)
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
* [tableio.border\_helper](#tableio.border_helper)
  * [BorderWeight](#tableio.border_helper.BorderWeight)
  * [CellBorder](#tableio.border_helper.CellBorder)
  * [NO\_BORDERS](#tableio.border_helper.NO_BORDERS)
  * [CellStyleState](#tableio.border_helper.CellStyleState)
  * [DEFAULT\_CELL\_STYLE](#tableio.border_helper.DEFAULT_CELL_STYLE)
  * [\_BorderComponents](#tableio.border_helper._BorderComponents)
  * [\_thicker](#tableio.border_helper._thicker)
  * [BorderHelper](#tableio.border_helper.BorderHelper)
    * [\_\_init\_\_](#tableio.border_helper.BorderHelper.__init__)
    * [\_checked\_style](#tableio.border_helper.BorderHelper._checked_style)
    * [has\_borders](#tableio.border_helper.BorderHelper.has_borders)
    * [\_horizontal\_boundary](#tableio.border_helper.BorderHelper._horizontal_boundary)
    * [\_vertical\_boundary](#tableio.border_helper.BorderHelper._vertical_boundary)
    * [cell\_border](#tableio.border_helper.BorderHelper.cell_border)
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
  * [TableBorderStyle](#tableio.tableio_types.TableBorderStyle)
    * [NONE](#tableio.tableio_types.TableBorderStyle.NONE)
    * [OUTER\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_THIN)
    * [OUTER\_THICK](#tableio.tableio_types.TableBorderStyle.OUTER_THICK)
    * [OUTER\_FIRST\_ROW\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THIN)
    * [OUTER\_FIRST\_ROW\_THICK](#tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK)
    * [OUTER\_THICK\_FIRST\_ROW\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_THICK_FIRST_ROW_THIN)
    * [OUTER\_FIRST\_ROW\_THICK\_VERTICAL\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK_VERTICAL_THIN)
    * [OUTER\_FIRST\_ROW\_THICK\_INNER\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN)
    * [OUTER\_THICK\_INNER\_THIN](#tableio.tableio_types.TableBorderStyle.OUTER_THICK_INNER_THIN)
    * [ALL\_THIN](#tableio.tableio_types.TableBorderStyle.ALL_THIN)
    * [ALL\_THICK](#tableio.tableio_types.TableBorderStyle.ALL_THICK)
* [tableio.config\_data\_describe](#tableio.config_data_describe)
  * [ConfigSpec](#tableio.config_data_describe.ConfigSpec)
    * [name](#tableio.config_data_describe.ConfigSpec.name)
    * [description](#tableio.config_data_describe.ConfigSpec.description)
    * [value\_type](#tableio.config_data_describe.ConfigSpec.value_type)
    * [default\_text](#tableio.config_data_describe.ConfigSpec.default_text)
    * [choices](#tableio.config_data_describe.ConfigSpec.choices)
    * [relevant\_formats](#tableio.config_data_describe.ConfigSpec.relevant_formats)
    * [relevant\_impls](#tableio.config_data_describe.ConfigSpec.relevant_impls)
    * [optional\_arg](#tableio.config_data_describe.ConfigSpec.optional_arg)
  * [\_csv\_dialect\_choices](#tableio.config_data_describe._csv_dialect_choices)
  * [\_table\_alignment\_choices](#tableio.config_data_describe._table_alignment_choices)
  * [\_formats\_for\_arg](#tableio.config_data_describe._formats_for_arg)
  * [\_impls\_for\_arg](#tableio.config_data_describe._impls_for_arg)
  * [\_arg\_spec](#tableio.config_data_describe._arg_spec)
  * [tio\_config\_specs](#tableio.config_data_describe.tio_config_specs)
  * [tio\_config\_descriptions](#tableio.config_data_describe.tio_config_descriptions)
  * [tio\_config\_describe](#tableio.config_data_describe.tio_config_describe)
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
    * [can\_write\_borders](#tableio.capability.Capabilities.can_write_borders)
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
  * [\_FormatKey](#tableio.tableio_excel_xlsxwriter._FormatKey)
  * [\_WorksheetLike](#tableio.tableio_excel_xlsxwriter._WorksheetLike)
    * [add\_table](#tableio.tableio_excel_xlsxwriter._WorksheetLike.add_table)
    * [set\_column](#tableio.tableio_excel_xlsxwriter._WorksheetLike.set_column)
    * [write](#tableio.tableio_excel_xlsxwriter._WorksheetLike.write)
    * [write\_blank](#tableio.tableio_excel_xlsxwriter._WorksheetLike.write_blank)
  * [\_WorkbookLike](#tableio.tableio_excel_xlsxwriter._WorkbookLike)
    * [add\_worksheet](#tableio.tableio_excel_xlsxwriter._WorkbookLike.add_worksheet)
    * [add\_format](#tableio.tableio_excel_xlsxwriter._WorkbookLike.add_format)
    * [close](#tableio.tableio_excel_xlsxwriter._WorkbookLike.close)
  * [\_SheetState](#tableio.tableio_excel_xlsxwriter._SheetState)
  * [TableIOExcelXlsxWriter](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter)
    * [\_\_init\_\_](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.__init__)
    * [get\_capabilities](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_capabilities)
    * [get\_description](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.get_description)
    * [open](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter.open)
    * [\_end\_state](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_file_suffix)
    * [\_close](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._close)
    * [\_create\_sheet\_state](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._create_sheet_state)
    * [\_current\_sheet\_state](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._current_sheet_state)
    * [\_list\_sheets](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._list_sheets)
    * [\_select\_sheet](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._select_sheet)
    * [\_current\_sheet\_name](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._current_sheet_name)
    * [\_read\_sheet](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_sheet)
    * [\_write\_sheet](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_sheet)
    * [\_write\_value\_to\_sheet](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_value_to_sheet)
    * [\_set\_cell\_format](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_cell_format)
    * [\_apply\_heading\_style](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._apply_heading_style)
    * [\_last\_used\_row](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._last_used_row)
    * [\_last\_used\_column](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._last_used_column)
    * [\_cell\_value](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._cell_value)
    * [\_filtered\_range\_infos](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._filtered_range_infos)
    * [\_delete\_filtered\_range](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._delete_filtered_range)
    * [\_add\_filtered\_range](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._add_filtered_range)
    * [\_set\_column\_width\_if\_wider](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_column_width_if_wider)
    * [\_filter\_range\_name\_in\_use](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._filter_range_name_in_use)
    * [\_read\_table\_listdata](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_table_listdata)
    * [\_read\_table\_dictdata](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_table_dictdata)
    * [\_cell\_fmt](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._cell_fmt)
    * [\_remove\_table\_metadata](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._remove_table_metadata)
    * [\_write\_actual\_cell](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_actual_cell)
    * [\_set\_stored\_cell\_style](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_stored_cell_style)
    * [\_border\_style](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._border_style)
    * [\_xlsx\_format](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._xlsx_format)
    * [\_set\_cell\_borders](#tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_cell_borders)
* [tableio.tableio\_csv](#tableio.tableio_csv)
  * [\_validate\_quoting](#tableio.tableio_csv._validate_quoting)
  * [CsvDefinitions](#tableio.tableio_csv.CsvDefinitions)
    * [type](#tableio.tableio_csv.CsvDefinitions.type)
    * [delimiter](#tableio.tableio_csv.CsvDefinitions.delimiter)
    * [quoting](#tableio.tableio_csv.CsvDefinitions.quoting)
    * [quotechar](#tableio.tableio_csv.CsvDefinitions.quotechar)
    * [lineterminator](#tableio.tableio_csv.CsvDefinitions.lineterminator)
    * [escapechar](#tableio.tableio_csv.CsvDefinitions.escapechar)
  * [\_get\_csv\_dialect\_type](#tableio.tableio_csv._get_csv_dialect_type)
  * [\_get\_csv\_dialect](#tableio.tableio_csv._get_csv_dialect)
  * [\_is\_heading\_line](#tableio.tableio_csv._is_heading_line)
  * [TableIOCsv](#tableio.tableio_csv.TableIOCsv)
    * [\_\_init\_\_](#tableio.tableio_csv.TableIOCsv.__init__)
    * [file\_name\_extension](#tableio.tableio_csv.TableIOCsv.file_name_extension)
    * [get\_description](#tableio.tableio_csv.TableIOCsv.get_description)
    * [get\_capabilities](#tableio.tableio_csv.TableIOCsv.get_capabilities)
    * [\_end\_state](#tableio.tableio_csv.TableIOCsv._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_csv.TableIOCsv._write_file_suffix)
    * [\_write\_heading](#tableio.tableio_csv.TableIOCsv._write_heading)
    * [\_write\_table\_listdata](#tableio.tableio_csv.TableIOCsv._write_table_listdata)
    * [\_write\_table\_fmtlistdata](#tableio.tableio_csv.TableIOCsv._write_table_fmtlistdata)
    * [\_write\_table\_dictdata](#tableio.tableio_csv.TableIOCsv._write_table_dictdata)
    * [\_write\_table\_fmtdictdata](#tableio.tableio_csv.TableIOCsv._write_table_fmtdictdata)
    * [\_read\_raw\_sections](#tableio.tableio_csv.TableIOCsv._read_raw_sections)
    * [\_read\_table\_listdata](#tableio.tableio_csv.TableIOCsv._read_table_listdata)
    * [\_read\_table\_dictdata](#tableio.tableio_csv.TableIOCsv._read_table_dictdata)
* [tableio.config\_data\_error](#tableio.config_data_error)
  * [ConfigIssue](#tableio.config_data_error.ConfigIssue)
    * [name](#tableio.config_data_error.ConfigIssue.name)
    * [message](#tableio.config_data_error.ConfigIssue.message)
  * [ConfigError](#tableio.config_data_error.ConfigError)
    * [issues](#tableio.config_data_error.ConfigError.issues)
    * [\_\_init\_\_](#tableio.config_data_error.ConfigError.__init__)
* [tableio.tableio\_spreadsheetbased](#tableio.tableio_spreadsheetbased)
  * [excel\_column\_name](#tableio.tableio_spreadsheetbased.excel_column_name)
  * [\_ScanResult](#tableio.tableio_spreadsheetbased._ScanResult)
  * [\_SheetState](#tableio.tableio_spreadsheetbased._SheetState)
  * [TableIOSpreadsheetBased](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased)
    * [\_\_init\_\_](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased.__init__)
    * [\_heading\_font\_size](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._heading_font_size)
    * [\_python\_value\_from\_spreadsheet](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._python_value_from_spreadsheet)
    * [\_spreadsheet\_value\_from\_python](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._spreadsheet_value_from_python)
    * [\_sheet\_key](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._sheet_key)
    * [\_find\_matching\_sheet\_name](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_matching_sheet_name)
    * [\_current\_sheet\_key](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._current_sheet_key)
    * [\_make\_current\_sheet\_state](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._make_current_sheet_state)
    * [\_load\_current\_sheet\_state](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._load_current_sheet_state)
    * [\_save\_current\_sheet\_state](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._save_current_sheet_state)
    * [\_initialize\_positions](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._initialize_positions)
    * [\_read\_sheet](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_sheet)
    * [\_write\_sheet](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_sheet)
    * [\_write\_value\_to\_sheet](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_value_to_sheet)
    * [\_set\_cell\_format](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_cell_format)
    * [\_set\_cell\_borders](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_cell_borders)
    * [\_apply\_heading\_style](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._apply_heading_style)
    * [\_last\_used\_row](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._last_used_row)
    * [\_last\_used\_column](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._last_used_column)
    * [\_cell\_value](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._cell_value)
    * [\_filtered\_range\_infos](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._filtered_range_infos)
    * [\_delete\_filtered\_range](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._delete_filtered_range)
    * [\_add\_filtered\_range](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._add_filtered_range)
    * [\_set\_column\_width\_if\_wider](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_column_width_if_wider)
    * [\_used\_bounds\_by\_cell\_scan](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._used_bounds_by_cell_scan)
    * [\_write\_value](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_value)
    * [\_clear\_range](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._clear_range)
    * [\_read\_limits](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_limits)
    * [\_scan\_limit\_bottom](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_limit_bottom)
    * [\_scan\_limit\_right](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_limit_right)
    * [\_row\_nonempty\_columns](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_nonempty_columns)
    * [\_row\_is\_empty](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_is_empty)
    * [\_row\_is\_heading](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_is_heading)
    * [\_scan\_section](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_section)
    * [\_read\_grid](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_grid)
    * [\_update\_read\_positions](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_read_positions)
    * [\_range\_contains](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._range_contains)
    * [\_ranges\_overlap](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._ranges_overlap)
    * [\_sheet\_table\_regions](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._sheet_table_regions)
    * [\_existing\_table\_regions](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._existing_table_regions)
    * [\_check\_boxed\_table\_overwrite](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._check_boxed_table_overwrite)
    * [\_filter\_range\_name\_in\_use](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._filter_range_name_in_use)
    * [\_next\_filter\_range\_name](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._next_filter_range_name)
    * [\_remove\_overlapping\_filtered\_ranges](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._remove_overlapping_filtered_ranges)
    * [\_write\_filtered\_data\_range](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_filtered_data_range)
    * [\_values\_match](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._values_match)
    * [\_split\_cell\_grid](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._split_cell_grid)
    * [\_find\_bounds](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_bounds)
    * [\_grid\_matches](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._grid_matches)
    * [\_column\_width\_text](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._column_width_text)
    * [\_table\_column\_width](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._table_column_width)
    * [\_update\_table\_column\_widths](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_table_column_widths)
    * [\_write\_start](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_start)
    * [\_update\_write\_position](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_write_position)
    * [\_write\_grid](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_grid)
    * [\_write\_grid\_borders](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_grid_borders)
    * [\_write\_heading](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_heading)
    * [\_split\_cell\_value](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._split_cell_value)
    * [\_write\_table\_listdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_listdata)
    * [\_write\_table\_fmtlistdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_fmtlistdata)
    * [\_write\_table\_dictdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_dictdata)
    * [\_write\_table\_fmtdictdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_fmtdictdata)
    * [\_read\_table\_listdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_table_listdata)
    * [\_read\_table\_dictdata](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_table_dictdata)
    * [\_find\_value](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_value)
    * [\_read\_cells](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_cells)
    * [\_write\_cells](#tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_cells)
* [tableio.tableio\_mformatbased](#tableio.tableio_mformatbased)
  * [\_allow\_overwrite](#tableio.tableio_mformatbased._allow_overwrite)
  * [TableIOMformatBased](#tableio.tableio_mformatbased.TableIOMformatBased)
    * [\_\_init\_\_](#tableio.tableio_mformatbased.TableIOMformatBased.__init__)
    * [get\_capabilities](#tableio.tableio_mformatbased.TableIOMformatBased.get_capabilities)
    * [get\_row\_format\_capability](#tableio.tableio_mformatbased.TableIOMformatBased.get_row_format_capability)
    * [open](#tableio.tableio_mformatbased.TableIOMformatBased.open)
    * [\_close](#tableio.tableio_mformatbased.TableIOMformatBased._close)
    * [\_end\_state](#tableio.tableio_mformatbased.TableIOMformatBased._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_mformatbased.TableIOMformatBased._write_file_suffix)
    * [\_write\_heading](#tableio.tableio_mformatbased.TableIOMformatBased._write_heading)
    * [\_write\_table\_listdata](#tableio.tableio_mformatbased.TableIOMformatBased._write_table_listdata)
    * [\_write\_table\_fmtlistdata](#tableio.tableio_mformatbased.TableIOMformatBased._write_table_fmtlistdata)
    * [\_write\_table\_dictdata](#tableio.tableio_mformatbased.TableIOMformatBased._write_table_dictdata)
    * [\_write\_table\_fmtdictdata](#tableio.tableio_mformatbased.TableIOMformatBased._write_table_fmtdictdata)
    * [\_read\_table\_listdata](#tableio.tableio_mformatbased.TableIOMformatBased._read_table_listdata)
    * [\_read\_table\_dictdata](#tableio.tableio_mformatbased.TableIOMformatBased._read_table_dictdata)
* [tableio.tableio\_excelbased](#tableio.tableio_excelbased)
  * [TableIOExcelBased](#tableio.tableio_excelbased.TableIOExcelBased)
    * [\_DATETIME\_NUMBER\_FORMAT](#tableio.tableio_excelbased.TableIOExcelBased._DATETIME_NUMBER_FORMAT)
    * [\_\_init\_\_](#tableio.tableio_excelbased.TableIOExcelBased.__init__)
    * [file\_name\_extension](#tableio.tableio_excelbased.TableIOExcelBased.file_name_extension)
    * [\_datetime\_number\_format](#tableio.tableio_excelbased.TableIOExcelBased._datetime_number_format)
    * [\_excel\_column\_name](#tableio.tableio_excelbased.TableIOExcelBased._excel_column_name)
    * [\_excel\_cell\_ref](#tableio.tableio_excelbased.TableIOExcelBased._excel_cell_ref)
    * [\_excel\_range\_ref](#tableio.tableio_excelbased.TableIOExcelBased._excel_range_ref)
    * [\_filtered\_table\_header](#tableio.tableio_excelbased.TableIOExcelBased._filtered_table_header)
    * [\_filtered\_table\_headers](#tableio.tableio_excelbased.TableIOExcelBased._filtered_table_headers)
* [tableio.reg\_pkg\_formats](#tableio.reg_pkg_formats)
  * [register\_formats\_in\_pkg](#tableio.reg_pkg_formats.register_formats_in_pkg)
* [tableio.tableio\_excel\_openpyxl](#tableio.tableio_excel_openpyxl)
  * [\_xml\_tag](#tableio.tableio_excel_openpyxl._xml_tag)
  * [\_font\_child\_sort\_key](#tableio.tableio_excel_openpyxl._font_child_sort_key)
  * [\_styles\_xml\_with\_sorted\_fonts](#tableio.tableio_excel_openpyxl._styles_xml_with_sorted_fonts)
  * [\_new\_shared\_strings\_root](#tableio.tableio_excel_openpyxl._new_shared_strings_root)
  * [\_read\_shared\_strings\_root](#tableio.tableio_excel_openpyxl._read_shared_strings_root)
  * [\_shared\_string\_count](#tableio.tableio_excel_openpyxl._shared_string_count)
  * [\_shared\_strings\_xml](#tableio.tableio_excel_openpyxl._shared_strings_xml)
  * [\_inline\_string\_to\_shared\_string](#tableio.tableio_excel_openpyxl._inline_string_to_shared_string)
  * [\_sheet\_xml\_with\_shared\_strings](#tableio.tableio_excel_openpyxl._sheet_xml_with_shared_strings)
  * [\_content\_types\_with\_shared\_strings](#tableio.tableio_excel_openpyxl._content_types_with_shared_strings)
  * [\_next\_relationship\_id](#tableio.tableio_excel_openpyxl._next_relationship_id)
  * [\_workbook\_rels\_with\_shared\_strings](#tableio.tableio_excel_openpyxl._workbook_rels_with_shared_strings)
  * [\_is\_worksheet\_xml](#tableio.tableio_excel_openpyxl._is_worksheet_xml)
  * [\_worksheet\_rewrites\_with\_shared\_strings](#tableio.tableio_excel_openpyxl._worksheet_rewrites_with_shared_strings)
  * [\_rewrite\_saved\_workbook](#tableio.tableio_excel_openpyxl._rewrite_saved_workbook)
  * [TableIOExcelOpenPyXL](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL)
    * [\_\_init\_\_](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.__init__)
    * [get\_capabilities](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_capabilities)
    * [get\_description](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.get_description)
    * [open](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL.open)
    * [\_end\_state](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._end_state)
    * [\_write\_file\_suffix](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_file_suffix)
    * [\_close](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._close)
    * [\_worksheet\_name\_map](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._worksheet_name_map)
    * [\_set\_active\_worksheets](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_active_worksheets)
    * [\_list\_sheets](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._list_sheets)
    * [\_select\_sheet](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._select_sheet)
    * [\_current\_sheet\_name](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._current_sheet_name)
    * [\_read\_sheet](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._read_sheet)
    * [\_write\_sheet](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_sheet)
    * [\_highlight\_fill](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._highlight_fill)
    * [\_write\_value\_to\_sheet](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_value_to_sheet)
    * [\_set\_cell\_format](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_cell_format)
    * [\_border\_side](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._border_side)
    * [\_border\_value](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._border_value)
    * [\_set\_cell\_borders](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_cell_borders)
    * [\_apply\_heading\_style](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._apply_heading_style)
    * [\_last\_used\_row](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._last_used_row)
    * [\_last\_used\_column](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._last_used_column)
    * [\_cell\_value](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._cell_value)
    * [\_table\_bounds](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._table_bounds)
    * [\_filtered\_range\_infos](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._filtered_range_infos)
    * [\_delete\_filtered\_range](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._delete_filtered_range)
    * [\_normalize\_filtered\_table\_header](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._normalize_filtered_table_header)
    * [\_add\_filtered\_range](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._add_filtered_range)
    * [\_set\_column\_width\_if\_wider](#tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_column_width_if_wider)

<a id="tableio.config_data_apply"></a>

# tableio.config\_data\_apply

Apply framework-neutral configuration data to TableIO backends.

<a id="tableio.config_data_apply._config_error"></a>

#### \_config\_error

```python
def _config_error(name: str, message: str) -> None
```

Raise one structured configuration error.

<a id="tableio.config_data_apply._check_default_input"></a>

#### \_check\_default\_input

```python
def _check_default_input(capabilities: Capabilities, file_access: FileAccess,
                         format_name: Optional[str],
                         implementation: Optional[str],
                         include_all_options: bool) -> None
```

Validate runtime values used for default selection.

<a id="tableio.config_data_apply._registered_formats_by_lower"></a>

#### \_registered\_formats\_by\_lower

```python
def _registered_formats_by_lower() -> dict[str, str]
```

Return registered format names keyed by lowercase name.

<a id="tableio.config_data_apply._candidate_formats"></a>

#### \_candidate\_formats

```python
def _candidate_formats(format_name: Optional[str]) -> list[str]
```

Return default-selection format candidates.

<a id="tableio.config_data_apply._candidate_impls"></a>

#### \_candidate\_impls

```python
def _candidate_impls(format_name: str,
                     implementation: Optional[str]) -> list[str]
```

Return default-selection implementation candidates.

<a id="tableio.config_data_apply._match_group"></a>

#### \_match\_group

```python
def _match_group(format_name: str, implementation: str,
                 capabilities: Capabilities) -> Optional[int]
```

Return strictness group for a candidate implementation.

<a id="tableio.config_data_apply._best_default_names"></a>

#### \_best\_default\_names

```python
def _best_default_names(capabilities: Capabilities, format_name: Optional[str],
                        implementation: Optional[str]) -> tuple[str, str]
```

Return canonical default format and implementation names.

<a id="tableio.config_data_apply._base_arg_items"></a>

#### \_base\_arg\_items

```python
def _base_arg_items(config: ConfigData) -> list[tuple[str, str, object]]
```

Return configured top-level optional argument values.

<a id="tableio.config_data_apply._csv_arg_items"></a>

#### \_csv\_arg\_items

```python
def _csv_arg_items(config: ConfigData) -> list[tuple[str, str, object]]
```

Return configured CSV optional argument values.

<a id="tableio.config_data_apply._html_arg_items"></a>

#### \_html\_arg\_items

```python
def _html_arg_items(config: ConfigData) -> list[tuple[str, str, object]]
```

Return configured HTML optional argument values.

<a id="tableio.config_data_apply._latex_arg_items"></a>

#### \_latex\_arg\_items

```python
def _latex_arg_items(config: ConfigData) -> list[tuple[str, str, object]]
```

Return configured LaTeX optional argument values.

<a id="tableio.config_data_apply._arg_items"></a>

#### \_arg\_items

```python
def _arg_items(config: ConfigData) -> list[tuple[str, str, object]]
```

Return all configured optional argument values.

<a id="tableio.config_data_apply._arg_dict"></a>

#### \_arg\_dict

```python
def _arg_dict(config: ConfigData) -> OptionalArgsDict
```

Return unfiltered optional arguments from non-None config values.

<a id="tableio.config_data_apply._filtered_args"></a>

#### \_filtered\_args

```python
def _filtered_args(
        config: ConfigData,
        capabilities: Optional[Capabilities],
        extra_args: Optional[OptionalArgsDict] = None) -> OptionalArgs
```

Return filtered optional arguments, or None when empty.

<a id="tableio.config_data_apply._all_option_config"></a>

#### \_all\_option\_config

```python
def _all_option_config(format_name: str, implementation: str) -> ConfigData
```

Return a configuration object with all options visible.

<a id="tableio.config_data_apply.tio_config_default"></a>

#### tio\_config\_default

```python
def tio_config_default(capabilities: Capabilities,
                       file_access: FileAccess,
                       format_name: Optional[str] = None,
                       implementation: Optional[str] = None,
                       include_all_options: bool = False) -> ConfigData
```

Return recommended default configuration data.

Default format and implementation selection first prefers implementations
that strictly support the requested capabilities, then implementations
that can tolerate capabilities marked as ignorable. If several formats
match equally well, the preferred format order is Excel, ODS, then CSV.
If several implementations of the selected format match equally well,
their TableIO implementation priority is used.

**Arguments**:

- `capabilities` - Runtime capabilities the application intends to use.
- `file_access` - Runtime file access requested by the application.
- `format_name` - Optional preferred format name.
- `implementation` - Optional preferred implementation name.
- `include_all_options` - Include visible non-None values for all
  configuration options, for teaching and configuration templates.

**Returns**:

  A configuration object containing durable user choices only.

<a id="tableio.config_data_apply.tio_config_optional_args"></a>

#### tio\_config\_optional\_args

```python
def tio_config_optional_args(
        config: ConfigData,
        capabilities: Optional[Capabilities] = None) -> OptionalArgs
```

Build TableIO optional arguments from configuration data.

The returned arguments contain only values relevant to the selected
format and implementation. ``None`` values and irrelevant parameters are
omitted. Runtime-only callbacks are not included.

**Arguments**:

- `config` - Configuration data to convert.
- `capabilities` - Optional runtime capabilities used for matching.

**Returns**:

  Optional arguments suitable for ``create_tableio``.

<a id="tableio.config_data_apply.tio_config_create"></a>

#### tio\_config\_create

```python
def tio_config_create(
        config: ConfigData,
        file_name: PathLike,
        file_access: FileAccess,
        capabilities: Optional[Capabilities] = None,
        file_exists_callback: Optional[Callable[[str],
                                                None]] = None) -> TableIO
```

Create a TableIO object from configuration and runtime values.

**Arguments**:

- `config` - Durable configuration data.
- `file_name` - Runtime file name to open.
- `file_access` - Runtime file access to request.
- `capabilities` - Optional runtime capabilities used for matching.
- `file_exists_callback` - Optional runtime overwrite callback.

**Returns**:

  A TableIO object intended for use as a context manager.

<a id="tableio.config_data_apply.tio_config_ignored_names"></a>

#### tio\_config\_ignored\_names

```python
def tio_config_ignored_names(
        config: ConfigData,
        capabilities: Optional[Capabilities] = None) -> list[str]
```

Return configured parameters ignored by the selected backend.

**Arguments**:

- `config` - Configuration data to inspect.
- `capabilities` - Optional runtime capabilities used for matching.

**Returns**:

  Dotted parameter names whose values are well-formed but irrelevant.

<a id="tableio.config_data_apply.tio_config_trim"></a>

#### tio\_config\_trim

```python
def tio_config_trim(config: ConfigData,
                    capabilities: Optional[Capabilities] = None) -> ConfigData
```

Return a copy without parameters irrelevant to the selected backend.

The original configuration object is not mutated. This helper is intended
for applications that want to write a compact, backend-specific snapshot
while still allowing the normal configuration file to keep portable
preferences for several formats.

**Arguments**:

- `config` - Configuration data to copy and trim.
- `capabilities` - Optional runtime capabilities used for matching.

**Returns**:

  A copy of ``config`` containing only relevant configured values.

<a id="tableio.config_data_apply._kept"></a>

#### \_kept

```python
def _kept(value: Optional[_ValueT], arg_name: str,
          filtered_names: set[str]) -> Optional[_ValueT]
```

Return value when its optional argument was kept.

<a id="tableio.config_data_apply._trim_csv"></a>

#### \_trim\_csv

```python
def _trim_csv(config: ConfigData,
              filtered_names: set[str]) -> Optional[CsvConfigData]
```

Return trimmed CSV configuration data.

<a id="tableio.config_data_apply._trim_html"></a>

#### \_trim\_html

```python
def _trim_html(config: ConfigData,
               filtered_names: set[str]) -> Optional[HtmlConfigData]
```

Return trimmed HTML configuration data.

<a id="tableio.config_data_apply._trim_latex"></a>

#### \_trim\_latex

```python
def _trim_latex(config: ConfigData,
                filtered_names: set[str]) -> Optional[LatexConfigData]
```

Return trimmed LaTeX configuration data.

<a id="tableio.config_data_validate"></a>

# tableio.config\_data\_validate

Validation helpers for framework-neutral TableIO configuration.

<a id="tableio.config_data_validate._add_issue"></a>

#### \_add\_issue

```python
def _add_issue(issues: list[ConfigIssue], name: str, message: str) -> None
```

Add one validation issue to the list.

<a id="tableio.config_data_validate._valid_caps"></a>

#### \_valid\_caps

```python
def _valid_caps(value: Optional[Capabilities],
                issues: list[ConfigIssue]) -> Optional[Capabilities]
```

Return valid capabilities or add an issue.

<a id="tableio.config_data_validate._valid_file_access"></a>

#### \_valid\_file\_access

```python
def _valid_file_access(value: Optional[FileAccess],
                       issues: list[ConfigIssue]) -> Optional[FileAccess]
```

Return valid file access or add an issue.

<a id="tableio.config_data_validate._choices_text"></a>

#### \_choices\_text

```python
def _choices_text(choices: tuple[str, ...]) -> str
```

Return a compact allowed choices text.

<a id="tableio.config_data_validate._matches_choice"></a>

#### \_matches\_choice

```python
def _matches_choice(value: str, choices: tuple[str, ...]) -> bool
```

Return true if a string matches choices case-insensitively.

<a id="tableio.config_data_validate._choice_issue"></a>

#### \_choice\_issue

```python
def _choice_issue(name: str, value: str, spec: ConfigSpec) -> ConfigIssue
```

Build an issue for an unknown finite choice.

<a id="tableio.config_data_validate._valid_choice"></a>

#### \_valid\_choice

```python
def _valid_choice(value: object, spec: ConfigSpec,
                  issues: list[ConfigIssue]) -> bool
```

Validate one optional string against spec choices.

<a id="tableio.config_data_validate._validate_str"></a>

#### \_validate\_str

```python
def _validate_str(issues: list[ConfigIssue], name: str, value: object) -> bool
```

Validate one required string.

<a id="tableio.config_data_validate._validate_opt_str"></a>

#### \_validate\_opt\_str

```python
def _validate_opt_str(issues: list[ConfigIssue], name: str,
                      value: object) -> bool
```

Validate one optional string.

<a id="tableio.config_data_validate._validate_encoding"></a>

#### \_validate\_encoding

```python
def _validate_encoding(issues: list[ConfigIssue], value: object) -> None
```

Validate one optional encoding name.

<a id="tableio.config_data_validate._validate_int_min"></a>

#### \_validate\_int\_min

```python
def _validate_int_min(issues: list[ConfigIssue], name: str, value: object,
                      minimum: int, inclusive: bool) -> None
```

Validate one optional integer lower bound.

<a id="tableio.config_data_validate._validate_one_char"></a>

#### \_validate\_one\_char

```python
def _validate_one_char(issues: list[ConfigIssue], name: str,
                       value: object) -> None
```

Validate one optional one-character string.

<a id="tableio.config_data_validate._validate_nonempty_str"></a>

#### \_validate\_nonempty\_str

```python
def _validate_nonempty_str(issues: list[ConfigIssue], name: str,
                           value: object) -> None
```

Validate one optional non-empty string.

<a id="tableio.config_data_validate._validate_top_values"></a>

#### \_validate\_top\_values

```python
def _validate_top_values(config: ConfigData, specs: dict[str, ConfigSpec],
                         issues: list[ConfigIssue]) -> None
```

Validate top-level configuration values.

<a id="tableio.config_data_validate._validate_csv"></a>

#### \_validate\_csv

```python
def _validate_csv(config: ConfigData, specs: dict[str, ConfigSpec],
                  issues: list[ConfigIssue]) -> None
```

Validate CSV-specific configuration values.

<a id="tableio.config_data_validate._validate_html"></a>

#### \_validate\_html

```python
def _validate_html(config: ConfigData, issues: list[ConfigIssue]) -> None
```

Validate HTML-specific configuration values.

<a id="tableio.config_data_validate._validate_latex"></a>

#### \_validate\_latex

```python
def _validate_latex(config: ConfigData, specs: dict[str, ConfigSpec],
                    issues: list[ConfigIssue]) -> None
```

Validate LaTeX-specific configuration values.

<a id="tableio.config_data_validate._match_caps"></a>

#### \_match\_caps

```python
def _match_caps(capabilities: Optional[Capabilities],
                file_access: Optional[FileAccess],
                issues: list[ConfigIssue]) -> Optional[Capabilities]
```

Return capabilities to use when matching registered backends.

<a id="tableio.config_data_validate._backend_can_be_checked"></a>

#### \_backend\_can\_be\_checked

```python
def _backend_can_be_checked(config: ConfigData,
                            specs: dict[str, ConfigSpec]) -> bool
```

Return true if backend names are well enough formed to check.

<a id="tableio.config_data_validate._impl_choices"></a>

#### \_impl\_choices

```python
def _impl_choices(format_name: str) -> tuple[str, ...]
```

Return implementation choices for one registered format.

<a id="tableio.config_data_validate._impl_matches_format"></a>

#### \_impl\_matches\_format

```python
def _impl_matches_format(format_name: str, implementation: str) -> bool
```

Return true if an implementation belongs to a format.

<a id="tableio.config_data_validate._validate_impl_for_format"></a>

#### \_validate\_impl\_for\_format

```python
def _validate_impl_for_format(config: ConfigData, specs: dict[str, ConfigSpec],
                              issues: list[ConfigIssue]) -> None
```

Validate implementation choices that depend on the format name.

<a id="tableio.config_data_validate._validate_backend"></a>

#### \_validate\_backend

```python
def _validate_backend(config: ConfigData, specs: dict[str, ConfigSpec],
                      capabilities: Optional[Capabilities],
                      file_access: Optional[FileAccess],
                      issues: list[ConfigIssue]) -> None
```

Validate registered backend selection and capability matching.

<a id="tableio.config_data_validate.tio_config_validate"></a>

#### tio\_config\_validate

```python
def tio_config_validate(config: ConfigData,
                        capabilities: Optional[Capabilities] = None,
                        file_access: Optional[FileAccess] = None) -> None
```

Validate configuration values and selected combinations.

All configured values are validated, including values that would be
ignored by the selected backend. Irrelevant but well-formed parameters
are valid. For example, CSV values may be present while ``format_name``
selects an Excel backend, but invalid CSV values are still validation
errors.

**Arguments**:

- `config` - Configuration data to validate.
- `capabilities` - Optional runtime capabilities used for matching.
- `file_access` - Optional runtime file access used for consistency checks.

**Raises**:

- `ConfigError` - The configuration contains invalid values, unknown
  format or implementation names, or a selected backend that cannot
  fulfill the requested capabilities or file access.

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

<a id="tableio.tableio.TableIO.ImplMetaForWrite.borders"></a>

#### borders

The normalized borders of the table.

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
def write_table_listdata(
        data: ListDataSeq[CellT],
        filtered_data_range: bool = False,
        box: Optional[Box] = None,
        border_style: TableBorderStyle = TableBorderStyle.NONE) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when specifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The list data to write.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.
- `border_style` - The border style to apply to the written table.

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
def write_table_fmtlistdata(
        data: FmtListData,
        filtered_data_range: bool = False,
        box: Optional[Box] = None,
        border_style: TableBorderStyle = TableBorderStyle.NONE) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when specifying a box: It is not allowed to write a
table that partly overwrites an existing table.

**Arguments**:

- `data` - The list data to write.
- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.
- `box` - The box to write the data into. If box.bottom or box.right is
  not None, the data must fill the box.
- `border_style` - The border style to apply to the written table.

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
def write_table_dictdata(
        data: DictDataMap[CellT],
        column_order: list[str],
        first_row_format: Optional[Fmt] = None,
        missing_ok: bool = False,
        extra_ok: bool = False,
        filtered_data_range: bool = False,
        box: Optional[Box] = None,
        border_style: TableBorderStyle = TableBorderStyle.NONE) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when specifying a box: It is not allowed to write a
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
- `border_style` - The border style to apply to the written table.

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
def write_table_fmtdictdata(
        data: FmtDictData,
        column_order: list[str],
        first_row_format: Optional[Fmt] = None,
        missing_ok: bool = False,
        extra_ok: bool = False,
        filtered_data_range: bool = False,
        box: Optional[Box] = None,
        border_style: TableBorderStyle = TableBorderStyle.NONE) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
If a box is provided the data will be written into the box.
The data must fit into the box.
Notice when specifying a box: It is not allowed to write a
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
- `border_style` - The border style to apply to the written table.

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

<a id="tableio.tableio.TableIO._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

End the state of the file.

<a id="tableio.tableio.TableIO._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

<a id="tableio.tableio.TableIO._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

<a id="tableio.tableio.TableIO._check_listdimensions"></a>

#### \_check\_listdimensions

```python
def _check_listdimensions(data: ListDataSeq[CellT],
                          box: Optional[Box] = None,
                          is_table: bool = True) -> None
```

Check the dimensions of the list data.

**Arguments**:

- `data` - The list data to check.
- `box` - The box to check the data into.

**Raises**:

- `ValueError` - If the data does not have the same number of columns in
  each row.
- `ValueError` - If the data does not fit into the box.
- `ValueError` - If the data is not at least 2 cells in size.

<a id="tableio.tableio.TableIO._value_area"></a>

#### \_value\_area

```python
def _value_area(value: Value | ListDataSeq[Value]) -> ListData[Value]
```

Return one scalar or rectangular value pattern as a list grid.

<a id="tableio.tableio.TableIO._check_dictdimensions"></a>

#### \_check\_dictdimensions

```python
def _check_dictdimensions(data: DictDataMap[CellT],
                          box: Optional[Box] = None) -> None
```

Check the dimensions of the dict data.

**Arguments**:

- `data` - The dict data to check.
- `box` - The box to check the data into.

**Raises**:

- `ValueError` - If the data does not fit into the box.
- `ValueError` - If the data is not at least 2 cells in size.

<a id="tableio.tableio.TableIO._check_box_write"></a>

#### \_check\_box\_write

```python
def _check_box_write(box: Optional[Box]) -> Optional[Box]
```

Check if the box is OK to use for writing.

**Arguments**:

- `box` - The box to check.

**Raises**:

- `CapabilityNotSupported` - If writing to a box is unsupported and
  strict.

**Returns**:

  The box if it is supported.
  None if it is not supported and ignored.

<a id="tableio.tableio.TableIO._check_box_read"></a>

#### \_check\_box\_read

```python
def _check_box_read(box: Optional[Box]) -> Optional[Box]
```

Check if the box is OK to use for reading.

**Arguments**:

- `box` - The box to check.

**Raises**:

- `CapabilityNotSupported` - If reading from a box is unsupported and
  strict.

**Returns**:

  The box if it is supported.
  None if it is not supported and ignored.

<a id="tableio.tableio.TableIO._check_box_impl"></a>

#### \_check\_box\_impl

```python
@staticmethod
def _check_box_impl(box: Optional[Box], cap: SingleCapability,
                    action: str) -> Optional[Box]
```

Check if the box is OK to use for the given capability.

**Arguments**:

- `box` - The box to check.
- `cap` - The capability to check.
- `action` - The action the box is requested for.

**Raises**:

- `CapabilityNotSupported` - If the box is not supported and strict.

**Returns**:

  The box if it is supported.
  None if it is not supported and ignored.

<a id="tableio.tableio.TableIO._check_filtered_data_range"></a>

#### \_check\_filtered\_data\_range

```python
def _check_filtered_data_range(filtered_data_range: bool) -> bool
```

Check if the filtered data range is supported.

**Arguments**:

- `filtered_data_range` - If True, the data written will be
  marked as a data range that can be filtered.

**Returns**:

  True if the filtered data range is requested and supported.
  False if the filtered data range is not requested.
  False if the filtered data range is not supported and ignored.

**Raises**:

- `CapabilityNotSupported` - If writing a filtered data range is not
  supported and strict.

<a id="tableio.tableio.TableIO._check_border_style"></a>

#### \_check\_border\_style

```python
def _check_border_style(border_style: TableBorderStyle) -> BorderHelper
```

Check if the requested table border style is supported.

<a id="tableio.tableio.TableIO._write_heading"></a>

#### \_write\_heading

```python
def _write_heading(heading: str, level: int) -> Position
```

Write a heading to the file.

Write a heading to the file. Headings are a line between tables.
For example in CSV format the heading has an empty line before and
after, and it starts with one or more '#' characters.
Do not confuse the heading with the first row of a table,
with the names of the columns.

**Arguments**:

- `heading` - The heading text to write.
- `level` - The level of the heading. 1 = highest, 3 = lowest.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO._write_table_listdata"></a>

#### \_write\_table\_listdata

```python
def _write_table_listdata(data: ListDataSeq[CellT],
                          impl_meta: ImplMetaForWrite) -> Position
```

Write a table of list data to the file.

**Arguments**:

- `data` - The list data to write.
- `impl_meta` - The meta data for the table write operation,
  passed to the implementation class.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO._write_table_fmtlistdata"></a>

#### \_write\_table\_fmtlistdata

```python
def _write_table_fmtlistdata(data: FmtListData,
                             impl_meta: ImplMetaForWrite) -> Position
```

Write a table of list data to the file.

**Arguments**:

- `data` - The list data to write.
- `impl_meta` - The meta data for the table write operation,
  passed to the implementation class.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO._write_table_dictdata"></a>

#### \_write\_table\_dictdata

```python
def _write_table_dictdata(data: DictDataMap[CellT],
                          impl_meta: ImplMetaForDictWrite) -> Position
```

Write a table of dict data to the file.

**Arguments**:

- `data` - The dict data to write.
- `impl_meta` - The meta data for the dict table write operation,
  passed to the implementation class.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO._write_table_fmtdictdata"></a>

#### \_write\_table\_fmtdictdata

```python
def _write_table_fmtdictdata(data: FmtDictData,
                             impl_meta: ImplMetaForDictWrite) -> Position
```

Write a table of dict data to the file.

**Arguments**:

- `data` - The dict data to write.
- `impl_meta` - The meta data for the dict table write operation,
  passed to the implementation class.

**Returns**:

  The position of the last cell written. Position is in the
  current sheet.

<a id="tableio.tableio.TableIO._read_table_listdata"></a>

#### \_read\_table\_listdata

```python
def _read_table_listdata(
        box: Optional[Box] = None) -> ReadResult[ListData[Value]]
```

Read a table of list data from the file.

Must be implemented by derived classes.
If a box is provided the data will be read from the box, and the
reading is restricted to the box.
Anything found in the leftmost column that does form a table of at
least 2 cells in size is considered to be a heading and is returned
as a list of headings.

**Arguments**:

- `box` - The box to read the data from.

**Returns**:

  The data read from the table and the headings before the table.

<a id="tableio.tableio.TableIO._read_table_dictdata"></a>

#### \_read\_table\_dictdata

```python
def _read_table_dictdata(
        box: Optional[Box] = None) -> ReadResult[DictData[Value]]
```

Read a table of dict data from the file.

Must be implemented by derived classes.
If a box is provided the data will be read from the box, and the
reading is restricted to the box.
Anything found in the leftmost column that does form a table of at
least 2 cells in size is considered to be a heading and is returned
as a list of headings.

**Arguments**:

- `box` - The box to read the data from.

**Returns**:

  The data read from the table and the headings before the table.

<a id="tableio.tableio.TableIO._file_exists_check"></a>

#### \_file\_exists\_check

```python
def _file_exists_check() -> None
```

Check if the file exists.

If the file exists and the file access is CREATE, the
file_exists_callback is called to decide if the file can be
overwritten.
If file access is READ or UPDATE, the file must exist.

<a id="tableio.tableio.TableIO._check_file_is_writable"></a>

#### \_check\_file\_is\_writable

```python
def _check_file_is_writable() -> None
```

Raise if the file access mode does not allow writing.

<a id="tableio.tableio.TableIO._list_sheets"></a>

#### \_list\_sheets

```python
def _list_sheets() -> list[str]
```

List the sheets in the file.

**Returns**:

  A list of the sheet names. Sheet names are case preserving,
  but compared case insensitively.

<a id="tableio.tableio.TableIO._select_sheet"></a>

#### \_select\_sheet

```python
def _select_sheet(sheet_name: str, create: bool = False) -> None
```

Select a sheet in the file.

**Arguments**:

- `sheet_name` - The name of the sheet to select.
- `create` - If True, create the sheet if it does not exist.

**Raises**:

- `KeyError` - If the sheet name is not found and create is False.
- `io.UnsupportedOperation` - If the file is opened for reading,
  and create is True, and the sheet does
  not exist.

<a id="tableio.tableio.TableIO._current_sheet_name"></a>

#### \_current\_sheet\_name

```python
def _current_sheet_name() -> str
```

Return the name of the current sheet.

**Returns**:

  The name of the current sheet. Sheet names are case preserving,
  but compared case insensitively.

<a id="tableio.tableio.TableIO._find_value"></a>

#### \_find\_value

```python
def _find_value(find_value: ListData[Value],
                type_conversion: bool = True,
                box: Optional[Box] = None) -> Optional[Box]
```

Backend hook for find_value().

<a id="tableio.tableio.TableIO._read_cells"></a>

#### \_read\_cells

```python
def _read_cells(box: Box) -> ListData[Value]
```

Backend hook for read_cells().

<a id="tableio.tableio.TableIO._write_cells"></a>

#### \_write\_cells

```python
def _write_cells(data: ListDataSeq[CellT], box: Box) -> None
```

Backend hook for write_cells().

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

<a id="tableio.tableio_ods_odfdo._manifest_xml_without_configuration_entries"></a>

#### \_manifest\_xml\_without\_configuration\_entries

```python
def _manifest_xml_without_configuration_entries(data: bytes) -> bytes
```

Return manifest XML without unused Configurations2 file entries.

<a id="tableio.tableio_ods_odfdo._referenced_style_names"></a>

#### \_referenced\_style\_names

```python
def _referenced_style_names(root: ET.Element) -> set[str]
```

Return the set of style names referenced from one XML tree.

<a id="tableio.tableio_ods_odfdo._content_xml_without_unused_styles"></a>

#### \_content\_xml\_without\_unused\_styles

```python
def _content_xml_without_unused_styles(data: bytes) -> bytes
```

Return content XML with unused automatic styles removed.

<a id="tableio.tableio_ods_odfdo._styles_xml_with_required_defaults"></a>

#### \_styles\_xml\_with\_required\_defaults

```python
def _styles_xml_with_required_defaults(data: bytes) -> bytes
```

Return styles XML with default table and table-row styles added.

<a id="tableio.tableio_ods_odfdo._rewrite_saved_document"></a>

#### \_rewrite\_saved\_document

```python
def _rewrite_saved_document(file_name: Path) -> None
```

Rewrite one saved ODS archive to remove validator complaints.

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

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._checked_lang"></a>

#### \_checked\_lang

```python
@staticmethod
def _checked_lang(lang: str) -> str
```

Validate one document language string.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._split_rfc3066_language"></a>

#### \_split\_rfc3066\_language

```python
@staticmethod
def _split_rfc3066_language(lang: str) -> tuple[str, str]
```

Split one validated RFC3066 language string.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_document_language"></a>

#### \_set\_document\_language

```python
def _set_document_language(document: Document) -> None
```

Set the ODS metadata and default cell language.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

Finalize in-memory state before closing.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the ODS document to disk when the file is writable.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._close"></a>

#### \_close

```python
def _close() -> None
```

Release document references.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._table_name_map"></a>

#### \_table\_name\_map

```python
def _table_name_map() -> dict[str, Table]
```

Return the document tables indexed case-insensitively.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._list_sheets"></a>

#### \_list\_sheets

```python
def _list_sheets() -> list[str]
```

List the sheets in the document.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._select_sheet"></a>

#### \_select\_sheet

```python
def _select_sheet(sheet_name: str, create: bool = False) -> None
```

Select one document sheet, optionally creating it.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._current_sheet_name"></a>

#### \_current\_sheet\_name

```python
def _current_sheet_name() -> str
```

Return the name of the selected sheet.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._read_sheet"></a>

#### \_read\_sheet

```python
def _read_sheet() -> object
```

Return the readable ODS table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_sheet"></a>

#### \_write\_sheet

```python
def _write_sheet() -> object
```

Return the writable ODS table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._spreadsheet_body"></a>

#### \_spreadsheet\_body

```python
def _spreadsheet_body() -> Spreadsheet
```

Return the spreadsheet body of the open ODS document.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_container"></a>

#### \_database\_range\_container

```python
def _database_range_container() -> Element
```

Return the container for ODS database ranges.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_ranges"></a>

#### \_database\_ranges

```python
def _database_ranges() -> list[Element]
```

Return the ODS database range elements.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._quoted_table_name"></a>

#### \_quoted\_table\_name

```python
@staticmethod
def _quoted_table_name(table_name: str) -> str
```

Return a table name formatted for an ODF range address.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_address"></a>

#### \_database\_range\_address

```python
@classmethod
def _database_range_address(cls, table_name: str, bounds: tuple[int, int, int,
                                                                int]) -> str
```

Return one ODS database range address.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._split_range_endpoint"></a>

#### \_split\_range\_endpoint

```python
@staticmethod
def _split_range_endpoint(endpoint: str) -> tuple[str, str]
```

Split one table-qualified ODF cell endpoint.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_ref_to_position"></a>

#### \_cell\_ref\_to\_position

```python
@staticmethod
def _cell_ref_to_position(cell_ref: str) -> tuple[int, int]
```

Convert one A1 cell reference to zero-based coordinates.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._endpoint_position"></a>

#### \_endpoint\_position

```python
@classmethod
def _endpoint_position(cls, endpoint: str) -> tuple[str, int, int]
```

Return table name and coordinates for one range endpoint.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._database_range_bounds"></a>

#### \_database\_range\_bounds

```python
@classmethod
def _database_range_bounds(
        cls, database_range: Element) -> tuple[str, tuple[int, int, int, int]]
```

Return table name and bounds for one ODS database range.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._write_value_to_sheet"></a>

#### \_write\_value\_to\_sheet

```python
def _write_value_to_sheet(sheet: object, row: int, column: int,
                          value: object) -> None
```

Write one value to one ODS cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_cell_format"></a>

#### \_set\_cell\_format

```python
def _set_cell_format(sheet: object, row: int, column: int,
                     fmt: Optional[Fmt]) -> None
```

Apply cell formatting to one ODS cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_cell_borders"></a>

#### \_set\_cell\_borders

```python
def _set_cell_borders(sheet: object, row: int, column: int,
                      borders: CellBorder) -> None
```

Apply normalized borders to one ODS cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._apply_heading_style"></a>

#### \_apply\_heading\_style

```python
def _apply_heading_style(row: int, column: int, level: int) -> None
```

Apply the heading style to one ODS cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._last_used_row"></a>

#### \_last\_used\_row

```python
def _last_used_row(sheet: object) -> int
```

Return the last used row index on one ODS table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._last_used_column"></a>

#### \_last\_used\_column

```python
def _last_used_column(sheet: object) -> int
```

Return the last used column index on one ODS table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(sheet: object, row: int, column: int) -> Value
```

Return one ODS cell as a public Value.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._filtered_range_infos"></a>

#### \_filtered\_range\_infos

```python
def _filtered_range_infos() -> list[tuple[str, tuple[int, int, int, int]]]
```

Return filtered ranges for the active table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._delete_filtered_range"></a>

#### \_delete\_filtered\_range

```python
def _delete_filtered_range(name: str) -> None
```

Delete one filtered range by name.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._add_filtered_range"></a>

#### \_add\_filtered\_range

```python
def _add_filtered_range(bounds: tuple[int, int, int, int], name: str) -> None
```

Create one filtered database range for the active table.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_width_string"></a>

#### \_column\_width\_string

```python
@staticmethod
def _column_width_string(width: float) -> str
```

Return the ODS column width string for one target width.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_width_from_text"></a>

#### \_column\_width\_from\_text

```python
@classmethod
def _column_width_from_text(cls, width: str) -> Optional[float]
```

Parse one ODS column width string to the internal width unit.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._current_column_width"></a>

#### \_current\_column\_width

```python
def _current_column_width(column: int) -> Optional[float]
```

Return the current width of one ODS column.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._set_column_width_if_wider"></a>

#### \_set\_column\_width\_if\_wider

```python
def _set_column_width_if_wider(column: int, width: float) -> None
```

Widen one ODS column if the target width is larger.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._next_style_name"></a>

#### \_next\_style\_name

```python
def _next_style_name(prefix: str, family: str) -> str
```

Return a document-unique style name.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_state_key"></a>

#### \_cell\_style\_state\_key

```python
@staticmethod
def _cell_style_state_key(table: Table, row: int,
                          column: int) -> tuple[str, int, int]
```

Return the cache key for one touched ODS cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_state"></a>

#### \_cell\_style\_state

```python
def _cell_style_state(table: Table, row: int, column: int) -> CellStyleState
```

Return the current in-memory style state for one cell.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._apply_cell_style"></a>

#### \_apply\_cell\_style

```python
def _apply_cell_style(table: Table, row: int, column: int,
                      style: CellStyleState) -> None
```

Store and apply one composed ODS cell style.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._border_property_text"></a>

#### \_border\_property\_text

```python
@staticmethod
def _border_property_text(weight: BorderWeight) -> Optional[str]
```

Return one ODF border property value.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._cell_style_name"></a>

#### \_cell\_style\_name

```python
def _cell_style_name(fmt: Fmt,
                     font_size: Optional[int] = None,
                     borders: CellBorder = NO_BORDERS) -> str
```

Return the cached style name for one cell format combination.

<a id="tableio.tableio_ods_odfdo.TableIOOdsOdfdo._column_style_name"></a>

#### \_column\_style\_name

```python
def _column_style_name(width: float) -> str
```

Return the cached style name for one column width.

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

<a id="tableio.tableio_textbased.TableIOTextBased._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Avoid using this method directly.
Use derived class as a context manager instead, using a with statement.

<a id="tableio.tableio_textbased.TableIOTextBased._get_last_chars_written_impl"></a>

#### \_get\_last\_chars\_written\_impl

```python
def _get_last_chars_written_impl(num_chars: int, end_pos: int,
                                 rec_count: int) -> str
```

Get the last characters written to the file.

This is an implementation detail of the _get_last_chars_written method.
Keep the file pointer at the same position, i.e. (normally) at the
end of the file, so that we can continue writing after the last
characters.
Returns the last characters written to the file.
As utf-8 encode characters may be 1-6 bytes long, we need to read
more than num_chars characters to get the last characters.
(On Microsoft Windows the newline character is 2 bytes long CR/LF.)
If we start reading bytes that are in the middle of a character,
the utf-8 decoder will raise and exception. If we read 6 bytes for
every character we are guaranteed to get the last characters.
If the reading happens to be in the middle of a character it will
be a character before the characters we are looking for. If
decoding fails we will try again with a larger number of bytes,
to try to find a place in the file where some preceeding character
starts.

**Arguments**:

- `num_chars` - The number of characters to get.
- `end_pos` - The position at end of file to start reading from.
- `rec_count` - The number of recursive calls.

**Returns**:

  The last characters written to the file.

<a id="tableio.tableio_textbased.TableIOTextBased._get_last_chars_written"></a>

#### \_get\_last\_chars\_written

```python
def _get_last_chars_written(num_chars: int) -> str
```

Get the last characters written to the file.

Keep the file pointer at the same position, i.e. at the end of the
file, so that we can continue writing after the last characters.
Returns the last characters written to the file.

<a id="tableio.tableio_textbased.TableIOTextBased._ensure_empty_line_before"></a>

#### \_ensure\_empty\_line\_before

```python
def _ensure_empty_line_before() -> int
```

Ensure an empty line before the write position.

If we are at the beginning of the file do nothing.
If we have an empty line before the current position do nothing.
Otherwise insert an empty line before the current position.
Returns the number of new lines inserted.

<a id="tableio.tableio_excel_pylightxl"></a>

# tableio.tableio\_excel\_pylightxl

TableIO reader/writer class for Excel files using pylightxl.

<a id="tableio.tableio_excel_pylightxl._WorksheetLike"></a>

## \_WorksheetLike Objects

```python
class _WorksheetLike(Protocol)
```

Typed subset of the pylightxl worksheet API used here.

<a id="tableio.tableio_excel_pylightxl._WorksheetLike._calc_size"></a>

#### \_calc\_size

```python
def _calc_size() -> None
```

Recalculate cached worksheet size information.

<a id="tableio.tableio_excel_pylightxl._WorksheetLike.update_address"></a>

#### update\_address

```python
def update_address(address: str, val: object) -> None
```

Update one worksheet cell by Excel address.

<a id="tableio.tableio_excel_pylightxl._worksheet_names"></a>

#### \_worksheet\_names

```python
def _worksheet_names(database: Database) -> list[str]
```

Return the workbook sheet names with a concrete static type.

<a id="tableio.tableio_excel_pylightxl._database_worksheet"></a>

#### \_database\_worksheet

```python
def _database_worksheet(database: Database, sheet_name: str) -> _WorksheetLike
```

Return one worksheet from the database with a concrete static type.

<a id="tableio.tableio_excel_pylightxl._worksheet_cells"></a>

#### \_worksheet\_cells

```python
def _worksheet_cells(
        worksheet: _WorksheetLike) -> dict[str, dict[str, object]]
```

Return the internal worksheet cell dictionary.

<a id="tableio.tableio_excel_pylightxl._recalculate_worksheet_size"></a>

#### \_recalculate\_worksheet\_size

```python
def _recalculate_worksheet_size(worksheet: _WorksheetLike) -> None
```

Recalculate the cached worksheet size after cell deletion.

<a id="tableio.tableio_excel_pylightxl._worksheet_id_attr"></a>

#### \_worksheet\_id\_attr

```python
def _worksheet_id_attr(tag_sheet: ET.Element) -> Optional[str]
```

Return the relationship id stored on one workbook sheet element.

<a id="tableio.tableio_excel_pylightxl._sheet_xml_targets"></a>

#### \_sheet\_xml\_targets

```python
def _sheet_xml_targets(file_name: str) -> dict[str, tuple[int, str]]
```

Return sheet order and XML target path for each workbook sheet.

<a id="tableio.tableio_excel_pylightxl._xml_text"></a>

#### \_xml\_text

```python
def _xml_text(element: Optional[ET.Element]) -> str
```

Return the text of one XML element, defaulting to the empty string.

<a id="tableio.tableio_excel_pylightxl._inline_string_text"></a>

#### \_inline\_string\_text

```python
def _inline_string_text(cell: ET.Element) -> str
```

Return the concatenated text of one inline string cell.

<a id="tableio.tableio_excel_pylightxl._number_from_cell_text"></a>

#### \_number\_from\_cell\_text

```python
def _number_from_cell_text(raw_value: str) -> object
```

Return one numeric cell text as int, float or the original string.

<a id="tableio.tableio_excel_pylightxl._xml_bytes"></a>

#### \_xml\_bytes

```python
def _xml_bytes(root: ET.Element) -> bytes
```

Return one XML element serialized as UTF-8 bytes.

<a id="tableio.tableio_excel_pylightxl._datetime_from_excel_number"></a>

#### \_datetime\_from\_excel\_number

```python
def _datetime_from_excel_number(number: int | float) -> datetime
```

Return one Excel serial number converted to a Python datetime.

<a id="tableio.tableio_excel_pylightxl._datetime_to_excel_number"></a>

#### \_datetime\_to\_excel\_number

```python
def _datetime_to_excel_number(value: datetime) -> float
```

Return one Python datetime converted to an Excel serial number.

<a id="tableio.tableio_excel_pylightxl._sheet_data_from_xml"></a>

#### \_sheet\_data\_from\_xml

```python
def _sheet_data_from_xml(
        xml_data: bytes, shared_strings: dict[int, str],
        styles: dict[int, str]) -> dict[str, dict[str, object]]
```

Return one worksheet cell dictionary parsed from worksheet XML.

<a id="tableio.tableio_excel_pylightxl._load_named_ranges"></a>

#### \_load\_named\_ranges

```python
def _load_named_ranges(workbook_root: ET.Element, database: Database) -> None
```

Load workbook defined names into the pylightxl database.

<a id="tableio.tableio_excel_pylightxl._read_database"></a>

#### \_read\_database

```python
def _read_database(file_name: str) -> Database
```

Read one workbook with pylightxl plus workbook-namespace fixes.

<a id="tableio.tableio_excel_pylightxl._style_index_for_code"></a>

#### \_style\_index\_for\_code

```python
def _style_index_for_code(style_code: str) -> Optional[str]
```

Return the compact styles.xml xf index for one stored style code.

<a id="tableio.tableio_excel_pylightxl._styles_xml"></a>

#### \_styles\_xml

```python
def _styles_xml() -> bytes
```

Return a minimal styles.xml supporting date, time and datetime tags.

<a id="tableio.tableio_excel_pylightxl._theme_xml"></a>

#### \_theme\_xml

```python
def _theme_xml() -> bytes
```

Return the standard Excel theme XML.

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

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._initialize_sheet_style_codes"></a>

#### \_initialize\_sheet\_style\_codes

```python
def _initialize_sheet_style_codes() -> None
```

Load compact style metadata from the open database.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

Finalize in-memory state before closing.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the workbook to disk when the file is writable.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._close"></a>

#### \_close

```python
def _close() -> None
```

Release workbook references.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._temporary_workbook_path"></a>

#### \_temporary\_workbook\_path

```python
@staticmethod
def _temporary_workbook_path(source_path: Path) -> Path
```

Return a temporary workbook path that does not yet exist.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._invalid_placeholder_cell"></a>

#### \_invalid\_placeholder\_cell

```python
@staticmethod
def _invalid_placeholder_cell(cell: ET.Element) -> bool
```

Return whether one written cell is a pylightxl blank placeholder.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._normalize_written_bool_cell"></a>

#### \_normalize\_written\_bool\_cell

```python
@staticmethod
def _normalize_written_bool_cell(cell: ET.Element) -> bool
```

Convert one written True/False text cell into a real bool cell.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._rewrite_workbook_xml"></a>

#### \_rewrite\_workbook\_xml

```python
def _rewrite_workbook_xml(file_name: Path) -> None
```

Clean written worksheet XML and add required workbook metadata.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._content_types_with_required_parts"></a>

#### \_content\_types\_with\_required\_parts

```python
def _content_types_with_required_parts(data: bytes) -> bytes
```

Return content types XML updated with styles and theme parts.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._workbook_rels_with_required_parts"></a>

#### \_workbook\_rels\_with\_required\_parts

```python
def _workbook_rels_with_required_parts(data: bytes) -> bytes
```

Return workbook relations XML updated with styles and theme.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._entry_style_codes"></a>

#### \_entry\_style\_codes

```python
def _entry_style_codes(
        entry_name: str,
        sheet_targets: dict[str, tuple[int, str]]) -> dict[str, str]
```

Return the compact style codes for one worksheet archive entry.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._rewrite_row_xml"></a>

#### \_rewrite\_row\_xml

```python
def _rewrite_row_xml(row: ET.Element, style_codes: dict[str, str]) -> bool
```

Clean one row element and apply compact cell styles.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._worksheet_xml_for_output"></a>

#### \_worksheet\_xml\_for\_output

```python
def _worksheet_xml_for_output(
        entry_name: str, data: bytes,
        sheet_targets: dict[str, tuple[int, str]]) -> bytes
```

Return cleaned worksheet XML updated with compact style markers.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._current_style_codes"></a>

#### \_current\_style\_codes

```python
def _current_style_codes() -> dict[str, str]
```

Return the compact style map for the current sheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._list_sheets"></a>

#### \_list\_sheets

```python
def _list_sheets() -> list[str]
```

List the sheets in the workbook.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._select_sheet"></a>

#### \_select\_sheet

```python
def _select_sheet(sheet_name: str, create: bool = False) -> None
```

Select one workbook sheet, optionally creating it.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._current_sheet_name"></a>

#### \_current\_sheet\_name

```python
def _current_sheet_name() -> str
```

Return the name of the selected worksheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._read_sheet"></a>

#### \_read\_sheet

```python
def _read_sheet() -> object
```

Return the readable worksheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_sheet"></a>

#### \_write\_sheet

```python
def _write_sheet() -> object
```

Return the writable worksheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._write_value_to_sheet"></a>

#### \_write\_value\_to\_sheet

```python
def _write_value_to_sheet(sheet: object, row: int, column: int,
                          value: object) -> None
```

Write one value to one worksheet cell.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._set_cell_format"></a>

#### \_set\_cell\_format

```python
def _set_cell_format(sheet: object, row: int, column: int,
                     fmt: Optional[Fmt]) -> None
```

Ignore cell formatting because pylightxl cannot write it.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._apply_heading_style"></a>

#### \_apply\_heading\_style

```python
def _apply_heading_style(row: int, column: int, level: int) -> None
```

Ignore heading styling because pylightxl cannot write it.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._last_used_row"></a>

#### \_last\_used\_row

```python
def _last_used_row(sheet: object) -> int
```

Return the last used row index on a worksheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._last_used_column"></a>

#### \_last\_used\_column

```python
def _last_used_column(sheet: object) -> int
```

Return the last used column index on a worksheet.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(sheet: object, row: int, column: int) -> Value
```

Return one worksheet cell as a public Value.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._parse_typed_cell_value"></a>

#### \_parse\_typed\_cell\_value

```python
@classmethod
def _parse_typed_cell_value(cls, value: object, style_code: str) -> Value
```

Convert one stored pylightxl cell value to the public Value type.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._filtered_range_infos"></a>

#### \_filtered\_range\_infos

```python
def _filtered_range_infos() -> list[tuple[str, tuple[int, int, int, int]]]
```

Return no filtered ranges because pylightxl ignores them.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._delete_filtered_range"></a>

#### \_delete\_filtered\_range

```python
def _delete_filtered_range(name: str) -> None
```

Ignore filtered-range deletion because none are written.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._add_filtered_range"></a>

#### \_add\_filtered\_range

```python
def _add_filtered_range(bounds: tuple[int, int, int, int], name: str) -> None
```

Ignore filtered-range requests.

pylightxl cannot write Excel filtered ranges.

<a id="tableio.tableio_excel_pylightxl.TableIOExcelPylightxl._set_column_width_if_wider"></a>

#### \_set\_column\_width\_if\_wider

```python
def _set_column_width_if_wider(column: int, width: float) -> None
```

Ignore width updates because pylightxl cannot write them.

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

Excel CSV file type/dialect.

<a id="tableio.optional_args.CsvDialect.UNIX"></a>

#### UNIX

Unix CSV file type/dialect.

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

<a id="tableio.optional_args.OptionalArgsDict.csv_dialect"></a>

#### csv\_dialect

The type/dialect of CSV file to write. None for default type.

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

<a id="tableio.access_capability"></a>

# tableio.access\_capability

Helpers that connect file access modes to capability requests.

<a id="tableio.access_capability.NO_ERROR_OUTPUT"></a>

#### NO\_ERROR\_OUTPUT

Text stream used when helper errors should not be printed.

<a id="tableio.access_capability.InsufficientCapabilities"></a>

## InsufficientCapabilities Objects

```python
class InsufficientCapabilities(ValueError)
```

Raised when requested capabilities contradict requested file access.

Error raised when the caller supplies file access and explicit
Capabilities, but the requested capabilities do not include the capability
implied by that access mode. For example, READ requires can_read, CREATE
requires can_write, and UPDATE requires both.

<a id="tableio.access_capability.InsufficientCapabilities.__init__"></a>

#### \_\_init\_\_

```python
def __init__(message: str, capability_names: tuple[str, ...] = ()) -> None
```

Initialize the exception.

<a id="tableio.access_capability._raise_error"></a>

#### \_raise\_error

```python
def _raise_error(error_file: TextIO, error: Exception) -> NoReturn
```

Write an error message and raise the error.

<a id="tableio.access_capability._check_access_value"></a>

#### \_check\_access\_value

```python
def _check_access_value(file_access: FileAccess, error_file: TextIO) -> None
```

Raise if file access is not a supported FileAccess value.

<a id="tableio.access_capability._check_capabilities_value"></a>

#### \_check\_capabilities\_value

```python
def _check_capabilities_value(capabilities: Capabilities,
                              error_file: TextIO) -> None
```

Raise if capabilities is not a Capabilities object.

<a id="tableio.access_capability.access_capabilities"></a>

#### access\_capabilities

```python
def access_capabilities(file_access: FileAccess,
                        error_file: TextIO = NO_ERROR_OUTPUT) -> Capabilities
```

Return the capabilities implied by a file access mode.

**Arguments**:

- `file_access` - File access mode to convert to capability requirements.
- `error_file` - Text stream receiving error messages before exceptions.

**Raises**:

- `TypeError` - If file_access is not a FileAccess value.
- `ValueError` - If file_access is an unsupported FileAccess value.

**Returns**:

  Capabilities needed for the requested file access.

<a id="tableio.access_capability.add_access_capabilities"></a>

#### add\_access\_capabilities

```python
def add_access_capabilities(
        file_access: FileAccess,
        capabilities: Capabilities,
        error_file: TextIO = NO_ERROR_OUTPUT) -> Capabilities
```

Return capabilities with file access requirements added.

The original capabilities object is not mutated.

**Arguments**:

- `file_access` - File access mode to add capability requirements for.
- `capabilities` - Existing capability requirements to extend.
- `error_file` - Text stream receiving error messages before exceptions.

**Raises**:

- `TypeError` - If file_access or capabilities has an invalid type.
- `ValueError` - If file_access is an unsupported FileAccess value.

**Returns**:

  New Capabilities object including the file access requirements.

<a id="tableio.access_capability._missing_access_caps"></a>

#### \_missing\_access\_caps

```python
def _missing_access_caps(file_access: FileAccess,
                         capabilities: Capabilities) -> tuple[str, ...]
```

Return capability names missing for the requested access mode.

<a id="tableio.access_capability._access_error_message"></a>

#### \_access\_error\_message

```python
def _access_error_message(file_access: FileAccess) -> str
```

Return the error message for missing access capabilities.

<a id="tableio.access_capability.check_access_capabilities"></a>

#### check\_access\_capabilities

```python
def check_access_capabilities(file_access: FileAccess,
                              capabilities: Capabilities,
                              error_file: TextIO = NO_ERROR_OUTPUT) -> None
```

Raise if capabilities are not enough for requested access mode.

**Arguments**:

- `file_access` - File access mode to check capability requirements for.
- `capabilities` - Capability requirements to check.
- `error_file` - Text stream receiving error messages before exceptions.

**Raises**:

- `TypeError` - If file_access or capabilities has an invalid type.
- `ValueError` - If file_access is an unsupported FileAccess value.
- `InsufficientCapabilities` - If capabilities do not support file_access.

<a id="tableio.config_data"></a>

# tableio.config\_data

Configuration data for the tableio package.

<a id="tableio.config_data.CsvConfigData"></a>

## CsvConfigData Objects

```python
@dataclass
class CsvConfigData()
```

CSV-specific configuration values.

This class holds durable user choices that only have meaning for CSV
output. The values are allowed to be present even when another format is
selected; helper functions decide whether they are relevant for the
current TableIO backend. The class has no configuration-framework base
class, so adapter libraries may combine it with their own base classes.

<a id="tableio.config_data.CsvConfigData.dialect"></a>

#### dialect

The CSV dialect template to use, or ``None`` for backend default.

<a id="tableio.config_data.CsvConfigData.delimiter"></a>

#### delimiter

The CSV delimiter to use, or ``None`` for backend default.

<a id="tableio.config_data.CsvConfigData.quoting"></a>

#### quoting

The CSV quoting style to use, or ``None`` for backend default.

<a id="tableio.config_data.CsvConfigData.quotechar"></a>

#### quotechar

The CSV quote character to use, or ``None`` for backend default.

<a id="tableio.config_data.CsvConfigData.lineterminator"></a>

#### lineterminator

The CSV line terminator to use, or ``None`` for backend default.

<a id="tableio.config_data.CsvConfigData.escapechar"></a>

#### escapechar

The CSV escape character to use, or ``None`` for backend default.

<a id="tableio.config_data.HtmlConfigData"></a>

## HtmlConfigData Objects

```python
@dataclass
class HtmlConfigData()
```

HTML-specific configuration values.

The class has no configuration-framework base class, so adapter
libraries may combine it with their own base classes.

<a id="tableio.config_data.HtmlConfigData.css_file"></a>

#### css\_file

The CSS file path or URL to reference, or ``None`` for no CSS file.

<a id="tableio.config_data.LatexConfigData"></a>

## LatexConfigData Objects

```python
@dataclass
class LatexConfigData()
```

LaTeX-specific configuration values.

The class has no configuration-framework base class, so adapter
libraries may combine it with their own base classes.

<a id="tableio.config_data.LatexConfigData.document_class"></a>

#### document\_class

The LaTeX document class to use, or ``None`` for backend default.

<a id="tableio.config_data.LatexConfigData.preamble"></a>

#### preamble

Extra LaTeX preamble text, or ``None`` for backend default.

<a id="tableio.config_data.ConfigData"></a>

## ConfigData Objects

```python
@dataclass
class ConfigData()
```

Durable, framework-neutral TableIO configuration choices.

This class intentionally excludes runtime intent. File names, file access,
capabilities and callbacks are supplied to helper functions instead of
being stored as configuration values. The default format is Excel, and
format-specific nested sections default to ``None`` until a user or
application deliberately configures them.

The class has no configuration-framework base class, so adapter libraries
may combine it with their own base classes.

<a id="tableio.config_data.ConfigData.format_name"></a>

#### format\_name

The TableIO format name. Matching is case-insensitive.

<a id="tableio.config_data.ConfigData.implementation"></a>

#### implementation

The optional implementation pin, or ``None`` to choose best match.

<a id="tableio.config_data.ConfigData.character_encoding"></a>

#### character\_encoding

The text encoding to use, or ``None`` for backend default.

<a id="tableio.config_data.ConfigData.language"></a>

#### language

The document language value mapped to backend ``lang`` arguments.

<a id="tableio.config_data.ConfigData.title"></a>

#### title

The document title, or ``None`` for backend default.

<a id="tableio.config_data.ConfigData.paper_size"></a>

#### paper\_size

The document paper size, or ``None`` for backend default.

<a id="tableio.config_data.ConfigData.line_length"></a>

#### line\_length

The preferred text line length, or ``None`` for backend default.

<a id="tableio.config_data.ConfigData.table_max_line_length"></a>

#### table\_max\_line\_length

The preferred text table line length, or ``None`` for default.

<a id="tableio.config_data.ConfigData.table_alignment"></a>

#### table\_alignment

The preferred text table alignment, or ``None`` for default.

<a id="tableio.config_data.ConfigData.csv"></a>

#### csv

CSV-specific configuration values, or ``None`` when unset.

<a id="tableio.config_data.ConfigData.html"></a>

#### html

HTML-specific configuration values, or ``None`` when unset.

<a id="tableio.config_data.ConfigData.latex"></a>

#### latex

LaTeX-specific configuration values, or ``None`` when unset.

<a id="tableio.factory"></a>

# tableio.factory

Factory class for creating TableIO instances.

<a id="tableio.factory._the_factory"></a>

#### \_the\_factory

pylint: disable=invalid-name # noqa: E501

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

<a id="tableio.factory.FactoryFormatInfo.get_usage"></a>

#### get\_usage

```python
def get_usage(implementation_name: str) -> Descriptor
```

Get usage information for one implementation.

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

<a id="tableio.factory.TableIOFactory._correct_format_name"></a>

#### \_correct\_format\_name

```python
def _correct_format_name(format_name: str) -> str
```

Correct a registered format name to its stored case.

<a id="tableio.factory.TableIOFactory._format_info"></a>

#### \_format\_info

```python
def _format_info(format_name: str) -> FactoryFormatInfo
```

Get registered format information by case-insensitive name.

<a id="tableio.factory.TableIOFactory._select_implementation_name"></a>

#### \_select\_implementation\_name

```python
@staticmethod
def _select_implementation_name(format_info: FactoryFormatInfo,
                                implementation: Optional[str],
                                capabilities: Optional[Capabilities]) -> str
```

Select the implementation name matching the request.

<a id="tableio.factory.TableIOFactory.filter_args"></a>

#### filter\_args

```python
@staticmethod
def filter_args(args: OptionalArgs,
                format_name: str,
                implementation: Optional[str],
                capabilities: Optional[Capabilities] = None) -> OptionalArgs
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
- `implementation` - The implementation name to use. If implementation
  is specified as None, filtering is done for the
  implementation create() would use with a None value
  for the implementation parameter.
- `capabilities` - The capabilities to match. This is used to determine
  the implementation to use if implementation is None.

**Returns**:

  The filtered arguments.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name is not registered
  or the implementation name is not
  registered.
- `TableIOFactoryNoCapabilityMatch` - If the capabilities cannot be
  matched to the selected
  implementation.

<a id="tableio.factory.TableIOFactory.i_filter_args"></a>

#### i\_filter\_args

```python
def i_filter_args(args: OptionalArgs,
                  format_name: str,
                  implementation: Optional[str],
                  capabilities: Optional[Capabilities] = None) -> OptionalArgs
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
                                   empty_is_ok: bool = False,
                                   alphabetical: bool = True) -> list[str]
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
- `alphabetical` - If True, the implementations are returned in
  alphabetical order. If False, the implementations
  are returned with the strict matches first and the
  nonstrict matches last. Both strict and nonstrict
  matches are sorted by priority, from highest to
  lowest.

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
        empty_is_ok: bool = False,
        alphabetical: bool = True) -> list[str]
```

Internally get a list of registered implementations (deprecated).

.. deprecated:: 0.7.1
    Use :meth:`i_get_reg_impls` instead.

<a id="tableio.factory.TableIOFactory.i_get_reg_impls"></a>

#### i\_get\_reg\_impls

```python
def i_get_reg_impls(format_name: Optional[str] = None,
                    lower: bool = False,
                    upper: bool = False,
                    capabilities: Optional[Capabilities] = None,
                    empty_is_ok: bool = False,
                    alphabetical: bool = True) -> list[str]
```

Internally get a list of registered implementation names.

<a id="tableio.factory.TableIOFactory._implementation_matches"></a>

#### \_implementation\_matches

```python
def _implementation_matches(format_names: list[str],
                            capabilities: Optional[Capabilities],
                            empty_is_ok: bool) -> BestMatch
```

Get matching implementations for the requested format names.

<a id="tableio.factory.TableIOFactory._implementation_names"></a>

#### \_implementation\_names

```python
@staticmethod
def _implementation_names(best_match: BestMatch,
                          alphabetical: bool) -> list[str]
```

Get implementation names from best matches without duplicates.

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
def filter_args_tableio(
        args: OptionalArgs,
        format_name: str,
        implementation: Optional[str],
        capabilities: Optional[Capabilities] = None) -> OptionalArgs
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
- `implementation` - The implementation name to use. If implementation
  is specified as None, filtering is done for the
  implementation create() would use with a None value
  for the implementation parameter.
- `capabilities` - The capabilities to match. This is used to determine
  the implementation to use if implementation is None.

**Returns**:

  The filtered arguments.

**Raises**:

- `TableIOFactoryNoSuchError` - If the format_name or implementation
  name is not registered.
- `TableIOFactoryNoCapabilityMatch` - If the capabilities cannot be
  matched to the selected
  implementation.

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
                                 empty_is_ok: bool = False,
                                 alphabetical: bool = True) -> list[str]
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
- `alphabetical` - If True, the implementations are returned in
  alphabetical order. If False, the implementations
  are returned with the strict matches first and the
  nonstrict matches last. Both strict and nonstrict
  matches are sorted by priority, from highest to
  lowest.

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

<a id="tableio.value_type._validate_column_order"></a>

#### \_validate\_column\_order

```python
def _validate_column_order(column_order: list[str]) -> None
```

Raise if column_order is empty or contains duplicate names.

<a id="tableio.value_type._raise_empty_row_error"></a>

#### \_raise\_empty\_row\_error

```python
def _raise_empty_row_error(row_index: int) -> None
```

Raise the empty-row error with the row index in the message.

<a id="tableio.value_type._first_row_is_plain_dict_data"></a>

#### \_first\_row\_is\_plain\_dict\_data

```python
def _first_row_is_plain_dict_data(
    data: DictDataMap[Value] | DictDataMap[ValueFmt]
) -> TypeGuard[DictDataMap[Value]]
```

Return whether the first cell in the first row is a plain value.

<a id="tableio.value_type._first_row_is_formatted_dict_data"></a>

#### \_first\_row\_is\_formatted\_dict\_data

```python
def _first_row_is_formatted_dict_data(
    data: DictDataMap[Value] | DictDataMap[ValueFmt]
) -> TypeGuard[DictDataMap[ValueFmt]]
```

Return whether the first cell in the first row is formatted.

<a id="tableio.value_type._normalize_dict_data_with_missing_cell"></a>

#### \_normalize\_dict\_data\_with\_missing\_cell

```python
def _normalize_dict_data_with_missing_cell(
        data: DictDataMap[CellT], column_order: list[str], missing_ok: bool,
        extra_ok: bool, missing_cell: CellT) -> DictDataMap[CellT]
```

Normalize dict data using the provided missing-cell value.

<a id="tableio.value_type._normalize_dict_data_impl"></a>

#### \_normalize\_dict\_data\_impl

```python
def _normalize_dict_data_impl(
        data: DictDataMap[Value] | DictDataMap[ValueFmt],
        column_order: list[str],
        missing_ok: bool = False,
        extra_ok: bool = False) -> DictDataMap[Value] | DictDataMap[ValueFmt]
```

Normalize dict data for one concrete cell-kind input.

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

<a id="tableio.border_helper"></a>

# tableio.border\_helper

Helpers for working with normalized table borders.

<a id="tableio.border_helper.BorderWeight"></a>

## BorderWeight Objects

```python
class BorderWeight(IntEnum)
```

Semantic weight for one border edge.

<a id="tableio.border_helper.CellBorder"></a>

## CellBorder Objects

```python
class CellBorder(NamedTuple)
```

Border weights for the four edges of one cell.

<a id="tableio.border_helper.NO_BORDERS"></a>

#### NO\_BORDERS

The absence of borders on all four cell edges.

<a id="tableio.border_helper.CellStyleState"></a>

## CellStyleState Objects

```python
class CellStyleState(NamedTuple)
```

Combined cell formatting state used by style-caching backends.

<a id="tableio.border_helper.DEFAULT_CELL_STYLE"></a>

#### DEFAULT\_CELL\_STYLE

The default cell formatting state with no extra styling.

<a id="tableio.border_helper._BorderComponents"></a>

## \_BorderComponents Objects

```python
class _BorderComponents(NamedTuple)
```

Normalized border weights for one table style.

<a id="tableio.border_helper._thicker"></a>

#### \_thicker

```python
def _thicker(first: BorderWeight, second: BorderWeight) -> BorderWeight
```

Return the thicker of two border weights.

<a id="tableio.border_helper.BorderHelper"></a>

## BorderHelper Objects

```python
class BorderHelper()
```

Normalize one public table-border style for backend use.

<a id="tableio.border_helper.BorderHelper.__init__"></a>

#### \_\_init\_\_

```python
def __init__(border_style: TableBorderStyle, capabilities: Capabilities)
```

Initialize the normalized table-border helper.

<a id="tableio.border_helper.BorderHelper._checked_style"></a>

#### \_checked\_style

```python
@staticmethod
def _checked_style(border_style: TableBorderStyle,
                   capabilities: Capabilities) -> TableBorderStyle
```

Return the effective border style after capability handling.

<a id="tableio.border_helper.BorderHelper.has_borders"></a>

#### has\_borders

```python
def has_borders() -> bool
```

Return whether any border is active in this normalized style.

<a id="tableio.border_helper.BorderHelper._horizontal_boundary"></a>

#### \_horizontal\_boundary

```python
def _horizontal_boundary(boundary_index: int, row_count: int) -> BorderWeight
```

Return the weight of one horizontal table boundary.

<a id="tableio.border_helper.BorderHelper._vertical_boundary"></a>

#### \_vertical\_boundary

```python
def _vertical_boundary(boundary_index: int, column_count: int) -> BorderWeight
```

Return the weight of one vertical table boundary.

<a id="tableio.border_helper.BorderHelper.cell_border"></a>

#### cell\_border

```python
def cell_border(row_index: int, column_index: int, row_count: int,
                column_count: int) -> CellBorder
```

Return the four border edges for one cell in a table.

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

<a id="tableio.tableio_types.TableBorderStyle"></a>

## TableBorderStyle Objects

```python
class TableBorderStyle(IntEnum)
```

Border style of a table.

Used to describe the borders of a table. Borders are defined at the
table level, not at the cell level. A table may have borders on all
sides and also internally in the table. In the styles the words
'thin' and 'thick' describe the semantic weight of the borders; they
may be mapped to different physical border styles in the file format.
When several parts of one style affect the same cell edge, the
thickest weight is used. For example, if the separator below the
first row should be thick and inner lines should be thin, the cell
edge below the first row is thick.

<a id="tableio.tableio_types.TableBorderStyle.NONE"></a>

#### NONE

No borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_THIN"></a>

#### OUTER\_THIN

Thin border around the table. No inner borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_THICK"></a>

#### OUTER\_THICK

Thick border around the table. No inner borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THIN"></a>

#### OUTER\_FIRST\_ROW\_THIN

Thin border around the table and thin separator below the first row.

Thin lines on the outside of the table and under (the column names
on) the first row. No other inner borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK"></a>

#### OUTER\_FIRST\_ROW\_THICK

Thick border around the table and thick separator below the first row.

Thick lines on the outside of the table and under (the column names
on) the first row. No other inner borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_THICK_FIRST_ROW_THIN"></a>

#### OUTER\_THICK\_FIRST\_ROW\_THIN

Thick border around the table and thin separator below the first row.

Thick lines on the outside of the table and a thin line under (the
column names on) the first row. No other lines inside the table.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK_VERTICAL_THIN"></a>

#### OUTER\_FIRST\_ROW\_THICK\_VERTICAL\_THIN

Thick border around the table, thick separator below the first
row, and thin vertical inner borders.

Thick lines on the outside of the table and under (the column names
on) the first row. Thin vertical lines between the columns. No other
inner borders.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN"></a>

#### OUTER\_FIRST\_ROW\_THICK\_INNER\_THIN

Thick border around the table, thick separator below the first
row, and thin inner borders.

Thick lines on the outside of the table and under (the column names
on) the first row. All other inner cell borders are thin.

<a id="tableio.tableio_types.TableBorderStyle.OUTER_THICK_INNER_THIN"></a>

#### OUTER\_THICK\_INNER\_THIN

Thick border around the table and thin inner borders.

<a id="tableio.tableio_types.TableBorderStyle.ALL_THIN"></a>

#### ALL\_THIN

All cell borders in the table have thin lines.

<a id="tableio.tableio_types.TableBorderStyle.ALL_THICK"></a>

#### ALL\_THICK

All cell borders in the table have thick lines.

<a id="tableio.config_data_describe"></a>

# tableio.config\_data\_describe

Description metadata for framework-neutral TableIO configuration.

<a id="tableio.config_data_describe.ConfigSpec"></a>

## ConfigSpec Objects

```python
@dataclass
class ConfigSpec()
```

Documentation metadata for one configuration parameter.

Applications and configuration adapters can use these specifications to
build user-facing documentation without duplicating TableIO knowledge.

<a id="tableio.config_data_describe.ConfigSpec.name"></a>

#### name

The dotted configuration parameter name.

<a id="tableio.config_data_describe.ConfigSpec.description"></a>

#### description

The user-facing description of the configuration parameter.

<a id="tableio.config_data_describe.ConfigSpec.value_type"></a>

#### value\_type

The user-facing value type description.

<a id="tableio.config_data_describe.ConfigSpec.default_text"></a>

#### default\_text

The user-facing default value description, if there is one.

<a id="tableio.config_data_describe.ConfigSpec.choices"></a>

#### choices

Allowed values, if the value has a finite advertised choice set.

<a id="tableio.config_data_describe.ConfigSpec.relevant_formats"></a>

#### relevant\_formats

Formats where this parameter can affect the created backend.

<a id="tableio.config_data_describe.ConfigSpec.relevant_impls"></a>

#### relevant\_impls

Implementations where this parameter can affect the backend.

<a id="tableio.config_data_describe.ConfigSpec.optional_arg"></a>

#### optional\_arg

The TableIO optional argument name this parameter maps to.

<a id="tableio.config_data_describe._csv_dialect_choices"></a>

#### \_csv\_dialect\_choices

```python
def _csv_dialect_choices() -> tuple[str, ...]
```

Return advertised CSV dialect choices.

<a id="tableio.config_data_describe._table_alignment_choices"></a>

#### \_table\_alignment\_choices

```python
def _table_alignment_choices() -> tuple[str, ...]
```

Return advertised plain text table alignment choices.

<a id="tableio.config_data_describe._formats_for_arg"></a>

#### \_formats\_for\_arg

```python
def _formats_for_arg(optional_arg: str) -> tuple[str, ...]
```

Return registered formats that accept an optional argument.

<a id="tableio.config_data_describe._impls_for_arg"></a>

#### \_impls\_for\_arg

```python
def _impls_for_arg(optional_arg: str) -> tuple[str, ...]
```

Return registered implementations that accept an optional argument.

<a id="tableio.config_data_describe._arg_spec"></a>

#### \_arg\_spec

```python
def _arg_spec(spec: ConfigSpec) -> ConfigSpec
```

Build a config spec mapped to one TableIO optional argument.

<a id="tableio.config_data_describe.tio_config_specs"></a>

#### tio\_config\_specs

```python
def tio_config_specs() -> dict[str, ConfigSpec]
```

Return documentation metadata for configuration parameters.

**Returns**:

  A mapping from dotted parameter names to structured specifications.

<a id="tableio.config_data_describe.tio_config_descriptions"></a>

#### tio\_config\_descriptions

```python
def tio_config_descriptions() -> dict[str, str]
```

Return descriptions for configuration parameters.

**Returns**:

  A mapping from dotted parameter names to description strings.

<a id="tableio.config_data_describe.tio_config_describe"></a>

#### tio\_config\_describe

```python
def tio_config_describe(name: str) -> str
```

Return the description for one configuration parameter.

**Arguments**:

- `name` - Dotted configuration parameter name.

**Returns**:

  The user-facing description string.

**Raises**:

- `KeyError` - The configuration parameter name is unknown.

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

<a id="tableio.capability.Capabilities.can_write_borders"></a>

#### can\_write\_borders

The writer class can write borders to the table.

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

<a id="tableio.tableio_excel_xlsxwriter._FormatKey"></a>

## \_FormatKey Objects

```python
class _FormatKey(NamedTuple)
```

Cache key for one XlsxWriter format object.

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

<a id="tableio.tableio_excel_xlsxwriter._SheetState"></a>

## \_SheetState Objects

```python
@dataclass
class _SheetState()
```

In-memory state for one XlsxWriter worksheet.

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

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

Finalize in-memory state before closing.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the workbook to disk.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._close"></a>

#### \_close

```python
def _close() -> None
```

Release workbook and worksheet references.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._create_sheet_state"></a>

#### \_create\_sheet\_state

```python
def _create_sheet_state(sheet_name: str) -> _SheetState
```

Create and register one worksheet state.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._current_sheet_state"></a>

#### \_current\_sheet\_state

```python
def _current_sheet_state() -> _SheetState
```

Return the selected worksheet state.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._list_sheets"></a>

#### \_list\_sheets

```python
def _list_sheets() -> list[str]
```

List the sheets in the workbook.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._select_sheet"></a>

#### \_select\_sheet

```python
def _select_sheet(sheet_name: str, create: bool = False) -> None
```

Select one workbook sheet, optionally creating it.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._current_sheet_name"></a>

#### \_current\_sheet\_name

```python
def _current_sheet_name() -> str
```

Return the name of the selected worksheet.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_sheet"></a>

#### \_read\_sheet

```python
def _read_sheet() -> object
```

Return the in-memory readable worksheet state.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_sheet"></a>

#### \_write\_sheet

```python
def _write_sheet() -> object
```

Return the in-memory writable worksheet state.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_value_to_sheet"></a>

#### \_write\_value\_to\_sheet

```python
def _write_value_to_sheet(sheet: object, row: int, column: int,
                          value: object) -> None
```

Write one value to one worksheet cell.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_cell_format"></a>

#### \_set\_cell\_format

```python
def _set_cell_format(sheet: object, row: int, column: int,
                     fmt: Optional[Fmt]) -> None
```

Apply cell formatting to one worksheet cell.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._apply_heading_style"></a>

#### \_apply\_heading\_style

```python
def _apply_heading_style(row: int, column: int, level: int) -> None
```

Apply the heading style to one worksheet cell.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._last_used_row"></a>

#### \_last\_used\_row

```python
def _last_used_row(sheet: object) -> int
```

Return the last used row index on a worksheet.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._last_used_column"></a>

#### \_last\_used\_column

```python
def _last_used_column(sheet: object) -> int
```

Return the last used column index on a worksheet.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(sheet: object, row: int, column: int) -> Value
```

Return one worksheet cell as a public Value.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._filtered_range_infos"></a>

#### \_filtered\_range\_infos

```python
def _filtered_range_infos() -> list[tuple[str, tuple[int, int, int, int]]]
```

Return the worksheet filtered ranges.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._delete_filtered_range"></a>

#### \_delete\_filtered\_range

```python
def _delete_filtered_range(name: str) -> None
```

Delete one worksheet filtered range.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._add_filtered_range"></a>

#### \_add\_filtered\_range

```python
def _add_filtered_range(bounds: tuple[int, int, int, int], name: str) -> None
```

Add one Excel table for a filtered data range.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_column_width_if_wider"></a>

#### \_set\_column\_width\_if\_wider

```python
def _set_column_width_if_wider(column: int, width: float) -> None
```

Widen one worksheet column if the target width is larger.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._filter_range_name_in_use"></a>

#### \_filter\_range\_name\_in\_use

```python
def _filter_range_name_in_use(name: str) -> bool
```

Return whether one filter range name is already used.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_table_listdata"></a>

#### \_read\_table\_listdata

```python
def _read_table_listdata(
        box: Optional[object] = None) -> ReadResult[list[list[Value]]]
```

Reject list-data reads for the write-only backend.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._read_table_dictdata"></a>

#### \_read\_table\_dictdata

```python
def _read_table_dictdata(
        box: Optional[object] = None) -> ReadResult[list[dict[str, Value]]]
```

Reject dict-data reads for the write-only backend.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._cell_fmt"></a>

#### \_cell\_fmt

```python
def _cell_fmt(row: int, column: int) -> Optional[Fmt]
```

Return the public format stored for one cell.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._remove_table_metadata"></a>

#### \_remove\_table\_metadata

```python
@classmethod
def _remove_table_metadata(cls, sheet: _SheetState, bounds: tuple[int, int,
                                                                  int, int],
                           name: str) -> None
```

Remove one pending XlsxWriter table from worksheet internals.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._write_actual_cell"></a>

#### \_write\_actual\_cell

```python
def _write_actual_cell(sheet: _SheetState, row: int, column: int) -> None
```

Write the current in-memory cell state to XlsxWriter.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_stored_cell_style"></a>

#### \_set\_stored\_cell\_style

```python
@staticmethod
def _set_stored_cell_style(sheet: _SheetState, key: tuple[int, int],
                           style: CellStyleState) -> None
```

Store or remove one in-memory cell style.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._border_style"></a>

#### \_border\_style

```python
@staticmethod
def _border_style(weight: BorderWeight) -> Optional[int]
```

Return one XlsxWriter border style code.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._xlsx_format"></a>

#### \_xlsx\_format

```python
def _xlsx_format(style: Optional[CellStyleState],
                 datetime_value: bool) -> Optional[object]
```

Return the cached XlsxWriter format for one cell style.

<a id="tableio.tableio_excel_xlsxwriter.TableIOExcelXlsxWriter._set_cell_borders"></a>

#### \_set\_cell\_borders

```python
def _set_cell_borders(sheet: object, row: int, column: int,
                      borders: CellBorder) -> None
```

Apply normalized borders to one worksheet cell.

<a id="tableio.tableio_csv"></a>

# tableio.tableio\_csv

Reader/writer for CSV files.

<a id="tableio.tableio_csv._validate_quoting"></a>

#### \_validate\_quoting

```python
def _validate_quoting(quoting: str) -> _QuoteStyle
```

Validate and convert a quoting string to a csv constant.

**Arguments**:

- `quoting` - The quoting style string. Case-insensitive.

**Returns**:

  The corresponding csv.QUOTE_* constant.

**Raises**:

- `ValueError` - If the quoting string is not recognized.

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

<a id="tableio.tableio_csv._get_csv_dialect_type"></a>

#### \_get\_csv\_dialect\_type

```python
def _get_csv_dialect_type(csv_dialect: CsvDialect) -> type[csv.Dialect]
```

Get the CSV dialect class from the CSV dialect enum.

<a id="tableio.tableio_csv._get_csv_dialect"></a>

#### \_get\_csv\_dialect

```python
def _get_csv_dialect(csv_definitions: CsvDefinitions) -> csv.Dialect
```

Get a CSV dialect instance from the CSV definitions.

<a id="tableio.tableio_csv._is_heading_line"></a>

#### \_is\_heading\_line

```python
def _is_heading_line(line: str) -> bool
```

Check if a line (without line terminator) is a heading.

A heading line starts with one or more '#' characters
followed by a space. This matches the format produced by
_write_heading and avoids false positives for values like
a hexadecimal color code with a leading hash that starts
with '#' but has no space after it.

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

<a id="tableio.tableio_csv.TableIOCsv._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

End the state of the CSV file.

<a id="tableio.tableio_csv.TableIOCsv._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the CSV file suffix.

<a id="tableio.tableio_csv.TableIOCsv._write_heading"></a>

#### \_write\_heading

```python
def _write_heading(heading: str, level: int) -> Position
```

Write a heading to the file.

A heading is a line starting with one or more '#' characters.
The heading is preceded by an empty line and is followed by an
empty line.

**Arguments**:

- `heading` - The heading text to write.
- `level` - The level of the heading. 1 = highest, 3 = lowest.
  If level is None and it is first heading, level 1 is used.
  If level is None and it is not first heading,
  level 2 is used.

**Raises**:

- `ValueError` - If level is outside the range 1 to 3.

**Returns**:

  The position of the last cell written.

<a id="tableio.tableio_csv.TableIOCsv._write_table_listdata"></a>

#### \_write\_table\_listdata

```python
def _write_table_listdata(data: ListDataSeq[CellT],
                          impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
CSV does not support the box, nor formatting, nor filtered data range.

**Arguments**:

- `data` - The list data to write.
- `impl_meta` - The implementation meta data.

**Raises**:

- `CapabilityNotSupported` - If box is provided.

**Returns**:

  The position of the last cell written.

<a id="tableio.tableio_csv.TableIOCsv._write_table_fmtlistdata"></a>

#### \_write\_table\_fmtlistdata

```python
def _write_table_fmtlistdata(data: FmtListData,
                             impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
CSV does not support the box, nor formatting, nor filtered data range.

**Arguments**:

- `data` - The list data to write.
- `impl_meta` - The implementation meta data.

**Raises**:

- `CapabilityNotSupported` - If impl_meta.box is provided.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_csv.TableIOCsv._write_table_dictdata"></a>

#### \_write\_table\_dictdata

```python
def _write_table_dictdata(data: DictDataMap[CellT],
                          impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
CSV does not support the box, nor formatting, nor filtered data range.

**Arguments**:

- `data` - The dict data to write.
- `impl_meta` - The implementation meta data.

**Raises**:

- `CapabilityNotSupported` - If impl_meta.common_impl.box is provided.

**Returns**:

  The position of the last cell written.

<a id="tableio.tableio_csv.TableIOCsv._write_table_fmtdictdata"></a>

#### \_write\_table\_fmtdictdata

```python
def _write_table_fmtdictdata(
        data: FmtDictData,
        impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
CSV does not support the box, nor formatting, nor filtered data range.

**Arguments**:

- `data` - The dict data to write.
- `impl_meta` - The implementation meta data.

**Raises**:

- `CapabilityNotSupported` - If impl_meta.common_impl.box is provided.

**Returns**:

  The position of the last cell written.

<a id="tableio.tableio_csv.TableIOCsv._read_raw_sections"></a>

#### \_read\_raw\_sections

```python
def _read_raw_sections() -> tuple[list[str], list[str]]
```

Read heading and data lines from the current position.

Skips leading empty lines. Lines matching the heading
pattern (one or more '#' followed by a space) that appear
before the first data line are collected as headings with
the leading '#' characters and space stripped. Data lines
are collected until an empty line or end of file.

**Returns**:

  A tuple of (headings, data_lines).

<a id="tableio.tableio_csv.TableIOCsv._read_table_listdata"></a>

#### \_read\_table\_listdata

```python
def _read_table_listdata(
        box: Optional[Box] = None) -> ReadResult[ListData[Value]]
```

Read a table of list data from the file.

Read a table from the file. The table is read into a list of
lists. Empty lines before the table are ignored. Lines
starting with '#' followed by a space are read as headings.
The first non-empty line not matching the heading pattern is
the first row of the table. Reading stops when an empty line
is encountered or the end of the file is reached.
CSV does not support reading from a box.

**Arguments**:

- `box` - Not allowed in CSV.

**Raises**:

- `CapabilityNotSupported` - If box is provided.

**Returns**:

  The data as a list of lists, and any headings found
  before the table.

<a id="tableio.tableio_csv.TableIOCsv._read_table_dictdata"></a>

#### \_read\_table\_dictdata

```python
def _read_table_dictdata(
        box: Optional[Box] = None) -> ReadResult[DictData[Value]]
```

Read a table of dict data from the file.

Read a table from the file. The table is read into a list of
dicts. Empty lines before the table are ignored. Lines
starting with '#' followed by a space are read as headings.
The first non-empty line not matching the heading pattern is
the header row with column names. Subsequent lines are data
rows. Reading stops when an empty line is encountered or the
end of the file is reached.
CSV does not support reading from a box.

**Arguments**:

- `box` - Not allowed in CSV.

**Raises**:

- `CapabilityNotSupported` - If box is provided.

**Returns**:

  The data as a list of dicts, and any headings found
  before the table.

<a id="tableio.config_data_error"></a>

# tableio.config\_data\_error

Structured errors for framework-neutral TableIO configuration.

<a id="tableio.config_data_error.ConfigIssue"></a>

## ConfigIssue Objects

```python
@dataclass
class ConfigIssue()
```

One validation issue for a TableIO configuration.

The issue name is the dotted user-facing configuration parameter name.
This lets applications and adapter libraries point diagnostics at the
same names that appear in configuration files and documentation.

<a id="tableio.config_data_error.ConfigIssue.name"></a>

#### name

The dotted configuration parameter name, for example ``csv.quoting``.

<a id="tableio.config_data_error.ConfigIssue.message"></a>

#### message

The human-readable validation message for this parameter.

<a id="tableio.config_data_error.ConfigError"></a>

## ConfigError Objects

```python
class ConfigError(ValueError)
```

Raised when TableIO configuration validation fails.

The ``issues`` attribute contains all validation issues that could be
found in one pass. ``str(error)`` is intended to be suitable as a compact
user-facing summary, while ``issues`` is intended for applications and
adapter libraries that want to attach messages to individual
configuration fields.

<a id="tableio.config_data_error.ConfigError.issues"></a>

#### issues

The validation issues that caused the exception.

<a id="tableio.config_data_error.ConfigError.__init__"></a>

#### \_\_init\_\_

```python
def __init__(issues: tuple[ConfigIssue, ...],
             message: Optional[str] = None) -> None
```

Initialize the configuration validation error.

**Arguments**:

- `issues` - One or more structured validation issues.
- `message` - Optional summary message for the whole configuration.

<a id="tableio.tableio_spreadsheetbased"></a>

# tableio.tableio\_spreadsheetbased

Intermediate base class for spreadsheet-based file formats.

<a id="tableio.tableio_spreadsheetbased.excel_column_name"></a>

#### excel\_column\_name

```python
def excel_column_name(column: int) -> str
```

Return the Excel-style A1 column name for one zero-based column.

<a id="tableio.tableio_spreadsheetbased._ScanResult"></a>

## \_ScanResult Objects

```python
class _ScanResult(NamedTuple)
```

Details gathered while scanning one worksheet section.

<a id="tableio.tableio_spreadsheetbased._SheetState"></a>

## \_SheetState Objects

```python
class _SheetState(NamedTuple)
```

Sequential state tracked for one sheet during an open session.

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

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._heading_font_size"></a>

#### \_heading\_font\_size

```python
@staticmethod
def _heading_font_size(level: int) -> int
```

Return the font size used for one heading level.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._python_value_from_spreadsheet"></a>

#### \_python\_value\_from\_spreadsheet

```python
@staticmethod
def _python_value_from_spreadsheet(value: object) -> Value
```

Convert one backend value to the public Value type.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._spreadsheet_value_from_python"></a>

#### \_spreadsheet\_value\_from\_python

```python
@staticmethod
def _spreadsheet_value_from_python(value: object) -> Value
```

Convert one Python value to a spreadsheet-compatible value.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._sheet_key"></a>

#### \_sheet\_key

```python
@staticmethod
def _sheet_key(sheet_name: str) -> str
```

Return the normalized dictionary key for one sheet name.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_matching_sheet_name"></a>

#### \_find\_matching\_sheet\_name

```python
@classmethod
def _find_matching_sheet_name(cls, existing_sheet_names: list[str],
                              sheet_name: str) -> Optional[str]
```

Return the existing sheet name matching the requested name.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._current_sheet_key"></a>

#### \_current\_sheet\_key

```python
def _current_sheet_key() -> str
```

Return the normalized key of the current sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._make_current_sheet_state"></a>

#### \_make\_current\_sheet\_state

```python
def _make_current_sheet_state() -> _SheetState
```

Build the initial sequential state for the current sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._load_current_sheet_state"></a>

#### \_load\_current\_sheet\_state

```python
def _load_current_sheet_state() -> None
```

Load the current sheet state into the public cursor fields.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._save_current_sheet_state"></a>

#### \_save\_current\_sheet\_state

```python
def _save_current_sheet_state() -> None
```

Persist the public cursor fields for the current sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._initialize_positions"></a>

#### \_initialize\_positions

```python
def _initialize_positions() -> None
```

Initialize the default read and write cursors.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_sheet"></a>

#### \_read\_sheet

```python
def _read_sheet() -> object
```

Return the readable sheet-like object.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_sheet"></a>

#### \_write\_sheet

```python
def _write_sheet() -> object
```

Return the writable sheet-like object.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_value_to_sheet"></a>

#### \_write\_value\_to\_sheet

```python
def _write_value_to_sheet(sheet: object, row: int, column: int,
                          value: object) -> None
```

Write one plain value to one backend cell.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_cell_format"></a>

#### \_set\_cell\_format

```python
def _set_cell_format(sheet: object, row: int, column: int,
                     fmt: Optional[Fmt]) -> None
```

Apply optional formatting to one backend cell.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_cell_borders"></a>

#### \_set\_cell\_borders

```python
def _set_cell_borders(sheet: object, row: int, column: int,
                      borders: CellBorder) -> None
```

Apply normalized cell borders to one backend cell.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._apply_heading_style"></a>

#### \_apply\_heading\_style

```python
def _apply_heading_style(row: int, column: int, level: int) -> None
```

Apply the backend heading style to one cell.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._last_used_row"></a>

#### \_last\_used\_row

```python
def _last_used_row(sheet: object) -> int
```

Return the last used row index on a backend sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._last_used_column"></a>

#### \_last\_used\_column

```python
def _last_used_column(sheet: object) -> int
```

Return the last used column index on a backend sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(sheet: object, row: int, column: int) -> Value
```

Return one backend cell converted to the public Value type.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._filtered_range_infos"></a>

#### \_filtered\_range\_infos

```python
def _filtered_range_infos() -> list[tuple[str, tuple[int, int, int, int]]]
```

Return the backend filtered ranges with zero-based bounds.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._delete_filtered_range"></a>

#### \_delete\_filtered\_range

```python
def _delete_filtered_range(name: str) -> None
```

Delete one backend filtered range by name.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._add_filtered_range"></a>

#### \_add\_filtered\_range

```python
def _add_filtered_range(bounds: tuple[int, int, int, int], name: str) -> None
```

Create one backend filtered range.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._set_column_width_if_wider"></a>

#### \_set\_column\_width\_if\_wider

```python
def _set_column_width_if_wider(column: int, width: float) -> None
```

Widen one backend column if the target width is larger.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._used_bounds_by_cell_scan"></a>

#### \_used\_bounds\_by\_cell\_scan

```python
def _used_bounds_by_cell_scan(sheet: object, row_limit: int,
                              column_limit: int) -> tuple[int, int]
```

Return the last used row and column by scanning cell values.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_value"></a>

#### \_write\_value

```python
def _write_value(row: int,
                 column: int,
                 value: object,
                 fmt: Optional[Fmt] = None) -> None
```

Write one value to the writable sheet and readable snapshot.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._clear_range"></a>

#### \_clear\_range

```python
def _clear_range(top: int, left: int, bottom: int, right: int) -> None
```

Clear values and simple formatting in a rectangle.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_limits"></a>

#### \_read\_limits

```python
def _read_limits(box: Optional[Box]) -> tuple[int, int, int, Optional[int]]
```

Return the row and column limits for a read operation.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_limit_bottom"></a>

#### \_scan\_limit\_bottom

```python
def _scan_limit_bottom(sheet: object, top: int) -> int
```

Return the exclusive bottom limit used when scanning rows.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_limit_right"></a>

#### \_scan\_limit\_right

```python
def _scan_limit_right(sheet: object, left: int, right: Optional[int]) -> int
```

Return the exclusive right limit used when scanning rows.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_nonempty_columns"></a>

#### \_row\_nonempty\_columns

```python
def _row_nonempty_columns(sheet: object, row: int, left: int,
                          right: Optional[int]) -> list[int]
```

Return the non-empty columns in one row within the scan limits.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_is_empty"></a>

#### \_row\_is\_empty

```python
def _row_is_empty(sheet: object, row: int, left: int,
                  right: Optional[int]) -> bool
```

Return whether the selected row region contains no values.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._row_is_heading"></a>

#### \_row\_is\_heading

```python
def _row_is_heading(sheet: object, row: int, left: int, right: Optional[int],
                    bottom: int) -> bool
```

Return whether the row matches the heading layout.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._scan_section"></a>

#### \_scan\_section

```python
def _scan_section(box: Optional[Box]) -> _ScanResult
```

Scan the next readable section on the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_grid"></a>

#### \_read\_grid

```python
def _read_grid(scan: _ScanResult) -> ListData[Value]
```

Read a rectangular grid from the scanned section.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_read_positions"></a>

#### \_update\_read\_positions

```python
def _update_read_positions(scan: _ScanResult, box: Optional[Box]) -> None
```

Update default read and write positions after a read.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._range_contains"></a>

#### \_range\_contains

```python
@staticmethod
def _range_contains(first: tuple[int, int, int, int],
                    second: tuple[int, int, int, int]) -> bool
```

Return whether one exclusive rectangle contains another.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._ranges_overlap"></a>

#### \_ranges\_overlap

```python
@staticmethod
def _ranges_overlap(first: tuple[int, int, int, int],
                    second: tuple[int, int, int, int]) -> bool
```

Return whether two zero-based exclusive rectangles overlap.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._sheet_table_regions"></a>

#### \_sheet\_table\_regions

```python
def _sheet_table_regions() -> list[tuple[int, int, int, int]]
```

Return detected table-like regions on the active readable sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._existing_table_regions"></a>

#### \_existing\_table\_regions

```python
def _existing_table_regions() -> list[tuple[int, int, int, int]]
```

Return persisted and inferred table regions on the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._check_boxed_table_overwrite"></a>

#### \_check\_boxed\_table\_overwrite

```python
def _check_boxed_table_overwrite(bounds: tuple[int, int, int, int]) -> None
```

Reject writes that would leave part of an existing table behind.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._filter_range_name_in_use"></a>

#### \_filter\_range\_name\_in\_use

```python
def _filter_range_name_in_use(name: str) -> bool
```

Return whether the backend already contains the filter name.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._next_filter_range_name"></a>

#### \_next\_filter\_range\_name

```python
def _next_filter_range_name() -> str
```

Return a backend-unique name for one filtered data range.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._remove_overlapping_filtered_ranges"></a>

#### \_remove\_overlapping\_filtered\_ranges

```python
def _remove_overlapping_filtered_ranges(
        bounds: tuple[int, int, int, int]) -> None
```

Remove backend filtered ranges that overlap the write bounds.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_filtered_data_range"></a>

#### \_write\_filtered\_data\_range

```python
def _write_filtered_data_range(bounds: tuple[int, int, int, int]) -> None
```

Create one backend filtered data range for the given bounds.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._values_match"></a>

#### \_values\_match

```python
@staticmethod
def _values_match(cell_value: Value, find_value: Value,
                  type_conversion: bool) -> bool
```

Return whether one cell matches one requested value.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._split_cell_grid"></a>

#### \_split\_cell\_grid

```python
@classmethod
def _split_cell_grid(
    cls, data: ListDataSeq[CellT]
) -> tuple[ListData[Value], list[list[Optional[Fmt]]]]
```

Return a grid of plain values and matching cell formats.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_bounds"></a>

#### \_find\_bounds

```python
def _find_bounds(box: Optional[Box]) -> tuple[int, int, int, int]
```

Return the search limits for one find operation.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._grid_matches"></a>

#### \_grid\_matches

```python
def _grid_matches(sheet: object, top: int, left: int,
                  find_value: ListData[Value], type_conversion: bool) -> bool
```

Return whether one sheet region matches the requested grid.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._column_width_text"></a>

#### \_column\_width\_text

```python
@staticmethod
def _column_width_text(value: object) -> str
```

Return the text used to estimate a readable column width.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._table_column_width"></a>

#### \_table\_column\_width

```python
def _table_column_width(top: int, bottom: int, column: int) -> float
```

Return a width target for one table column.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_table_column_widths"></a>

#### \_update\_table\_column\_widths

```python
def _update_table_column_widths(top: int, left: int, bottom: int,
                                right: int) -> None
```

Widen backend columns to fit the written table content.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_start"></a>

#### \_write\_start

```python
def _write_start(box: Optional[Box]) -> tuple[int, int]
```

Return the start position for a write operation.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._update_write_position"></a>

#### \_update\_write\_position

```python
def _update_write_position(next_row: int) -> None
```

Update the default write cursor after a write operation.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_grid"></a>

#### \_write\_grid

```python
def _write_grid(values: ListData[Value], formats: list[list[Optional[Fmt]]],
                impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write a rectangular grid of values and optional formats.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_grid_borders"></a>

#### \_write\_grid\_borders

```python
def _write_grid_borders(start_row: int, start_column: int,
                        values: ListData[Value],
                        borders: BorderHelper) -> None
```

Apply normalized table borders to all cells in a grid.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_heading"></a>

#### \_write\_heading

```python
def _write_heading(heading: str, level: int) -> Position
```

Write a heading to the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._split_cell_value"></a>

#### \_split\_cell\_value

```python
@classmethod
def _split_cell_value(cls, cell: CellT) -> tuple[Value, Optional[Fmt]]
```

Return the plain value and optional cell format.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_listdata"></a>

#### \_write\_table\_listdata

```python
def _write_table_listdata(data: ListDataSeq[CellT],
                          impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write list data to the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_fmtlistdata"></a>

#### \_write\_table\_fmtlistdata

```python
def _write_table_fmtlistdata(data: FmtListData,
                             impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write row-formatted list data to the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_dictdata"></a>

#### \_write\_table\_dictdata

```python
def _write_table_dictdata(data: DictDataMap[CellT],
                          impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write dict data to the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_table_fmtdictdata"></a>

#### \_write\_table\_fmtdictdata

```python
def _write_table_fmtdictdata(
        data: FmtDictData,
        impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write row-formatted dict data to the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_table_listdata"></a>

#### \_read\_table\_listdata

```python
def _read_table_listdata(
        box: Optional[Box] = None) -> ReadResult[ListData[Value]]
```

Read list data from the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_table_dictdata"></a>

#### \_read\_table\_dictdata

```python
def _read_table_dictdata(
        box: Optional[Box] = None) -> ReadResult[DictData[Value]]
```

Read dict data from the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._find_value"></a>

#### \_find\_value

```python
def _find_value(find_value: ListData[Value],
                type_conversion: bool = True,
                box: Optional[Box] = None) -> Optional[Box]
```

Find the first matching value grid on the active sheet.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._read_cells"></a>

#### \_read\_cells

```python
def _read_cells(box: Box) -> ListData[Value]
```

Read the exact cell rectangle described by the box.

<a id="tableio.tableio_spreadsheetbased.TableIOSpreadsheetBased._write_cells"></a>

#### \_write\_cells

```python
def _write_cells(data: ListDataSeq[CellT], box: Box) -> None
```

Write the exact cell rectangle described by the box.

<a id="tableio.tableio_mformatbased"></a>

# tableio.tableio\_mformatbased

TableIO reader/writer class for a file format based on mformat.

<a id="tableio.tableio_mformatbased._allow_overwrite"></a>

#### \_allow\_overwrite

```python
def _allow_overwrite(_: str) -> None
```

No-op callback signalling that overwrite is permitted.

Passed to the mformat constructor so that it does not raise
when the file already exists. The actual overwrite decision
has already been made by the TableIO base class.

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

<a id="tableio.tableio_mformatbased.TableIOMformatBased._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Close the file. Avoid calling this method directly,
use the context manager instead.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

End the state of the reader/writer class. NOP for this class.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix. NOP for this class.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_heading"></a>

#### \_write\_heading

```python
def _write_heading(heading: str, level: int) -> Position
```

Write a heading to the file.

Write a heading to the file. Headings are a line between tables.

**Arguments**:

- `heading` - The heading text to write.
- `level` - The level of the heading. 1 = highest, 3 = lowest.
  If level is None and it is first heading, level 1 is used.
  If level is None and it is not first heading,
  level 2 is used.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_table_listdata"></a>

#### \_write\_table\_listdata

```python
def _write_table_listdata(data: ListDataSeq[CellT],
                          impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write a table of list data to the file.

Write a table of list data to the file.
impl_meta.box is not supported for this class.
impl_meta.filtered_data_range is ignored for this class.

**Arguments**:

- `data` - The list data to write.
- `impl_meta` - The implementation meta data.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_table_fmtlistdata"></a>

#### \_write\_table\_fmtlistdata

```python
def _write_table_fmtlistdata(data: FmtListData,
                             impl_meta: TableIO.ImplMetaForWrite) -> Position
```

Write a table of formatted list data to the file.

Write a table of formatted list data to the file.
impl_meta.box is not supported for this class.
impl_meta.filtered_data_range is ignored for this class.

**Arguments**:

- `data` - The formatted list data to write.
- `impl_meta` - The implementation meta data.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_table_dictdata"></a>

#### \_write\_table\_dictdata

```python
def _write_table_dictdata(data: DictDataMap[CellT],
                          impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write a table of dict data to the file.

Write a table of dict data to the file.
impl_meta.common_impl.box is not supported for this class.
impl_meta.common_impl.filtered_data_range is ignored for this class.

**Arguments**:

- `data` - The dict data to write.
- `impl_meta` - The implementation meta data.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._write_table_fmtdictdata"></a>

#### \_write\_table\_fmtdictdata

```python
def _write_table_fmtdictdata(
        data: FmtDictData,
        impl_meta: TableIO.ImplMetaForDictWrite) -> Position
```

Write a table of formatted dict data to the file.

Write a table of formatted dict data to the file.
impl_meta.box is not supported for this class.
impl_meta.filtered_data_range is ignored for this class.
The dict data is converted to list data with column_order
as the header row, then written via _write_table_fmtlistdata.

**Arguments**:

- `data` - The formatted dict data to write.
- `impl_meta` - The implementation meta data.

**Returns**:

  The position of the last cell written. Not reliable.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._read_table_listdata"></a>

#### \_read\_table\_listdata

```python
def _read_table_listdata(
        box: Optional[Box] = None) -> ReadResult[ListData[Value]]
```

Read a table of list data from the file.

Reading is not supported for mformat based classes.

<a id="tableio.tableio_mformatbased.TableIOMformatBased._read_table_dictdata"></a>

#### \_read\_table\_dictdata

```python
def _read_table_dictdata(
        box: Optional[Box] = None) -> ReadResult[DictData[Value]]
```

Read a table of dict data from the file.

Reading is not supported for mformat based classes.

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

<a id="tableio.tableio_excelbased.TableIOExcelBased._DATETIME_NUMBER_FORMAT"></a>

#### \_DATETIME\_NUMBER\_FORMAT

Excel number format used for datetime values.

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

<a id="tableio.tableio_excelbased.TableIOExcelBased._datetime_number_format"></a>

#### \_datetime\_number\_format

```python
@classmethod
def _datetime_number_format(cls) -> str
```

Return the Excel number format used for datetime values.

<a id="tableio.tableio_excelbased.TableIOExcelBased._excel_column_name"></a>

#### \_excel\_column\_name

```python
@staticmethod
def _excel_column_name(column: int) -> str
```

Return the Excel A1 column name for one zero-based column.

<a id="tableio.tableio_excelbased.TableIOExcelBased._excel_cell_ref"></a>

#### \_excel\_cell\_ref

```python
@classmethod
def _excel_cell_ref(cls, row: int, column: int) -> str
```

Return one Excel A1 cell reference for zero-based coordinates.

<a id="tableio.tableio_excelbased.TableIOExcelBased._excel_range_ref"></a>

#### \_excel\_range\_ref

```python
@classmethod
def _excel_range_ref(cls, top: int, left: int, bottom: int, right: int) -> str
```

Return one Excel A1 range string for zero-based bounds.

<a id="tableio.tableio_excelbased.TableIOExcelBased._filtered_table_header"></a>

#### \_filtered\_table\_header

```python
@staticmethod
def _filtered_table_header(value: object, index: int) -> str
```

Return the normalized Excel table header for one cell value.

<a id="tableio.tableio_excelbased.TableIOExcelBased._filtered_table_headers"></a>

#### \_filtered\_table\_headers

```python
@classmethod
def _filtered_table_headers(cls, values: Sequence[object]) -> list[str]
```

Return normalized Excel table headers for one header row.

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

<a id="tableio.tableio_excel_openpyxl._xml_tag"></a>

#### \_xml\_tag

```python
def _xml_tag(namespace: str, tag_name: str) -> str
```

Return one fully qualified XML tag name.

<a id="tableio.tableio_excel_openpyxl._font_child_sort_key"></a>

#### \_font\_child\_sort\_key

```python
def _font_child_sort_key(element: ET.Element) -> int
```

Return the schema-order key for one Excel font child element.

<a id="tableio.tableio_excel_openpyxl._styles_xml_with_sorted_fonts"></a>

#### \_styles\_xml\_with\_sorted\_fonts

```python
def _styles_xml_with_sorted_fonts(data: bytes) -> bytes
```

Return styles XML with font child elements in schema order.

<a id="tableio.tableio_excel_openpyxl._new_shared_strings_root"></a>

#### \_new\_shared\_strings\_root

```python
def _new_shared_strings_root() -> ET.Element
```

Create an empty shared strings XML root element.

<a id="tableio.tableio_excel_openpyxl._read_shared_strings_root"></a>

#### \_read\_shared\_strings\_root

```python
def _read_shared_strings_root(file_name: Path) -> ET.Element
```

Read the shared strings root, or create an empty one.

<a id="tableio.tableio_excel_openpyxl._shared_string_count"></a>

#### \_shared\_string\_count

```python
def _shared_string_count(shared_strings_root: ET.Element) -> int
```

Return the number of shared string items in the root.

<a id="tableio.tableio_excel_openpyxl._shared_strings_xml"></a>

#### \_shared\_strings\_xml

```python
def _shared_strings_xml(shared_strings_root: ET.Element) -> bytes
```

Return finalized shared strings XML bytes.

<a id="tableio.tableio_excel_openpyxl._inline_string_to_shared_string"></a>

#### \_inline\_string\_to\_shared\_string

```python
def _inline_string_to_shared_string(cell: ET.Element,
                                    shared_strings_root: ET.Element) -> None
```

Move one inline string cell value to the shared string table.

<a id="tableio.tableio_excel_openpyxl._sheet_xml_with_shared_strings"></a>

#### \_sheet\_xml\_with\_shared\_strings

```python
def _sheet_xml_with_shared_strings(data: bytes,
                                   shared_strings_root: ET.Element) -> bytes
```

Return sheet XML with inline strings converted to shared strings.

<a id="tableio.tableio_excel_openpyxl._content_types_with_shared_strings"></a>

#### \_content\_types\_with\_shared\_strings

```python
def _content_types_with_shared_strings(data: bytes) -> bytes
```

Return content types XML with a shared strings override.

<a id="tableio.tableio_excel_openpyxl._next_relationship_id"></a>

#### \_next\_relationship\_id

```python
def _next_relationship_id(root: ET.Element) -> str
```

Return the next workbook relationship id.

<a id="tableio.tableio_excel_openpyxl._workbook_rels_with_shared_strings"></a>

#### \_workbook\_rels\_with\_shared\_strings

```python
def _workbook_rels_with_shared_strings(data: bytes) -> bytes
```

Return workbook relationships XML with a shared strings relation.

<a id="tableio.tableio_excel_openpyxl._is_worksheet_xml"></a>

#### \_is\_worksheet\_xml

```python
def _is_worksheet_xml(filename: str) -> bool
```

Return True if an archive entry is a worksheet XML file.

<a id="tableio.tableio_excel_openpyxl._worksheet_rewrites_with_shared_strings"></a>

#### \_worksheet\_rewrites\_with\_shared\_strings

```python
def _worksheet_rewrites_with_shared_strings(
        file_name: Path, shared_strings_root: ET.Element) -> dict[str, bytes]
```

Return worksheet XML rewrites and update the shared string table.

<a id="tableio.tableio_excel_openpyxl._rewrite_saved_workbook"></a>

#### \_rewrite\_saved\_workbook

```python
def _rewrite_saved_workbook(file_name: Path) -> None
```

Rewrite the saved workbook so styles XML follows validator order.

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

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

Finalize in-memory state before closing.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the workbook to disk when the file is writable.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._close"></a>

#### \_close

```python
def _close() -> None
```

Close any open workbook handles.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._worksheet_name_map"></a>

#### \_worksheet\_name\_map

```python
@staticmethod
def _worksheet_name_map(workbook: Workbook) -> dict[str, Worksheet]
```

Return the workbook worksheets indexed case-insensitively.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_active_worksheets"></a>

#### \_set\_active\_worksheets

```python
def _set_active_worksheets(worksheet: Worksheet,
                           read_worksheet: Worksheet) -> None
```

Set the current writable and readable worksheets.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._list_sheets"></a>

#### \_list\_sheets

```python
def _list_sheets() -> list[str]
```

List the sheets in the workbook.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._select_sheet"></a>

#### \_select\_sheet

```python
def _select_sheet(sheet_name: str, create: bool = False) -> None
```

Select one workbook sheet, optionally creating it.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._current_sheet_name"></a>

#### \_current\_sheet\_name

```python
def _current_sheet_name() -> str
```

Return the name of the selected worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._read_sheet"></a>

#### \_read\_sheet

```python
def _read_sheet() -> object
```

Return the readable worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_sheet"></a>

#### \_write\_sheet

```python
def _write_sheet() -> object
```

Return the writable worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._highlight_fill"></a>

#### \_highlight\_fill

```python
@staticmethod
def _highlight_fill(highlight: Color) -> PatternFill
```

Return the fill object for the requested highlight color.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._write_value_to_sheet"></a>

#### \_write\_value\_to\_sheet

```python
def _write_value_to_sheet(sheet: object, row: int, column: int,
                          value: object) -> None
```

Write one value to one worksheet cell.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_cell_format"></a>

#### \_set\_cell\_format

```python
def _set_cell_format(sheet: object, row: int, column: int,
                     fmt: Optional[Fmt]) -> None
```

Apply cell formatting to one worksheet cell.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._border_side"></a>

#### \_border\_side

```python
@staticmethod
def _border_side(weight: BorderWeight) -> Side
```

Return one OpenPyXL side object for the requested weight.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._border_value"></a>

#### \_border\_value

```python
def _border_value(borders: CellBorder) -> Border
```

Return one cached OpenPyXL border object.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_cell_borders"></a>

#### \_set\_cell\_borders

```python
def _set_cell_borders(sheet: object, row: int, column: int,
                      borders: CellBorder) -> None
```

Apply normalized borders to one worksheet cell.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._apply_heading_style"></a>

#### \_apply\_heading\_style

```python
def _apply_heading_style(row: int, column: int, level: int) -> None
```

Apply the heading font to one worksheet cell.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._last_used_row"></a>

#### \_last\_used\_row

```python
def _last_used_row(sheet: object) -> int
```

Return the last used row index on a worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._last_used_column"></a>

#### \_last\_used\_column

```python
def _last_used_column(sheet: object) -> int
```

Return the last used column index on a worksheet.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(sheet: object, row: int, column: int) -> Value
```

Return one worksheet cell as a public Value.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._table_bounds"></a>

#### \_table\_bounds

```python
@staticmethod
def _table_bounds(table_ref: str) -> tuple[int, int, int, int]
```

Return zero-based exclusive bounds for one worksheet table.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._filtered_range_infos"></a>

#### \_filtered\_range\_infos

```python
def _filtered_range_infos() -> list[tuple[str, tuple[int, int, int, int]]]
```

Return the worksheet tables and their bounds.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._delete_filtered_range"></a>

#### \_delete\_filtered\_range

```python
def _delete_filtered_range(name: str) -> None
```

Delete one worksheet table by name.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._normalize_filtered_table_header"></a>

#### \_normalize\_filtered\_table\_header

```python
def _normalize_filtered_table_header(top: int, left: int, right: int) -> None
```

Convert the filtered table header row to strings when needed.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._add_filtered_range"></a>

#### \_add\_filtered\_range

```python
def _add_filtered_range(bounds: tuple[int, int, int, int], name: str) -> None
```

Add one lightweight Excel table for a filtered data range.

<a id="tableio.tableio_excel_openpyxl.TableIOExcelOpenPyXL._set_column_width_if_wider"></a>

#### \_set\_column\_width\_if\_wider

```python
def _set_column_width_if_wider(column: int, width: float) -> None
```

Widen one worksheet column if the target width is larger.

