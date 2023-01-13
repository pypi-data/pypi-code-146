""" Тестовое ядро, к которому прикрепляется QPI """


class TestCore:
    def __init__(self, name='TestCore'):
        self.name = name

    def get_api_support_methods(self, *args, **kwargs):
        api_methods = {'hello_core': {'method': self.hello_core}}
        return api_methods

    def hello_core(self, *args, **kwargs):
        print("TARGETTARGET")
        return {'info': 'hElLo!1!'}