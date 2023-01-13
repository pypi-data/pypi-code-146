import pandas as pd
import codecs
from lxml import etree as et
import re
import os
from typing import List
import logging

def extract_calculated_from_report_spec(file_path: str, 
                                        report_spec: str, 
                                        analysis: int, 
                                        var_overview: pd.DataFrame
                                        ) -> List[str]:
    
    def parse_xml(file_name: str):

        full_path_to_file = file_name
        parser = et.XMLParser()

        def tidy_xml(file_name):

            global file_content_new

            with codecs.open(file_name, mode=r'r', encoding=r'UTF-8-SIG') as f:
                file_content = f.read()
                file_content_new = re.sub(r'(<td).*(/td>)', r'', file_content)
                file_content_new = re.sub(r'(<td|<row|<value|<collWidth)(| colpan.*>)(.*)(/td>|/row>|/value>|/collWidth>)', r'', file_content_new)
                # file_content_new = re.sub(r'(<value>)(.*)(</value>)', r'', file_content_new)
                file_content_new = re.sub(r'(<)(\d)', r'&lt;\2', file_content_new)
                file_content_new = re.sub(r'([^expression]>)(\d)', r'&gt;\2', file_content_new)            
                # file_content_new = re.sub(r'(<td>)(.*)(</td>)', r'', file_content_new)
                file_content_new = re.sub(r'(<td>)((\n.*)*)(</td>)', r'\1\3', file_content_new, flags=re.MULTILINE)
                file_content_new = re.sub(r'(<e>)(.*)(</e>)', r'', file_content_new)
                file_content_new = re.sub(r'(<e>)((\n.*)*)(</e>)', r'\1\3', file_content_new, flags=re.MULTILINE)
                file_content_new = re.sub(r'(==|!=)(")([^"]+)(")', r'\1&quot;\3&quot;', file_content_new)
                file_content_new = re.sub(r' \|\| ', r' ', file_content_new)
                file_content_new = re.sub(r' & ', r' &amp; ', file_content_new)
                file_content_new = re.sub(r'Hjernen&Hjertet', r'Hjernen&amp;Hjertet', file_content_new)
                file_content_new = re.sub(r'( {0,1})&& ', r'\1(&amp;&amp; ', file_content_new)
                file_content_new = re.sub(r'(expression=")(.*)(<)([^"]+)(" )', r'\1\2&lt;\4\5', file_content_new)
                file_content_new = re.sub(r'(expression=")(.*)(>)([^"]+)(" )', r'\1\2&gt;\4\5', file_content_new)
                file_content_new = re.sub(r'(expression=")([^"]+)( ")(.)([^"]+)(")(.)([^"]+)(" )', r'\1\2 &quot;\4\5&quot;\7\8\9', file_content_new)
                file_content_new = re.sub(r'(column|row|doubleValue)( {0,1})(<)', r'\1\2&lt;', file_content_new)
                file_content_new = re.sub(r'([^<^/]column|[^<^/]row|doubleValue)( {0,1})(>)', r'\1\2&gt;', file_content_new)            
        
        try:
            et.parse(full_path_to_file, parser).getroot()
            return et.parse(full_path_to_file, parser).getroot()
        except:
            logger.info(f'Malformed XML - trying to clean up the specification in {file_name}')
            tidy_xml(full_path_to_file)
            file_name_new = full_path_to_file + r'_cleaned'
            with codecs.open(file_name_new, mode=r'w', encoding=r'UTF-8-SIG') as text_file:
                text_file.write(file_content_new)
                text_file.close()
            return et.parse(file_name_new, parser).getroot()            
    
    def ext_attribs(element, type):

        var_ref = ''
        var_analysisId = ''
        var_type = ''
        var_name = ''        
        
        if element.get('variableName'):
            var_ref = element.get('variableName')
        if element.get('analysisID'):
            var_analysisId = element.get('analysisID')
        var_type = type
        df_row = {'ref':var_ref,
                    'analysisId':var_analysisId,                             
                    'type':var_type,
                    'name':var_name
                    }

        return df_row

    logger = logging.getLogger(__name__)
    file_name = f'{file_path}{os.path.sep}{report_spec}'
    root = parse_xml(file_name)
    tree = et.ElementTree(root)

    df_cols = ['ref', 'analysisId', 'type', 'name']
    df_rows = []

    for e in root.findall('.//question') + root.findall('.//questionOpenString'):
        e_path = tree.getpath(e)
        if r'/indicatorBank/' in e_path:
            df_rows.append(ext_attribs(e, r'Part of indicator'))
        elif r'/minRepliesIndicator/' in e_path:
            df_rows.append(ext_attribs(e, r'Used in minreplies element'))
        else:
            df_rows.append(ext_attribs(e, r'Used in graph element'))

    df_report_vars = pd.DataFrame(df_rows, columns=df_cols)

    # Only including variables with full reference - blank reference indicates, that the variable has been used previously (i.e. idref=XXX)
    df_report_vars = df_report_vars[df_report_vars['ref']!='']

    # Only keeping cases from the current analysis_id
    df_report_vars = df_report_vars[df_report_vars['analysisId']==str(analysis)]

    # Creating unique reference across analysisIds - used for merning information
    df_report_vars['analysis_var_ref'] = df_report_vars['analysisId'] + '_' + df_report_vars['ref']    
    
    # save_dataframe(df_report_vars, 999, r'reportVars')

    df_report_vars_calc = df_report_vars.loc[df_report_vars['ref'].str.startswith('{*3/', na=False)]

    # Merging fullName onto the variables
    df_vo_temp = var_overview[['adj_name', 'analysis_var_ref']]

    df_report_vars_calc = pd.merge(left=df_report_vars_calc, right=df_vo_temp, on='analysis_var_ref', how='left')

    logger.info(f'Done extracting variables from report specification: {file_name}')

    return df_report_vars_calc['adj_name'].tolist()