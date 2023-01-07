from simple_ddl_parser import DDLParser
import pprint

result = DDLParser("""
 CREATE TABLE IF NOT EXISTS default.salesorderdetail(
                something<2% ARRAY<structcolx:string,coly:string>
                )
""", normalize_names=True).run(group_by_type=True)
# https://github.com/xnuinside/simple-ddl-parser/issues/145 
pprint.pprint(result) 
