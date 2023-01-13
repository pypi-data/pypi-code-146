"""
ArcherAPI.ArcherServerClient

A wrapper class to simplify Archer API calls. The different Archer APIs do NOT
have feature parity. You will see calls to different Archer APIs in this class.

Methods that a user interacts with currently return the following types:
-- str
-- pandas.DataFrame

Types to avoid returning:
-- xml.etree.* (I personally do not find xml or this module intuitive.
                Please feel free to improve the code in this class.)

Available Archer APIs:
1) Web Services
2) RESTful
3) Content

See the Archer documentaion for more information.
"""
import re
import xml.etree.ElementTree as ET
import pandas as pd

try:
  import importlib.resources as pkg_resources
except ImportError:
  # Try backported to PY<37 'importlib_resources'.
  import importlib_resources as pkg_resources

# Relative Imports
from . import templates

class ArcherServerClient:
  """
  Get GUID of report. Used in future API queries, specifically to generate
  search options for Execute Search.

  API Used: Web Services

  Positional arguments:
  name -- Name of report.
  """
  def get_report_guid(self, name: str) -> str:
    url = f'{self.auth.base_url}/ws/search.asmx'

    body = f'''<GetReports xmlns="http://archer-tech.com/webservices/">
                 <sessionToken>{self.auth.token}</sessionToken>
               </GetReports>'''
    
    # All xml requests have the same envelope.
    data = ET.parse(pkg_resources.open_text(templates, 'template.xml'))
    
    # Insert body xml unique to this query.
    data.getroot().find(
      './/{http://schemas.xmlsoap.org/soap/envelope/}Body'
    ).append(ET.fromstring(body))

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/GetReports'
    }

    # ArcherAuth maintains the session state.
    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    # The root of our search is the result of our query.
    root = ET.fromstring(
      ET.fromstring(
        response.text
      ).find(
        './/{http://archer-tech.com/webservices/}GetReportsResult'
      ).text
    )

    # Map report name to GUID and lookup by name.
    guid = {element.find('ReportName').text: element.find('ReportGUID').text
            for element
            in root.findall('ReportValue')}[name]
    
    return guid

  """
  Get search options for Execute Search. Requires report GUID.
  Use get_report_guid if report name is known, but GUID is not.

  API Used: Web Services

  Positional arguments:
  guid -- GUID of report for which we return the associated Search Options.
  """
  def get_search_options(self, guid: str) -> str:
    url = f'{self.auth.base_url}/ws/search.asmx'    

    body = f'''<GetSearchOptionsByGuid 
                xmlns="http://archer-tech.com/webservices/">
                  <sessionToken>{self.auth.token}</sessionToken>
                  <searchReportGuid>{guid}</searchReportGuid>
               </GetSearchOptionsByGuid>'''
    
    data = ET.parse(pkg_resources.open_text(templates, 'template.xml'))
    
    data.getroot().find(
      './/{http://schemas.xmlsoap.org/soap/envelope/}Body'
    ).append(ET.fromstring(body))

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/GetSearchOptionsByGuid'
    }

    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    # Isolate Search Options returned by our query.
    options = ET.fromstring(
      ET.fromstring(
        response.text
      ).find(
        './/{http://archer-tech.com/webservices/}GetSearchOptionsByGuidResult'
      ).text
    )
    
    # This needs to be fixed for num_pages calculation in _search_pages
    options.find(
      './/PageSize'
    ).text = '1000' # If edited, you MUST edit _search_pages!

    # Return Search Options as str for use in Execute Search.
    return options

  """Method to standardize field names in returned Data Frames.
  Positional arguments:
  name -- Field name."""
  def _clean_field_name(self, name: str) -> str:
    return re.sub('\s+|\W+', '_', name.strip().lower())

  """Helper method for exec_search to query all pages.

  API Used: Web Services

  Positional arguments:
  url -- Post request url.
  data -- Post request data. pageNumber will always update to page_num.
  headers -- Post request headers.
  page_num -- Page number to query. Starts at 1, increments by 1.
  """
  def _search_pages(self, url: str, data: ET.ElementTree,
                    headers: dict, page_num: int) -> ET.ElementTree:
    data.find(
      './/{http://archer-tech.com/webservices/}pageNumber'
    ).text = str(page_num)

    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    result = ET.fromstring(
      ET.fromstring(
        response.text
      ).find('.//{http://archer-tech.com/webservices/}ExecuteSearchResult').text
    )

    # num_pages = Ceiling(Number of records / PageSize)
    num_pages = -(-int(result.attrib['count']) // 1000)

    if page_num == num_pages:
      return result
    else:
      search = self._search_pages(url, data, headers, page_num + 1)
      
      for record in result.findall('.//Record'):
        search.append(record)

      return search

  """Execute Search with provided Search Options.

  API Used: Web Services

  Positional arguments:
  options -- Search Options
  """
  def exec_search(self, options: ET.ElementTree) -> dict:
    url = f'{self.auth.base_url}/ws/search.asmx'    

    body = f'''<ExecuteSearch xmlns="http://archer-tech.com/webservices/">
                 <sessionToken>{self.auth.token}</sessionToken>
                 <searchOptions>
                   <![CDATA[{ET.tostring(options, encoding = 'unicode')}]]>
                 </searchOptions>
                 <pageNumber>1</pageNumber>
               </ExecuteSearch>'''
    
    data = ET.parse(pkg_resources.open_text(templates, 'template.xml'))
    
    data.getroot().find(
      './/{http://schemas.xmlsoap.org/soap/envelope/}Body'
    ).append(ET.fromstring(body))

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/ExecuteSearch'
    }

    result = self._search_pages(url, data, headers, 1)

    # Map field id to field name.
    map_fields = {
      field_def.attrib['id']: self._clean_field_name(field_def.attrib['name'])
      for field_def
      in result.findall('.//FieldDefinition')
    }

    search = {map_fields[field]: [] for field in map_fields}

    for record in result.findall('.//Record'):
      for field in record.findall('Field'):
        if field.attrib['id'] in map_fields:
          search[
            map_fields[field.attrib['id']]
          ].append(field.text)

    return search

  def get_history_logs(self) -> str:
    dfs = []

    for id in self.context['tracking_id']:
      url = f'{self.auth.base_url}/platformapi/core/content/history/{id}'
      headers = {'X-Http-Method-Override': 'GET'}
  
      response = self.auth.session.post(url, headers = headers)
      history_audits = response.json()[0]['RequestedObject']['HistoryAudits']

      for audit in history_audits:
        temp = []
        for field in audit['FieldHistory']:
          temp.append(audit['FieldHistory'][field])
        audit['FieldHistory'] = temp
    
      dfs.append(
        pd.json_normalize(
          history_audits,
          record_path = ['FieldHistory'],
          meta = ['Id',
                  'HistoryAction',
                  'Type',
                  'ContentId',
                  'ActionDate',
                  'ActionUserId']
        )
      )

    return pd.concat(dfs).reset_index(drop = True).rename(
      columns = lambda name: re.sub('(?<!^)(?=[A-Z])', '_', name).lower()
    )

  def get_context(self, report_name: str) -> pd.DataFrame:
    report_guid = self.get_report_guid(report_name)
    search_options = self.get_search_options(report_guid)

    return pd.DataFrame(self.exec_search(search_options))

  def __init__(self, auth: 'ArcherAuth') -> None:
    self.auth = auth
    # Context can be updated by calling get_context after instantiation.
    self.context = self.get_context('__api_facility__')