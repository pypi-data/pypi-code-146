from dash import html
from .AntdButton import *
from .AntdCheckbox import *

class dashTable(html.Div):
    """
    A component to generate dash table. It inheritated keyword arguments form
    dash.html.Div unless specified.
    - data (pandas.DataFrame)
      For non-text data, sort the inputs into the formats below
          - Hyperlink: {'type': 'A', 'href': 'xxxx', 'text': 'xxxx', 'disabled': False}
    - column_mapping (dict, optional)
      {'label': 'text_to_show_in_tHead', 'className': 'class_to_apply', 'style': {}, 'rowspan': False}
    - checkedRows (dict, optional)
      In case there exists a checkbox column
      {'columnaName': ['var1', 'var2']}
    """

    def __init__(self,
                 data=None,
                 column_mapping={},
                 *args, **kwargs):
        html.Div.__init__(self, *args, **kwargs)
        # check rowspan
        if column_mapping:
            rowspanColumns = [
                k for k, v in column_mapping.items() if v.get('rowSpan') is True]
            if len(rowspanColumns) > 0:
                rowSpans = {}
                for c in rowspanColumns:
                    data[c + '_'] = data[c].apply(lambda x: str(x)).tolist()
                    rowSpans[c] = dict(data[c + '_'].value_counts())
                data = data.sort_values(by=[x + '_' for x in rowspanColumns])
                data.loc[data.duplicated(subset=[x + '_' for x in rowspanColumns]),
                         [x + '_' for x in rowspanColumns]] = ''
                for c in rowspanColumns:
                    data[c] = data.apply(
                        lambda x: self.sortRowSpan(c, x, rowSpans), axis=1)
                data = data.drop(columns=[x + '_' for x in rowspanColumns])
        tHeads, tRows, columnClassNames, columnStyles = [], [], {}, {}
        cols = list(data.columns)
        for i in range(len(cols)):
            columnId, columnName, colContent = cols[i], cols[i], cols[i]
            columnClassName = ['ant-table-cell', '{}-cell'.format(cols[i])]
            columnStyle = None
            if column_mapping.get(columnId):
                if column_mapping[columnId].get('label'):
                    colContent = column_mapping[columnId]['label']
                if column_mapping[columnId].get('className'):
                    columnClassName.append(
                        column_mapping[columnId]['className'])
                    columnClassName = ' '.join(
                        [x for x in columnClassName if x])
                    columnClassNames[columnId] = columnClassName
                if column_mapping[columnId].get('style'):
                    columnStyle = column_mapping[columnId]['style']
                    columnStyles[columnId] = columnStyle
            thead = html.Th(colContent, className=columnClassName,
                            style=columnStyle)
            tHeads.append(thead)

        values = data.to_dict('records')
        for j in range(len(values)):
            row, tr, td = values[j], [], ''
            for k, v in row.items():
                columnId, columnContent = k, v
                columnStyle = columnStyles.get(columnId)
                columnClassName = columnClassNames.get(columnId)
                if type(columnContent) == dict:
                    if columnContent.get('rowSpan'):
                        if columnContent.get('rowSpan') > 0:
                            td = html.Td(
                                self.sortCellContent(columnContent['content']),
                                className=columnClassName,
                                style=columnStyle,
                                rowSpan=columnContent.get('rowSpan')
                            )
                    else:
                        td = html.Td(
                            self.sortCellContent(columnContent),
                            className=columnClassName,
                            style=columnStyle)
                else:
                    td = html.Td(
                        columnContent,
                        className=columnClassName,
                        style=columnStyle)
                tr.append(td)
            tr = html.Tr([x for x in tr if x], className='ant-table-row')
            tRows.append(tr)

        table_wrapper = html.Div(
            html.Table(
                [
                    html.Thead(
                        html.Tr(tHeads),
                        className='ant-table-thead'
                    ),
                    html.Tbody(
                        tRows,
                        className='ant-table-tbody'
                    )
                ],
                className='ant-table w-100'
            ),
            className='ant-table-content w-100'
        )
        self.children = table_wrapper

    @staticmethod
    def sortRowSpan(col, df, rowSpansDt):
        if not df[col + '_']:
            return {'rowSpan': 0}
        else:
            return {
                'content': df[col],
                'rowSpan': rowSpansDt[col][df[col + '_']]
            }

    @staticmethod
    def sortCellContent(cell):
        if type(cell) in [str, int, float]:
            return cell
        elif type(cell) is list:
            return ', '.join(cell)
        elif type(cell) is dict:
            if cell.get('type') == 'A':
                if cell.get('disabled') is True:
                    return cell['text']
                else:
                    return html.A(
                        cell['text'],
                        href=cell['href'],
                        target='_blank')
            if cell.get('type') == 'Button':
                return AntdButton(
                    cell['text'],
                    type=cell['btnType'] if cell.get('btnType') else 'primary',
                    id=cell['id'] if cell.get('id') else str(cell['text']),
                    style=cell['style'] if cell.get('style') else None,
                    className=cell['className'] if cell.get('className') else None,
                    nClicks=cell['nClicks'] if cell.get('nClicks') else 0
                )
            if cell.get('type') == 'CheckBox':
                return AntdCheckbox(
                        label=cell['text'],
                        id=cell['id'] if cell.get('id') else str(cell['text']),
                        checked=cell['checked'] if cell.get('checked') is True else False
                    )


#         tHeads.append(
#             html.Th(
#                 col_name,
#                 className=class_dt[col],
#                 style=style
#             )
#         )


