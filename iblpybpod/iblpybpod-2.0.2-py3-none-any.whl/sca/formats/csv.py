from sca import format_flags as flags
from dateutil import parser
import csv as csv, uuid, datetime, hashlib, os, sys
from sca.utils import hash_utils


csv.field_size_limit(10000000)

CSV_DELIMITER = ';'
CSV_QUOTECHAR = '|'
CSV_QUOTING   = csv.QUOTE_MINIMAL
CSV_LINETERMINATOR = '\n'

class writer(object):

    def __init__(self, filestream, uuid4_id=None, columns_headers=None, def_url=None, def_text=None, software=None, update=False):
        self.filestream      = filestream
        self.csvwriter       = csv.writer(filestream, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR, quoting=CSV_QUOTING, lineterminator=CSV_LINETERMINATOR)
        self.uuid4           = str(uuid.uuid4() if uuid4_id is None else uuid4_id)
        self.columns_headers = columns_headers
        
        if update:
            self.csvwriter.writerow([flags.UPDATED_ON_FLAG, datetime.datetime.now()])
        else:
            self.csvwriter.writerow([flags.UUID4_FLAG, self.uuid4])
            self.csvwriter.writerow([flags.CREATED_ON_FLAG, datetime.datetime.now()])
            
            if def_url:  self.__add_def_url(def_url)
            if def_text: self.__add_def_text(def_text)

        if software: self.csvwriter.writerow([flags.SOFTWARE_REF_FLAG, software])
       
        self._write_header = True if columns_headers else False

    def __add_def_url(self, def_url):
        self.csvwriter.writerow([flags.DEFINITION_URL_FLAG, def_url])

    def __add_def_text(self, def_text):
        self.csvwriter.writerow([flags.DEFINITION_TEXT_FLAG, def_text])

    def add_parent_ref(self, ref_uuid4):
        self.csvwriter.writerow([flags.PARENT_REF_FLAG, ref_uuid4])

    def add_external_ref(self, ref_uuid4):
        self.csvwriter.writerow([flags.EXTERNAL_REF_FLAG, ref_uuid4])

    def add_external_url(self, url):
        self.csvwriter.writerow([flags.EXTERNAL_URL_FLAG, url])

    def add_external_file(self, filepath):
        filename, hash_algorithm, hash_value = hash_utils.calculate_hash(filepath)

        self.csvwriter.writerow([flags.EXTERNAL_FILE_FLAG, filename, hash_algorithm, hash_value])

    def writerow(self, row): 
        if self._write_header: 
            self.csvwriter.writerow([flags.HAS_HEADER_FLAG])
            self.csvwriter.writerow(self.columns_headers)
            self._write_header = False

        self.csvwriter.writerow(row)



    def flush(self):
        self.filestream.flush()






class reader(object):

    def __init__(self, filestream):
        self.csvreader  = csv.reader(filestream, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR, quoting=CSV_QUOTING, lineterminator=CSV_LINETERMINATOR)
        
        self.uuid4      = None
        self.created_on = None
        self.updated_on = None
        self.parents    = None
        self.externals  = None
        self.software   = None
        self.def_text   = None
        self.def_url    = None
        self.external_urls  = None
        self.external_files = None
        self.columns_headers = None

        self.metadata_countrows = 0 #stores when the row data starts
        self._read_metadata     = True

    def __iter__(self): return self

    def __next__(self):
        row = next(self.csvreader, None)

        if row is None: raise StopIteration
        
        if self._read_metadata:
            self._read_metadata = self.__checkfor_flags(row)
            while( self._read_metadata ):
                # count the number of metadata rows
                self.metadata_countrows +=1
                row = next(self.csvreader, None)
                self._read_metadata = self.__checkfor_flags(row)
                if row is None: raise StopIteration

        return row

    def __checkfor_flags(self, row):
        if len(row)==0: return False
       
        if row[0] == flags.UUID4_FLAG:
            self.uuid4 = row[1]
            return True

        elif row[0] == flags.CREATED_ON_FLAG:
            self.created_on = parser.parse(row[1])
            return True

        elif row[0] == flags.UPDATED_ON_FLAG:         
            if self.updated_on is None: self.updated_on = []
            self.updated_on.append(parser.parse(row[1]))
            return True

        elif row[0] == flags.SOFTWARE_REF_FLAG:
            self.software = row[1]
            return True

        elif row[0] == flags.PARENT_REF_FLAG:
            if self.parents is None: self.parents = []
            self.parents.append(row[1])
            return True

        elif row[0] == flags.EXTERNAL_REF_FLAG:
            if self.externals is None: self.externals = []
            self.externals.append(row[1])
            return True

        elif row[0] == flags.EXTERNAL_URL_FLAG:
            if self.external_urls is None: self.external_urls = []
            self.external_urls.append(row[1:])
            return True

        elif row[0] == flags.EXTERNAL_FILE_FLAG:
            if self.external_files is None: self.external_files = []
            self.external_files.append(row[1:])
            return True

        elif row[0] == flags.DEFINITION_TEXT_FLAG:
            self.def_text = row[1]
            return True

        elif row[0] == flags.DEFINITION_URL_FLAG:
            self.def_url = row[1]
            return True

        elif row[0] == flags.HAS_HEADER_FLAG:
            self.columns_headers = next(self.csvreader, None)
            return True

        return False

    @staticmethod
    def count_metadata_rows(filename):
        count = 0
        with open(filename) as filestream:
            csvreader = csv.reader(filestream, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR, quoting=CSV_QUOTING, lineterminator=CSV_LINETERMINATOR)
            for i, row in enumerate(csvreader):
                if i>20: break
                
                if row[0] in [
                    flags.UUID4_FLAG,
                    flags.CREATED_ON_FLAG,
                    flags.UPDATED_ON_FLAG,
                    flags.SOFTWARE_REF_FLAG,
                    flags.PARENT_REF_FLAG,
                    flags.EXTERNAL_REF_FLAG,
                    flags.EXTERNAL_FILE_FLAG,
                    flags.EXTERNAL_URL_FLAG,
                    flags.DEFINITION_TEXT_FLAG,
                    flags.DEFINITION_URL_FLAG,
                    flags.HAS_HEADER_FLAG
                ]: 
                    count += 1
                else:
                    return count
        return count


