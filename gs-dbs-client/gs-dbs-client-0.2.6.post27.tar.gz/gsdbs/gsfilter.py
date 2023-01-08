import logging
import time


class GSDBSLogger(logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    pymssql required
    '''

    def __init__(self, sql_conn, sql_cursor, db_tbl_log):
        logging.Handler.__init__(self)
        self.sql_cursor = sql_cursor
        self.sql_conn = sql_conn
        self.db_tbl_log = db_tbl_log
        self.cnt = 0

    def emit(self, record, jobinfo):
        self.cnt += 1
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')
        # Make the SQL insert
        gql = f"""
           mutation{{
            addDTable(
                dtablename:"gscnodelog",
                superDTable:[DTABLE],
                sriBuildInfo:"${{jobid}}-${{groupid}}-${{computingstep}}-${{cnode}}-${{cnt}}",
                dataLinks:[ {{ alias:"jobid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"groupid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"computingstep",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"cnode",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"cnt",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"level",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"levelname",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"log",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"createdat",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}],
                data:[["jobid","groupid","computingstep","cnode","cnt","level","levelname","log","createdat"],
                      ["${jobinfo["jobid"]}"  ,"${""}"    ,"${""}"          ,"${""}"  ,"${""}","${""}"  ,"${""}"      ,"${""}","${""}"]]
            )
        }}
        """

#
logging.getLogger('').addHandler(logdb)
#
# logdb = GSDBSLogger(log_conn, log_cursor, db_tbl_log)
