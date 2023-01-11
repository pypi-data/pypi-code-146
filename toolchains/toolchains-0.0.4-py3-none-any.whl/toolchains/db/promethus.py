from prometheus_client.parser import text_string_to_metric_families
from termcolor import cprint
from toolchains.typing import dict2influxdb_line


class PrometheusParser:
    """
    Convert Prometheus metrics to DICT or LIST
    """

    def __init__(self, data, tags=None, measurement=None, common_key=None, return_key=None, filter_label=None, debug=False):

        if tags is None:
            tags = {}
        self.data = data
        self.tags = tags
        self.measurement = measurement
        self.common_key = common_key
        self.return_key = return_key
        self.debug = debug
        self.filter_label = filter_label

    def _debug_print(self, msg, match=False, color="yellow"):
        if self.debug:
            if self.return_key is None:
                cprint(f"{msg}", color)
            else:
                if match:
                    cprint(f"{msg}", color)

    def _filtering(self, data):
        if self.filter_label:
            for filter_key, filter_value in self.filter_label.items():
                if data.get(filter_key) == filter_value and data.get(self.common_key):
                    self._debug_print(f"filtered, {data}", match=True)
                    return True
            return False
        else:
            return True

    def _parse(self, obj_type="single", common_key=None, return_key=None):
        if common_key:
            self.common_key = common_key
        if return_key:
            self.return_key = return_key
        self.return_data = {}
        fields_set = {}
        for family in text_string_to_metric_families(self.data):

            for sample in family.samples:
                category, data, val = (sample.name, sample.labels, sample.value)
                tags = {}
                fields = {}
                metric_key = None

                if self._filtering(data) and self.return_key == category:
                    self._debug_print(f"parsed_prometheus::  {sample}", match=self.return_key == category)
                    if obj_type == "single" and isinstance(data, dict) and val >= 0:
                        metric_key = f"{category}{sample.labels}"
                        if self.return_data.get(metric_key) is None:
                            self.return_data[metric_key] = []
                        tags = dict(data, **self.tags)
                        fields = {"value": val}
                    elif obj_type == "multi":
                        metric_key = category
                        if data.get(self.common_key):
                            fields_set[data.get(self.common_key)] = val
                        if self.return_data.get(metric_key) is None:
                            self.return_data[metric_key] = {}
                        tags = self.tags.copy()
                        fields = fields_set

                    self._debug_print(
                        f"_push_data:: category={category}, "
                        f"tags={tags}, "
                        f"fields={fields}, "
                        f"fields_set={fields_set} "
                        f"self.common_key = {self.common_key} ",
                        match=self.return_key == category
                    )

                    self._push_data(category=category, metric_key=metric_key, tags=tags, fields=fields)
        if self.return_data.get(self.return_key):
            return self.return_data[self.return_key]
        return self.return_data

    def _push_data(self, category=None, metric_key=None, tags={}, fields={}):
        metric = {
            "measurement": "",
            # "measurement": key,
            "tags": tags,
            "fields": fields
        }
        if self.measurement:
            metric['measurement'] = self.measurement
            metric['tags']['category'] = category
        else:
            metric['measurement'] = category

        if isinstance(self.return_data[metric_key], list):
            self.return_data[metric_key].append(metric)
        elif isinstance(self.return_data[metric_key], dict):
            self.return_data[metric_key].update(metric)
        return metric

    def get_multi_dict(self, return_key=None, common_key=None):
        """
        :param return_key:
        :param common_key:
        :return:
          {
             measurement:         NGINX.STAT
             tags:         {
                status:            writing
                new_tag:            new_value
                category:            nginx_vts_main_connections
             }
             fields:         {
                value: 1.0
         }
        """
        return self._parse(obj_type="multi", common_key=common_key, return_key=return_key)

    def get_single_dict(self, return_key=None, common_key=None):
        """
        :param return_key:
        :param common_key:
        :return:
           {
              accepted: 5295344.0
              active: 1.0
              handled: 5295344.0
              reading: 0.0
              requests: 5295344.0
              waiting: 0.0
              writing: 1.0
           }
        """
        return self._parse(obj_type="single", common_key=common_key, return_key=return_key)

    def get_lines(self, return_key=None):
        """
        :param return_key:
        :return:
           [
              NGINX.STAT,status=accepted,new_tag=new_value,category=nginx_vts_main_connections value=5295258.0
              NGINX.STAT,status=active,new_tag=new_value,category=nginx_vts_main_connections value=1.0
              NGINX.STAT,status=handled,new_tag=new_value,category=nginx_vts_main_connections value=5295258.0
              NGINX.STAT,status=reading,new_tag=new_value,category=nginx_vts_main_connections value=0.0
              NGINX.STAT,status=requests,new_tag=new_value,category=nginx_vts_main_connections value=5295258.0
              NGINX.STAT,status=waiting,new_tag=new_value,category=nginx_vts_main_connections value=0.0
              NGINX.STAT,status=writing,new_tag=new_value,category=nginx_vts_main_connections value=1.0
           ]
        """
        if return_key:
            self.return_key = return_key

        self._parse(obj_type="single")
        return_data = []

        for div_key, metrics in self.return_data.items():
            if not isinstance(metrics, list):
                metrics = [metrics]

            for metric in metrics:
                if self.return_key is not None:
                    if self.return_key == metric['tags'].get('category'):
                        return_data.append(dict2influxdb_line(metric))
                else:
                    return_data.append(dict2influxdb_line(metric))

        return return_data

    # def get_kv(self, common_key="status", return_key="nginx_vts_main_connections"):
    #
    #     """
    #     :param common_key:  common key in prometheus structure
    #     :param return_key:  return key in generated dict
    #     :return: nginx status example
    #         # HELP nginx_vts_main_connections Nginx connections
    #         # TYPE nginx_vts_main_connections gauge
    #         nginx_vts_main_connections{status="accepted"} 5253291
    #         nginx_vts_main_connections{status="active"} 1
    #         nginx_vts_main_connections{status="handled"} 5253291
    #         nginx_vts_main_connections{status="reading"} 0
    #         nginx_vts_main_connections{status="requests"} 5253291
    #         nginx_vts_main_connections{status="waiting"} 0
    #         nginx_vts_main_connections{status="writing"} 1
    #                   ▼ ▼ ▼ ▼ ▼
    #         if common_key is "status" returns
    #
    #            {
    #               accepted: 5253291.0
    #               active: 1.0
    #               handled: 5253291.0
    #               reading: 0.0
    #               requests: 5253291.0
    #               waiting: 0.0
    #               writing: 1.0
    #            }
    #     """
    #
    #     metrics = {}
    #     return_data = {}
    #
    #     for family in text_string_to_metric_families(self.data):
    #         parsed_data = {}
    #         fields = {}
    #         tags = {}
    #         for sample in family.samples:
    #             key, data, val = (sample.name, sample.labels, sample.value)
    #             # if key == "nginx_vts_main_connections":
    #                 # print(f"{key}, {dict_to_line(data)} {val}")
    #
    #             if data.get(common_key):
    #                 parsed_data[data.get(common_key)] = val
    #             elif isinstance(data, dict) and val >= 0:
    #                 if return_data.get(key) is None:
    #                     return_data[key] = []
    #
    #                 each_items = {
    #                     "measurement": self.measurement,
    #                     "tags": dict(data, **self.tags),
    #                     "fields": {"value": val}
    #                 }
    #                 return_data[key].append(each_items)
    #
    #             # print(return_data)
    #
    #             # jmon_lib.dump(parsed_data)
    #             if metrics.get(key) is None:
    #                 metrics[key] = {}
    #             metrics[key].update(parsed_data)
    #
    #     print(return_data)
    #
    #     if return_data.get(return_key):
    #         return return_data[return_key]
    #
    #     return return_data
