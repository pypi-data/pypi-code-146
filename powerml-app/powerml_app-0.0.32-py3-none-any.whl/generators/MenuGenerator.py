from powerml import Generator
from powerml import ExtractMenuItemsModel
from powerml.utils.generator import load_menu_from_files
from math import ceil
import re

class MenuGenerator(Generator):
    '''
    This is a class that can be used to generate more data for ExtractMenuItemsModels.
    '''

    def __init__(self, menu=None):
        self.menu = menu
        if not self.menu:
            self.menu = load_menu_from_files()
        super().__init__(list(self.menu.values()))

    def __strip_count(self, name_and_count):
        match = re.search(r"^\d+x", name_and_count)

        if match is None:
            return name_and_count

        return name_and_count[match.end(0):].strip()
    
    def __convert_item(self, item):
        item = self.__strip_count(item)
        return self.menu[item] if item in self.menu else item

    def __order_to_items(self, order):
        items = [self.__convert_item(item.lstrip()) for item in order.split('\n')]
        return items

    def coverage_generator(self, data, return_metrics=True):
        model = ExtractMenuItemsModel()
        # should call model.fit(data) once available
        generated_items = set()
        for datum in data:
            generated_items.update(self.__order_to_items(model.predict(datum)))
        metrics = self.compute_coverage(generated_items)
        coverage = metrics['Coverage']
        rare_items = metrics['Rare Types']
        generated_data = []
        if rare_items:
            # generate at least 1 example per rare_item, proportional to the amount of coverage of the data
            num_generate = ceil((1 - coverage) * len(data) / len(rare_items))
            print(f'num generate: {num_generate}')
            for item in rare_items:
                modifier = f'include 1x \'{item}\''
                generated_data.extend(self._generate_modified(data, modifier, num_generate))
        if return_metrics:
            return generated_data, metrics
        return generated_data