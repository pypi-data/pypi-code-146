# coding:utf-8
from tools_hjh.Log import Log
from tools_hjh.DBConn import DBConn
from tools_hjh.DBConn import QueryResults
from tools_hjh.MemoryDB import MemoryDB
from tools_hjh.Tools import line_merge_align, locatdate, merge_spaces, \
    analysis_hosts, locattime, remove_leading_space


def main():
    rows = []
    for idx in range(0, 10):
        row = (idx, idx, idx)
        rows.append(row)
    testDB = DBConn('sqlite', db='test.ora_conn')
    num = testDB.insert('t1', rows, 'c1')
    print(num)
    testDB.close()


class OracleTools:
    """ 用于Oracle的工具类 """

    @staticmethod
    def desc(ora_conn, username, table):
        """ 类似于sqlplus中的desc命令 """
        username = username.upper()
        table = table.upper()
        sql = '''
            select column_name, 
                case 
                    when data_type = 'VARCHAR2' or data_type = 'CHAR' or data_type = 'VARCHAR' then 
                        data_type || '(' || data_length || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale > 0 then 
                        data_type || '(' || data_precision || ', ' || data_scale || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale = 0 then 
                        data_type || '(' || data_precision || ')'
                    when data_type = 'NUMBER' and data_precision = 0 and data_scale = 0 then 
                        data_type
                    else data_type 
                end column_type
            from dba_tab_cols where owner = ? and table_name = ? and column_name not like '%$%' order by column_id
        '''
        tab = ''
        cols_ = ora_conn.run(sql, (username, table)).get_rows()
        lenNum = 0
        for col_ in cols_:
            if lenNum < len(col_[0]):
                lenNum = len(col_[0])
        for col_ in cols_:
            tablename = col_[0]
            typestr = col_[1]
            spacesnum = lenNum - len(tablename) + 1
            colstr = tablename + ' ' * (spacesnum) + typestr
            tab = tab + colstr + '\n'
        return tab
    
    @staticmethod
    def get_ddl(dba_conn, username, table):
        """ 需要dba权限，得到目标user.table的单元性的建表语句，包括约束，索引和注释等 """
        username = username.upper()
        table = table.upper()
        rssqls = []
        # 建表
        rssqls.append('create table ' + username + '.' + table + '(test_col number)')
        # 按顺序建列
        sql = '''
            select column_name, 
                case 
                    when data_type = 'VARCHAR2' or data_type = 'CHAR' or data_type = 'VARCHAR' or data_type = 'NVARCHAR2' then 
                        data_type || '(' || data_length || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale > 0 then 
                        data_type || '(' || data_precision || ', ' || data_scale || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale = 0 then 
                        data_type || '(' || data_precision || ')'
                    when data_type = 'NUMBER' and data_precision = 0 and data_scale = 0 then 
                        data_type
                    else data_type 
                end column_type
            from dba_tab_cols where owner = ? and table_name = ? and column_name not like '%$%' order by column_id
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add ' + r[0] + ' ' + r[1].strip())
        rssqls.append('alter table ' + username + '.' + table + ' drop column test_col')
        # 建主键
        sql = '''
            select t.constraint_name, to_char(wm_concat(t2.column_name)) cols
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'P'
            group by t.constraint_name
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add constraint ' + r[0] + ' primary key(' + r[1] + ')')
        # 建非空约束
        sql = '''
            select t.search_condition
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'C'
            and t.search_condition is not null
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            if 'IS NOT NULL' in r[0]:
                col = r[0].split(' ')[0]
                rssqls.append('alter table ' + username + '.' + table + ' modify ' + col + ' not null')
        # 建唯一约束
        sql = '''
            select t.constraint_name, to_char(wm_concat(t2.column_name)) cols
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'U'
            group by t.constraint_name
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add constraint ' + r[0] + ' unique(' + r[1] + ')')
        # 建默认值
        sql = '''
            select column_name, data_default
            from dba_tab_columns
            where owner = ? 
            and table_name = ? 
            and column_name not like '%$%'
            and data_default is not null
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' modify ' + r[0] + ' default ' + r[1].strip())
        # 建普通索引
        sql = '''
            select t.index_name, to_char(wm_concat(t2.column_name)) cols
            from dba_indexes t, dba_ind_columns t2
            where t.owner = ? 
            and t.table_name = ? 
            and t.index_name = t2.index_name
            and t.owner = t2.table_owner
            and t.uniqueness = 'NONUNIQUE'
            and t.index_type = 'NORMAL'
            group by t.index_name
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append('create index ' + username + '.' + r[0] + ' on ' + username + '.' + table + '(' + r[1] + ')')
        # 建函数索引
        sql = '''
            select t.index_name, t3.column_expression
            from dba_indexes t, dba_ind_expressions t3
            where t.owner = ? 
            and t.table_name = ? 
            and t.index_name = t3.index_name
            and t.table_name = t3.table_name
            and t.owner = t3.table_owner
            and t.uniqueness = 'NONUNIQUE'
            and t.index_type = 'FUNCTION-BASED NORMAL'
            order by t3.column_position
        '''
        col, rows = dba_conn.run(sql, (username, table))
        mdb = MemoryDB()
        mdb.set('t_idx', col, rows)
        rs = mdb.ora_conn.run('select index_name, group_concat(column_expression) from t_idx group by index_name').get_rows()
        mdb.close()
        for r in rs:
            rssqls.append('create index ' + username + '.' + r[0] + ' on ' + username + '.' + table + '(' + r[1] + ')')
        # 建注释
        sql = '''
            select column_name, comments
            from dba_col_comments
            where owner = ? 
            and table_name = ? 
            and comments is not null
        '''
        for r in dba_conn.run(sql, (username, table)).get_rows():
            rssqls.append("comment on column " + username + "." + table + "." + r[0] + " is '" + r[1] + "'")
        # 建外键
        pass
        return rssqls
    
    @staticmethod
    def get_dbms_ddl(dba_conn, username, table):
        """ 得到目标user.table的的建表语句，直接调用dbms_metadata.get_ddl得到结果 """
        username = username.upper()
        table = table.upper()
        sql = '''
            select to_char(
                dbms_metadata.get_ddl('TABLE', ?, ?)
            ) from dual
        '''
        return dba_conn.run(sql, (table, username)).get_rows()[0]
    
    @staticmethod
    def compare_table(src_dba_conn, src_username, dst_dba_conn, dst_username):
        """ 比较两个不同用户下同名表表结构，输出不一致的表清单，和一段报告 """
        src_username = src_username.upper()
        dst_username = dst_username.upper()
        out = ''
        table_list = []
        sql = 'select table_name from dba_tables where owner = ?'
        srctabs = src_dba_conn.run(sql, (src_username,)).get_rows()
        for tab in srctabs:
            src_desc = OracleTools.desc(src_dba_conn, src_username, tab[0])
            dst_desc = OracleTools.desc(dst_dba_conn, dst_username, tab[0])
            if src_desc != dst_desc:
                table_list.append(tab[0])
                out = out + line_merge_align(src_username + '.' + tab[0] + '\n' + src_desc
                                           , dst_username + '.' + tab[0] + '\n' + dst_desc
                                           , True) + '\n\n'
        return table_list, out
    
    '''
    @staticmethod
    def sync_table(src_ora_conn, src_username, dst_ora_conn, dst_username, table, mode=1):
        """ 同步表，mode：
        0：仅输出增量同步表结构的sql
        1：增量同步表结构
        2：重建表结构，不包含外键
        3：重建表，且同步数据，数据量大的问题暂没考虑 """
        report = ''
        if mode == 0:
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                report = report + sql + ';\n'
        if mode == 1:
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                try:
                    dst_ora_conn.run(sql)
                    report = report + 'ok:' + sql + '\n'
                except:
                    report = report + 'err:' + sql + '\n'
        if mode == 2:
            try:
                sql = 'drop table ' + dst_username + '.' + table
                dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
            except:
                report = report + 'err:' + sql + '\n'
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
        if mode == 3:
            try:
                sql = 'drop table ' + dst_username + '.' + table + ' cascade constraints purge'
                # dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
            except:
                report = report + 'err:' + sql + '\n'
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                try:
                    # dst_ora_conn.run(sql)
                    report = report + 'ok:' + sql + '\n'
                except:
                    report = report + 'err:' + sql + '\n'
            sql = 'select * from ' + src_username + '.' + table
            conn = src_ora_conn.dbpool.acquire()
            cur = conn.cursor()
            cur.execute(sql)
            while True:
                rs = cur.fetchone()
                if rs is not None:
                    pa = str(rs)
                    sql = 'insert into ' + dst_username + '.' + table + ' values' + pa
                    # dst_ora_conn.run(sql)
                    print(sql)
                else:
                    break
            cur.close()
            conn.close()
        return report
    '''
   
    @staticmethod
    def get_sids_by_host(host_conn):
        """ 根据给入的linux系统tools_hjh.SSHConn对象获取这台主机运行的全部SID实例名称 """
        try:
            sids = []
            pros = host_conn.exec_command("source .bash_profile && cd $ORACLE_HOME/dbs && ls -l init*.ora | awk '{print $9}'").split('\n')
            for pro in pros:
                sid = pro.replace('init', '').replace('.ora', '')
                if len(sid) > 0:
                    sids.append()
        except:
            sids = []
            pros = host_conn.exec_command("ps -ef | grep ora_smon | grep -v grep | awk '{print $8}'").split('\n')
            for pro in pros:
                sids.append(pro.replace('ora_smon_', ''))
        return sids

    @staticmethod
    def get_obj_size(dba_conn):
        """ 得到对象(table、index、lob)大小 """
        sql = '''
            select (select utl_inaddr.get_host_address from dual) ip
            , (select global_name from global_name) service_name
            , t2.owner owner_user
            , t3.account_status user_status
            , to_char(nvl(t3.lock_date, t3.expiry_date), 'yyyy-mm-dd hh24:mi:ss') lock_or_expiry_date
            , t.tablespace_name owner_tablespace
            , t2.table_name owner_table
            , t2.obj_name
            , t2.obj_type
            , sum(t.bytes) / 1024 / 1024 size_m
            from dba_segments t, (
                select table_owner owner, table_name, index_name obj_name, 'INDEX' obj_type from dba_indexes
                union all
                select owner, table_name, segment_name obj_name, 'LOB' obj_type from dba_lobs
                union all
                select owner, table_name, table_name, 'TABIE' obj_type from dba_tables
            ) t2, dba_users t3 
            where t.owner = t2.owner
            and t.segment_name = t2.obj_name
            and t3.username = t2.owner
            group by t2.owner, t.tablespace_name, t2.table_name, t2.obj_name, t2.obj_type
            , t3.account_status, t3.lock_date, t3.expiry_date
        '''
        return dba_conn.run(sql)
    
    @staticmethod
    def get_data_file_size(dba_conn):
        """ 得到数据文件大小 """
        sql = '''
            select (select utl_inaddr.get_host_address from dual) ip
            , (select global_name from global_name) service_name
            , t2.tablespace_name 
            , t2.file_name
            , t2.file_id
            , t2.bytes / 1024 / 1024 all_size_m
            , max(t.block_id) * 8 / 1024 occupy_size_m
            , sum(t.bytes) / 1024 / 1024 use_size_m
            from dba_extents t, dba_data_files t2
            where t.file_id = t2.file_id
            group by t2.tablespace_name, t2.file_name, t2.file_id, t2.bytes
        '''
        return dba_conn.run(sql)
    
    @staticmethod   
    def expdp_estimate(host_conn, sid, users='', estimate='statistics'):
        """ 评估导出的dmp文件大小, users不填会使用full=y, estimate=statistics|blocks """
        date_str = locatdate()
        ip = host_conn.host
        if users == '':
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                full=y \\
                estimate_only=y \\
                estimate=''' + estimate + '''
            '''
        else:
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                schemas=''' + users + ''' \\
                estimate_only=y \\
                estimate=''' + estimate + '''
            '''  
        mess = host_conn.exec_script(sh)
        size = None
        rs_list = []
        if 'successfully completed' in mess:
            size = mess.split('method: ')[-1].split('\n')[0]
            lines = mess.replace('\n', '').split('.  estimated')
            for line in lines:
                if 'Total' in line or 'expdp' in line:
                    pass
                else:
                    line = merge_spaces(line.replace('"', '')).strip()
                    user_name = line.split(' ')[0].split('.')[0]
                    obj_name = line.split(' ')[0].split('.')[1]
                    obj_size = line.split(' ')[1]
                    dw = line.split(' ')[2]
                    if ':' in obj_name:
                        fq_name = obj_name.split(':')[1]
                        tab_name = obj_name.split(':')[0]
                    else:
                        tab_name = obj_name
                        fq_name = tab_name
                    if dw == 'GB':
                        obj_size = float(obj_size) * 1024
                    elif dw == 'KB':
                        obj_size = float(obj_size) / 1024
                    rs_list.append((date_str, ip, sid, user_name, tab_name, fq_name, obj_size))
        elif 'elapsed 0' in mess:
            size = mess.split('TATISTICS : ')[-1].split('\n')[0]
            lines = mess.split('\n')
            
            for line in lines:
                if '.   "' in line:
                    line = merge_spaces(line.replace('"', '').replace('\n', '')).strip()
                    user_name = line.split(' ')[1].split('.')[0]
                    obj_name = line.split(' ')[1].split('.')[1]
                    obj_size = line.split(' ')[2]
                    dw = line.split(' ')[3]
                    if ':' in obj_name:
                        fq_name = obj_name.split(':')[1]
                        tab_name = obj_name.split(':')[0]
                    else:
                        tab_name = obj_name
                        fq_name = tab_name
                    if dw == 'GB':
                        obj_size = float(obj_size) * 1024
                    elif dw == 'KB':
                        obj_size = float(obj_size) / 1024
                    rs_list.append((date_str, ip, sid, user_name, tab_name, fq_name, obj_size))
                    
        size = size.replace('\n', '').strip()
        return size, rs_list, mess
    
    @staticmethod   
    def expdp_job(sid, users=''):
        date_str = locatdate()
        if users == '':
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                full=y \\
                directory=DUMP \\
                dumpfile=''' + sid + '_' + date_str + '''.dmp
            '''
        else:
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                schemas=''' + users + ''' \\
                directory=DUMP \\
                dumpfile=''' + sid + '_' + date_str + '''.dmp
            '''  
        
        return remove_leading_space(sh)
    
    @staticmethod  
    def expdp(src_host_conn, src_dba_conn, src_ora_sid, src_ora_user='', dump_tmp_py='/tmp/oracle_dump_py'):
        if src_ora_user == '':
            src_ora_user = 'all'
        date_str = locatdate()
        dump_filename = src_ora_user + '_' + date_str + '.dmp'
        log = Log('logs/expdp.log')
        src_ora_user = ''
        
        # 源端创建DUMP_TMP_PY
        src_host_ip = src_host_conn.host
        try:
            src_dba_conn.run('drop directory DUMP_TMP_PY')
        except Exception as e:
            pass
        try:
            src_dba_conn.run("create directory DUMP_TMP_PY as '" + dump_tmp_py + "'")
            log.info('源端', src_host_ip, 'DUMP_TMP_PY 创建成功')
        except Exception as e:
            log.error('源端', src_host_ip, 'DUMP_TMP_PY 创建失败，程序终止', e)
            log.error(str(e))
            return False
        
        # 源端导出dmp
        if src_ora_user != '':
            sh = '''
                rm -f ''' + dump_tmp_py + '''/{dump_filename}
                source ~/.bash_profile
                export ORACLE_SID={oracle_sid}
                expdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} schemas={src_ora_user} compression=all cluster=n parallel=4
            '''
        else:
            sh = '''
                rm -f ''' + dump_tmp_py + '''/{dump_filename}
                source ~/.bash_profile
                export ORACLE_SID={oracle_sid}
                expdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} full=y compression=all cluster=n parallel=4
            '''
        sh = sh.replace('{oracle_sid}', src_ora_sid)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{src_ora_user}', src_ora_user)
        mess = src_host_conn.exec_script(sh)
        if 'successfully completed' in mess:
            log.info('源端', src_host_ip, 'DMP导出成功')
        else:
            log.error('源端', src_host_ip, 'DMP导出失败，程序终止')
            log.error(mess)
            return False
        return True

    @staticmethod     
    def expdp_scp_impdp(src_host_conn, src_dba_conn, src_ora_sid, src_ora_user, dst_host_conn, dst_dba_conn, dst_ora_sid, dump_tmp_py='/tmp/oracle_dump_py'):
        """ 
        0.需要事项创建好表空间, src_ora_user给入''表示full=y
        1.源端和目标端新建 directory DUMP_TMP_PY /tmp/oracle_dump_py
        2.源端获取 需要导出用户的表空间名称和大小
        3.源端执行 expdp 导出数据文件到 DUMP_TMP_PY
        4.scp文件到目标端 dump_tmp_py
        5.目标端执行 impdp 导入数据文件
        """
        if src_ora_user == '':
            src_ora_user = 'all'
        date_str = locatdate()
        dump_filename = src_ora_user + '_' + date_str + '.dmp'
        dump_logname = src_ora_user + '_' + date_str + '.log'
        log = Log('logs/expdp_scp_impdp.log')
        src_ora_user = ''
        
        # 源端创建DUMP_TMP_PY
        src_host_ip = src_host_conn.host
        try:
            src_dba_conn.run('drop directory DUMP_TMP_PY')
        except Exception as e:
            pass
        try:
            src_dba_conn.run("create directory DUMP_TMP_PY as '" + dump_tmp_py + "'")
            log.info('源端', src_host_ip, 'DUMP_TMP_PY 创建成功')
        except Exception as e:
            log.error('源端', src_host_ip, 'DUMP_TMP_PY 创建失败，程序终止', e)
            log.error(str(e))
            return False
        
        # 目标端创建DUMP_TMP_PY
        dst_host_ip = dst_host_conn.host
        try:
            dst_dba_conn.run('drop directory DUMP_TMP_PY')
        except Exception as e:
            pass
        try:
            dst_dba_conn.run("create directory DUMP_TMP_PY as '" + dump_tmp_py + "'")
            log.info('目标端', dst_host_ip, 'DUMP_TMP_PY 创建成功')
        except Exception as e:
            log.error('目标端', dst_host_ip, 'DUMP_TMP_PY 创建失败，程序终止', e)
            log.error(str(e))
            return False
        
        # 源端导出dmp
        if src_ora_user != '':
            sh = '''
                rm -f ''' + dump_tmp_py + '''/{dump_filename}
                source ~/.bash_profile
                export ORACLE_SID={oracle_sid}
                expdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} schemas={src_ora_user} compression=all cluster=n parallel=4
            '''
        else:
            sh = '''
                rm -f ''' + dump_tmp_py + '''/{dump_filename}
                source ~/.bash_profile
                export ORACLE_SID={oracle_sid}
                expdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} full=y compression=all cluster=n parallel=4
            '''
        sh = sh.replace('{oracle_sid}', src_ora_sid)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{src_ora_user}', src_ora_user)
        mess = src_host_conn.exec_script(sh)
        if 'successfully completed' in mess:
            log.info('源端', src_host_ip, 'DMP导出成功')
        else:
            log.error('源端', src_host_ip, 'DMP导出失败，程序终止')
            log.error(mess)
            return False

        # scp到目标端
        sh = '''
            source ~/.bash_profile
            expect -c "
            spawn scp -P {dst_host_port} -r ''' + dump_tmp_py + '''/{dump_filename} {dst_host_user}@{dst_host_ip}:''' + dump_tmp_py + '''/
            expect {
                \\"*assword\\" {set timeout 30; send \\"{dst_host_password}\\r\\";}
                \\"yes/no\\" {send \\"yes\\r\\"; exp_continue;}
            }
            expect eof"
        '''
        dst_host_port = dst_host_conn.port
        dst_host_user = dst_host_conn.username
        dst_host_password = dst_host_conn.password
        sh = sh.replace('{dst_host_port}', dst_host_port)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{dst_host_user}', dst_host_user)
        sh = sh.replace('{dst_host_ip}', dst_host_ip)
        sh = sh.replace('{dst_host_password}', dst_host_password)
        mess = src_host_conn.exec_script(sh)
        if '100%' in mess:
            log.info('源端', src_host_ip, 'SCP成功')
        else:
            log.error('源端', src_host_ip, 'SCP失败，程序终止')
            log.error(mess)
            return False
        
        # 目标端导入dmp
        sh = '''
            source ~/.bash_profile
            export ORACLE_SID={oracle_sid}
            impdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} logfile={dump_logname} full=y transform=segment_attributes:n table_exists_action=replace
        '''
        sh = sh.replace('{oracle_sid}', dst_ora_sid)
        sh = sh.replace('{src_ora_user}', src_ora_user)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{dump_logname}', dump_logname)
        mess = dst_host_conn.exec_script(sh)
        if 'completed' in mess:
            log.info('目标端', dst_host_ip, 'DMP导入结束')
        else:
            log.error('目标端', dst_host_ip, 'DMP导入失败，程序终止')
            log.error(mess)
            return False
        return True
        
    @staticmethod
    def analysis_tns(host_conn):
        """ 解析Oracle tnsnames.ora文件 """
        """ tns_name, ip, port, sid, service_name """
        host_map = analysis_hosts(host_conn)
        cmd = '''source ~/.bash_profile;cat $ORACLE_HOME/network/admin/tnsnames.ora'''
        tns_str = host_conn.exec_command(cmd)
        tns_str2 = ''
        tns_list = []
        tnss = {}
        for line in tns_str.split('\n'):
            if not line.startswith('#'):
                tns_str2 = tns_str2 + line + '\n'
        tns_str2 = tns_str2.replace('\n', ' ')
        tns_str2 = merge_spaces(tns_str2)
        for s in tns_str2.split(') ) )'):
            s = s.replace(' ', '')
            if len(s) > 0:
                tns_list.append(s + ')))')
        for tns_s in tns_list:
            sid = ''
            service_name = ''
            tns_name = tns_s.split('=')[0]
            tns_s = tns_s.replace(tns_name + '=', '')  # 避免tns_name里面含有关键字
            if 'SID=' in tns_s:
                sid = tns_s.split('SID=')[1].split(')')[0]
            elif 'SERVICE_NAME=' in tns_s:
                service_name = tns_s.split('SERVICE_NAME=')[1].split(')')[0]
            tns_host = tns_s.split('HOST=')
            for idx in range(1, len(tns_host)):
                host = tns_host[idx].split(')')[0]
                try:
                    host = host_map[host]
                except:
                    pass
                port = tns_s.split('PORT=')[idx].split(')')[0]
                tnss[tns_name.lower()] = (host, port, service_name.lower(), sid.lower())
        return tnss

    @staticmethod     
    def analysis_ogg_status(host_conn):
        """ 进入主机全部找到的ggsci，执行info all 返回结果 """
        query_time = locattime()
        host = host_conn.host
        
        # 进程状态 
        # 查询时间 ogg所在主机HOST ggsci所在路径 进程类型 进程状态 进程名称 lag_at_chkpt time_since_chkpt
        ogg_status = QueryResults()
        ogg_status.set_cols(('query_time', 'host', 'ggsci_path', 'type', 'status', 'name', 'lag_at_chkpt', 'time_since_chkpt'))
        
        # 解析进程状态 
        cmd = 'locate *ggsci'
        paths = host_conn.exec_command(cmd)
        for path in paths.split('\n'):
            cmd = 'source ~/.bash_profile;echo "info all" | ' + path
            mess = host_conn.exec_command(cmd)
            for line in mess.split('\n'):
                if line.startswith('MANAGER'):
                    lines = merge_spaces(line).split(' ')
                    ogg_status.get_rows().append((query_time, host, path, lines[0].lower(), lines[1].lower()))
                elif line.startswith('EXTRACT') or line.startswith('REPLICAT'):
                    lines = merge_spaces(line).split(' ')
                    ogg_status.get_rows().append((query_time, host, path, lines[0].lower(), lines[1].lower(), lines[2].lower(), lines[3], lines[4]))
        
        return ogg_status
    
    @staticmethod     
    def analysis_ogg_info(host_conn):
        """ 对主机所有找到的ggsci，搜寻全部ogg进程的基本信息 """
        host = host_conn.host
        tns_list = OracleTools.analysis_tns(host_conn)
        
        # 进程状态 
        # 查询时间 ogg所在主机HOST ggsci所在路径 进程类型 进程状态 进程名称 lag_at_chkpt time_since_chkpt
        ogg_status = OracleTools.analysis_ogg_status(host_conn)
        
        # 进程信息 
        ogg_info = []
        
        # ORACLE_SID
        default_sid = host_conn.exec_command('source ~/.bash_profile;echo $ORACLE_SID')
        
        # 解析进程信息
        for ogg in ogg_status.get_rows():
            if ogg[3] != 'manager':
                ggsci_path = ogg[2]
                pro_name = ogg[5]
                cmd1 = 'source ~/.bash_profile;echo "view param ' + pro_name + '" | ' + ggsci_path
                cmd2 = 'source ~/.bash_profile;echo "info ' + pro_name + ' showch" | ' + ggsci_path
                param = host_conn.exec_command(cmd1)
                showch = host_conn.exec_command(cmd2)
                
                ogg_type = ''
                
                for line in param.split('\n'):
                    line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                    if line_.startswith('extract '):
                        ogg_type = 'ext_or_dmp'
                    elif line_.startswith('replicat '):
                        ogg_type = 'rep_or_rep2kafka'
                    elif line_.startswith('rmthost ') and ogg_type == 'ext_or_dmp':
                        ogg_type = 'dmp'
                        break
                    elif line_.startswith('exttrail ') and ogg_type == 'ext_or_dmp':
                        ogg_type = 'ext'
                        break
                    elif line_.startswith('userid ') and ogg_type == 'rep_or_rep2kafka':
                        ogg_type = 'rep'
                        break
                    elif line_.startswith('targetdb ') and ogg_type == 'rep_or_rep2kafka':
                        ogg_type = 'rep2kafka'
                        break
                
                if ogg_type == 'ext':
                    ext_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_tables':[], 'write_file':''}
                    ext_info['host'] = host
                    ext_info['ggsci_path'] = ggsci_path
                    ext_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('extract '):
                            ext_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    ext_info['ora_host'] = tns_list[tns_name][0]
                                    ext_info['ora_port'] = tns_list[tns_name][1]
                                    ext_info['ora_service_name'] = tns_list[tns_name][2]
                                    ext_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    ext_info['ora_host'] = ''
                                    ext_info['ora_port'] = ''
                                    ext_info['ora_service_name'] = ''
                                    ext_info['ora_sid'] = ''
                            else:
                                ext_info['ora_host'] = host
                                ext_info['ora_port'] = '1521'
                                ext_info['ora_service_name'] = ''
                                ext_info['ora_sid'] = default_sid
                        elif line_.startswith('table '):
                            ext_info['read_tables'].append(line_.split(' ')[1].replace(';', '').replace('"', '').strip().lower())
                    # write_file
                    try:
                        write_ = showch.split('Write Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if write_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            write_ = write_.replace('./', base_path)
                    except:
                        write_ = ''
                    ext_info['write_file'] = write_
                    ogg_info.append(ext_info)
                    # print(ext_info)
                    
                elif ogg_type == 'dmp':
                    dmp_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_tables':[], 'read_file':'', 'write_host':'', 'write_port':'', 'write_file':''}
                    dmp_info['host'] = host
                    dmp_info['ggsci_path'] = ggsci_path
                    dmp_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('extract '):
                            dmp_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    dmp_info['ora_host'] = tns_list[tns_name][0]
                                    dmp_info['ora_port'] = tns_list[tns_name][1]
                                    dmp_info['ora_service_name'] = tns_list[tns_name][2]
                                    dmp_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    dmp_info['ora_host'] = ''
                                    dmp_info['ora_port'] = ''
                                    dmp_info['ora_service_name'] = ''
                                    dmp_info['ora_sid'] = ''
                            else:
                                dmp_info['ora_host'] = host
                                dmp_info['ora_port'] = '1521'
                                dmp_info['ora_service_name'] = ''
                                dmp_info['ora_sid'] = default_sid
                        elif line_.startswith('table '):
                            dmp_info['read_tables'].append(line_.split(' ')[1].replace(';', '').replace('"', '').strip().lower())
                        elif line_.startswith('rmthost '):
                            try:
                                dmp_info['write_host'] = line_.split(',')[0].split(' ')[1]
                                dmp_info['write_port'] = line_.split(',')[1].split(' ')[1]
                            except:
                                dmp_info['write_host'] = line_.split(' ')[1]
                                dmp_info['write_port'] = line_.split(' ')[3]
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    dmp_info['read_file'] = read_
                    # write_file
                    try:
                        write_ = showch.split('Write Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if write_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            write_ = write_.replace('./', base_path)
                    except:
                        write_ = ''
                    dmp_info['write_file'] = write_
                    ogg_info.append(dmp_info)
                    # print(dmp_info)
                    
                elif ogg_type == 'rep':
                    rep_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_file':'', 'write_table_maps':[], 'exclude_table_maps':[]}
                    rep_info['host'] = host
                    rep_info['ggsci_path'] = ggsci_path
                    rep_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('replicat '):
                            rep_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    rep_info['ora_host'] = tns_list[tns_name][0]
                                    rep_info['ora_port'] = tns_list[tns_name][1]
                                    rep_info['ora_service_name'] = tns_list[tns_name][2]
                                    rep_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    rep_info['ora_host'] = ''
                                    rep_info['ora_port'] = ''
                                    rep_info['ora_service_name'] = ''
                                    rep_info['ora_sid'] = ''
                            else:
                                rep_info['ora_host'] = host
                                rep_info['ora_port'] = '1521'
                                rep_info['ora_service_name'] = ''
                                rep_info['ora_sid'] = default_sid
                        elif line_.startswith('map ') and 'target ' in line_:
                            line_ = line_.replace(',', ' ')
                            line_ = merge_spaces(line_)
                            m = line_.split(' ')[1].replace('"', '')
                            t = line_.split(' ')[3].replace(';', '').replace('"', '').strip().lower()
                            rep_info['write_table_maps'].append((m, t))
                        elif line_.startswith('mapexclude '):
                            t = line_.split(' ')[1].replace(';', '').strip().lower()
                            rep_info['exclude_table_maps'].append(t)
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    rep_info['read_file'] = read_
                    ogg_info.append(rep_info)
                    # print(rep_info)
                            
                elif ogg_type == 'rep2kafka':
                    rep2kafka_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'read_file':'', 'write_table_maps':[], 'exclude_table_maps':[]}
                    rep2kafka_info['host'] = host
                    rep2kafka_info['ggsci_path'] = ggsci_path
                    rep2kafka_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('replicat '):
                            rep2kafka_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('map ') and 'target ' in line_:
                            line_ = line_.replace(',', ' ')
                            line_ = merge_spaces(line_)
                            m = line_.split(' ')[1].replace('"', '')
                            t = line_.split(' ')[3].replace(';', '').replace('"', '').strip().lower()
                            rep2kafka_info['write_table_maps'].append((m, t))
                        elif line_.startswith('mapexclude '):
                            t = line_.split(' ')[1].replace(';', '').strip().lower()
                            rep2kafka_info['exclude_table_maps'].append(t)
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    rep2kafka_info['read_file'] = read_
                    ogg_info.append(rep2kafka_info)
                    # print(rep2kafka_info)
                    
        return ogg_info


if __name__ == '__main__':
    main()
