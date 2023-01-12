import shutil
from yamlconfigs import Config

t = Config('./test.nginx.yaml',{'FM_NGINX_CONFIG': '/etc/nginx'})
print(t.__dict__)
t.native()

t = Config('./test_minidlna.yaml')
print(t.__dict__)
t.native()

print("")
print("MiniDLNA output")
print("------------")
with open("test_minidlna.conf") as f: # The with keyword automatically closes the file when you are done
    print (f.read())


# Backup files to be modified
shutil.copy('test_merge.ini','test_merge.bak')
shutil.copy('test_insert.ini','test_insert.bak')
t = Config('./test_ini.yaml',{'TEST_SUBST': 'environment_Value'})
print(t.__dict__)
t.native()

print("")
print("Merge output")
print("------------")
with open("test_merge.ini") as f: # The with keyword automatically closes the file when you are done
    print (f.read())

print("")
print("Insert output")
print("------------")
with open("test_insert.ini") as f: # The with keyword automatically closes the file when you are done
    print(f.read())

print("")
print("NGINX output")
print("------------")
with open("test.nginx.txt") as f: # The with keyword automatically closes the file when you are done
    print(f.read())
    
# Restore backups
shutil.copy('test_merge.bak','test_merge.ini')
shutil.copy('test_insert.bak','test_insert.ini')
 
t = Config('./test_samba.yaml')
print(t.__dict__)
t.native()
print("")
print("Samba config output")
print("-------------------")
with open("test_samba.conf") as f: # The with keyword automatically closes the file when you are done
    print(f.read())

t = Config('./test_menu.yaml')
print(t.__dict__)
t.native()
print("")
print("Samba config output")
print("-------------------")
with open("test_menu.conf") as f: # The with keyword automatically closes the file when you are done
    print(f.read())
