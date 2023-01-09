import requests
from dcentrapi.Base import Base


class GasMonitor(Base):

    def get_optimal_gas_price(self, network_name, minutes, stats=None, values=None):
        url = self.url + "gas_monitor/optimal_gas_price_for_network"
        data = {
            "network_name": network_name,
            "minutes": minutes,
            "stats": stats,
            "values": values,
        }
        response = requests.get(url, json=data, headers=self.headers)
        return response.json()
