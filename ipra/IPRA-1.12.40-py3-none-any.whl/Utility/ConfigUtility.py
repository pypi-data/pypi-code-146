import configparser

class _ConfigSingleton:
    _configInstance = None

    def __init__(self) -> None:
        self.config_obj = configparser.ConfigParser()
        self.config_obj.read("C:\IPRA\config.ini")
        pass


    def IsConfigExist(self,section,key):
        if not self.config_obj.has_section(section):
            return False
        else:
            if self.config_obj.has_option(section,key):
                return True
            else:
                return False
    
    def ReadConfig(self,section,key):
        #call IsConfigExist before
        return self.config_obj[section][key]
    
    def WriteConfig(self,section,key,value):
        if not self.config_obj.has_section(section):
            self.config_obj.add_section(section)


        self.config_obj.set(section=section,option=key,value=value)

        with open('C:\IPRA\config.ini', 'w') as configfile:
            self.config_obj.write(configfile)




def GetConfigSingletion():
    if _ConfigSingleton._configInstance is None:
        _ConfigSingleton._configInstance = _ConfigSingleton()
    return _ConfigSingleton._configInstance