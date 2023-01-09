import dbhydra.dbhydra_core as dh


db1=dh.Mysqldb("config-mysql-forloop.ini")




table_dict=db1.generate_table_dict()





machines_table=table_dict["machines"]




result=machines_table.select_to_df()


list1=[[12,"127.0.0.1","jsdfhvdj","afhdfjvk",1,1,1688456875]]


machines_table.insert(list1)





machines_table




db1.execute("SELECT * FROM jkfvhfdkjhvdkfjvhkjf")







db1.close_connection()
