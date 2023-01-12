import os
import yaml


local_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(local_path)


class Config:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'conf.yml')

    def get(self, module, key):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
            return yaml_data[module][key]
        except Exception as e:
            print(e)
            return None

    def set(self, module, key, value):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
            yaml_data[module][key] = value
            with open(self.file_path, 'w', encoding="utf-8") as f:
                yaml.dump(yaml_data, f)
        except Exception as e:
            print(e)

    def get_platform(self):
        return self.get('common', 'platform')

    def get_device(self):
        return self.get('app', 'device_id')

    def get_pkg(self):
        return self.get('app', 'pkg_name')

    def get_browser(self):
        return self.get('web', 'browser')

    def get_host(self):
        return self.get('common', 'base_url')

    def get_login(self):
        return self.get('common', 'login')

    def get_visit(self):
        return self.get('common', 'visit')

    def get_timeout(self):
        return self.get('common', 'timeout')

    def get_env(self):
        return self.get('common', 'env')


config = Config()


if __name__ == '__main__':
    print(config.get('app', 'device_id'))






