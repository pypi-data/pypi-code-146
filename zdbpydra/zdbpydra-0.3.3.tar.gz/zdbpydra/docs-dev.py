class CsvBuilder:

    def __init__(self, data):
        self.header = CSV_HEADER
        self._source = TitleResponseParser(data)

    @property
    def row(self):
        return [
          self._source.identifier or "",
          self._source.pica.idn or "",
          self._source.pica.oclc_joined or "",
          self._source.pica.loc_joined or "",
          self._source.pica.coden or "",
          self._source.pica.title or "",
          self._source.pica.title_supplement_joined or "",
          self._source.pica.title_responsibility or "",
          self._source.medium or "",
          self._source.pica.issn_joined or "",
          self._source.pica.issn_l or "",
          self._source.pica.publisher_joined or "",
          self._source.pica.publisher_place_joined or "",
          self._source.pica.product_code_joined or "",
          self._source.pica.zdb_code_joined or "",
          self._source.pica.bbg or "",
          self._source.pica.dewey_joined or "",
          self._source.pica.access_status_joined or "",
          self._source.pica.access_rights_joined or "",
          self._source.pica.access_source_joined or "",
          self._source.pica.parallel_id_joined or "",
          self._source.pica.parallel_idn_joined or "",
          self._source.pica.parallel_issn_joined or "",
          self._source.pica.parallel_bbg_joined or "",
          self._source.pica.parallel_type_joined or ""
        ]