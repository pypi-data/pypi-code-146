import logging, sys, copy, yaml

class CustomResourceDefinition:
    
    def __init__(self, crd, logger=None):
        self.crd = copy.deepcopy(crd)
        self.properties = {}

        self.fullName = self.crd['metadata']['name']
        self.name = self.fullName.split('.')[0]
        if 'labels' in self.crd['metadata']:
            if 'name' in self.crd['metadata']['labels']:
                self.operator = self.crd['metadata']['labels']['name']
            elif 'app.kubernetes.io/name' in self.crd['metadata']['labels']:
                self.operator = self.crd['metadata']['labels']['app.kubernetes.io/name']
            else:
                self.operator = ''
        else:
            self.operator = ''
        self.namespaced = True if self.crd['spec']['scope'] == 'Namespaced' else False

        self._get_properties()
    
    def _get_properties(self):
        try:
            for v in self.crd['spec']['versions']:
                for p in v['schema']['openAPIV3Schema']['properties']['spec']['properties']:
                    self.properties[p] = v['schema']['openAPIV3Schema']['properties']['spec']['properties']['p']
        except:
            self.properties = {}

    def get_properties(self):
        return self.properties

    def get_name(self):
        return self.name

    def get_fullName(self):
        return self.fullName

    def get_operator(self):
        return self.operator
    
    def is_namespaced(self):
        return self.namespaced
