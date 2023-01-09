import json
import os.path


class AllureData:
    """解析allure_results的数据"""

    def __init__(self, result_path, product=None, test_type=None):
        self.result_path = result_path
        self.product = product
        self.test_type = test_type

    def get_files(self):
        """获取以result.json结尾的文件列表"""
        file_list = []
        for filename in os.listdir(self.result_path):
            if filename.endswith('result.json'):
                file_list.append(filename)
        return [os.path.join(self.result_path, item) for item in os.listdir(self.result_path) if
                item.endswith('result.json')]

    @staticmethod
    def get_file_content(file_path):
        """获取文件内容并转成json"""
        with open(file_path, 'r', encoding='UTF-8') as f:
            content = json.load(f)
        return content

    def parser_content(self, content):
        """解析执行结果"""
        name = content.get('name')
        status = content.get('status')
        full_name = content.get('fullName')
        decription = content.get('description')
        parameters = content.get('parameters', None)
        log_name = [os.path.join(self.result_path, item.get('source')) for item in content.get('attachments') if
                    item.get('name') == 'log'][0]
        start = content.get('start')
        end = content.get('stop')
        case_data = {
            "name": name,
            "full_name": full_name,
            "description": decription,
            "log": log_name,
            "status": status,
            "start_time": start,
            "end_time": end,
            "parameters": parameters
        }
        return case_data

    @staticmethod
    def remove_duplicate(json_contents):
        """去除失败重试的重复结果"""
        case_list = []
        no_repeat_tags = []
        for item in json_contents:
            full_name = item["full_name"]
            parameters = item["parameters"]
            if (full_name, parameters) not in no_repeat_tags:
                no_repeat_tags.append((full_name, parameters))
                case_list.append(item)
            else:
                for case in case_list:
                    if case.get('full_name') == full_name and case.get('parameters') == parameters:
                        if case.get('status') != 'passed':
                            case_list.remove(case)
                            case_list.append(item)
        return case_list

    def get_results(self):
        """获取对外的测试结果列表"""
        file_list = self.get_files()
        result_list = []
        for file in file_list:
            content = self.get_file_content(file)
            parser_content = self.parser_content(content)
            result_list.append(parser_content)
        return self.remove_duplicate(result_list)

    def get_statistical_data(self):
        case_list = self.get_results()

        # 获取用例统计数据
        passed_list = []
        fail_list = []
        for case in case_list:
            status = case.get('status')
            if status == 'passed':
                passed_list.append(case)
            else:
                fail_list.append(case)
        total = len(case_list)
        passed = len(passed_list)
        failed = len(fail_list)
        rate = round((passed / total) * 100, 2)

        # 获取整个任务的开始和结束时间
        start_time, end_time = case_list[0].get('start_time'), case_list[0].get('end_time')
        for case in case_list:
            inner_start = case.get('start_time')
            inner_end = case.get('end_time')
            if inner_start < start_time:
                start_time = inner_start
            if inner_end > end_time:
                end_time = inner_end

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'rate': rate,
            'start': start_time,
            'end': end_time,
            'product': self.product,
            'type': self.test_type
        }


def get_allure_data(result_path):
    """兼容邮件和钉钉的调用"""
    return AllureData(result_path).get_statistical_data()


class ApiData(AllureData):
    """接口测试统计数据"""
    def __init__(self, result_path, product=None):
        super(ApiData, self).__init__(result_path, product, 'api')

    def get_interfaces(self):
        case_list = self.get_results()
        interface_list = []
        for case in case_list:
            log = case.get('log')
            with open(log, 'r') as f:
                for line in f.readlines():
                    if 'url]: ' in line:
                        interface = line.strip().split('url]: ')[1]
                        interface_list.append(interface)
        interface_list = list(set(interface_list))
        return interface_list

    def get_statistic_data(self):
        statistic_data: dict = self.get_statistical_data()
        interface_count = len(self.get_interfaces())
        statistic_data["num"] = interface_count
        return statistic_data


class AppData(AllureData):
    """app测试统计数据"""

    def __init__(self, result_path, product=None):
        super(AppData, self).__init__(result_path, product, 'app')

    def get_statistic_data(self):
        return self.get_statistical_data()


class WebData(AllureData):
    """web页面测试统计数据"""
    def __init__(self, result_path, product=None):
        super(WebData, self).__init__(result_path, product, 'web')

    def get_statistic_data(self):
        return self.get_statistical_data()


if __name__ == '__main__':
    result_path1 = '/Users/UI/PycharmProjects/qrunner_new_gitee/allure-results'
    print(get_allure_data(result_path1))