#
#
#
#
# def Table(
#         df,
#         cell_class='cat-cell',
#         className='cataloge-table w-100',
#         col_mapping={
#             'theme': {'label': 'Theme', 'className': 'px-1 md-hidden', 'style': {'width': '20%'}},
#             'topic': {'label': 'Topic', 'className': 'w-25', 'style': {'width': '33%'}},
#             'fmc': {'label': ' ', 'style': {'width': '20px'}, 'className': 'px-0'},
#             'curated': {'label': 'Curated by Data Team', 'style': {'width': '22%'}},
#             'raw': {'label': 'Raw / In progress/ Hardcopy'},
#             'others': {'class': 'timepoint', 'className': 'text-center'}
#         },
#         key=None,
#         badge_cols={'units': 'ant-badge-status-success"'},
#         checkedValues=[],
#         disableHyperlink=False,
#         id=''
# ):
#     rename_cols = lambda x: col_rename[x] if x in col_rename.keys() else x
#     cell_className = concat_text(['ant-table-cell', cell_class])
#     cols = list(df.columns)
#     tHeads, tRows, class_dt, style_dt = [], [], {}, {}
#     checkedValues = [] if isna(checkedValues) else checkedValues
#     for i in range(len(cols)):
#         col, style, col_name = cols[i], None, cols[i]
#         th_class = ['ant-table-cell']
#         if col_mapping.get(col):
#             if col_mapping.get(col).get('class'):
#                 th_class.append('{}-cell'.format(col_mapping[col].get('class').lower()))
#             else:
#                 th_class.append('{}-cell'.format(col.lower()))
#             th_class.append(col_mapping[col].get('className'))
#             if col_mapping[col].get('style'):
#                 style = col_mapping[col]['style']
#             if col_mapping[col].get('label'):
#                 col_name = col_mapping[col]['label']
#         elif col_mapping.get('others'):
#             th_class.append('{}-cell'.format(col_mapping['others'].get('class')))
#             th_class.append('{}'.format(col_mapping['others'].get('className')))
#         class_dt[col] = concat_text(th_class, sep=' ')
#         style_dt[col] = style
#         tHeads.append(
#             html.Th(
#                 col_name,
#                 className=class_dt[col],
#                 style=style
#             )
#         )
#     for i in range(len(df)):
#         row = df.iloc[i].tolist()
#         tr = []
#         for j in range(len(row)):
#             col, cell = cols[j], row[j]
#             if key == col:
#                 id = {'index': 'row_' + cell['id'], 'type': 'tr-row'}
#             if type(cell) == dict:
#                 if cell.get('type') == 'rowSpan':
#                     if cell.get('text'):
#                         td = html.Td(cell['text'], className=class_dt[col], style=style_dt.get(col), rowSpan=cell['rowspan'])
#                         tr.append(td)
#                 else:
#                     if cell.get('type') == 'A':
#                         if not disableHyperlink:
#                             ccontent = html.A(
#                                 cell['text'],
#                                 href=cell['href']
#                             )
#                         else:
#                             ccontent = cell['text']
#                     elif cell.get('type') == 'Span':
#                         ccontent = cell['text']
#                     elif cell.get('type') == 'Button':
#                         n_clicks = cell['n_clicks'] if cell.get('n_clicks') else 0
#                         ccontent = Btn(id=cell['id']['index'],
#                                        input_type=cell['id']['type'],
#                                        content=cell['text'],
#                                        className='cell-btn w-100',
#                                        btn_type='primary',
#                                        style=cell['style'],
#                                        disabled=False,
#                                        title=cell['title'],
#                                        n_clicks=0,
#                                        output_id='selection').button
#                     elif cell.get('type') == 'Checkbox':
#                         if cell['id'] in checkedValues:
#                             val = [cell['id']]
#                         else:
#                             val = []
#                         ccontent = CheckBoxes(
#                             id=cell['id'],
#                             input_type=cell['input_type'],
#                             is_icon=False,
#                             options=[{'label': cell['text'], 'value': cell['id']}],
#                             select_all=False,
#                             value=val
#                         )
#                     else:
#                         ccontent = cell
#                     td = html.Td(ccontent, className=class_dt[col], style=style_dt.get(col))
#                     tr.append(td)
#             else:
#                 if col in badge_cols.keys():
#                     text = row[j]
#                     if '^' in text:
#                         p1 = text.split('^')[0]
#                         p2 = text.split('^')[1]
#                         text = html.Span([p1, html.Sup(p2)])
#                     if text:
#                         ccontent = html.Span(
#                             text,
#                             className='badge ant-badge-status-success'
#                         )
#                     else:
#                         ccontent = text
#                 else:
#                     ccontent = row[j]
#                 td = html.Td(ccontent, className=class_dt[col], style=style_dt.get(col))
#                 tr.append(td)
#         tr = [x for x in tr if x]
#         row_tr = html.Tr(
#             tr,
#             className='ant-table-row',
#         )
#         tRows.append(row_tr)
#     tHeads = html.Tr(tHeads)
#     wrapper = html.Div(
#         html.Table(
#             [
#                 html.Thead(
#                     tHeads,
#                     className='ant-table-thead'
#                 ),
#                 html.Tbody(
#                     tRows,
#                     className='ant-table-tbody'
#                 )
#             ],
#             className='ant-table ' + className,
#         ),
#         className='ant-table-content',
#         id=id
#     )
#     return wrapper
