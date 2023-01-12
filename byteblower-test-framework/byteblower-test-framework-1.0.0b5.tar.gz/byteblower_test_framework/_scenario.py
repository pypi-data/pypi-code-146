"""ByteBlower Test Scenario interface module."""
import logging
from datetime import datetime, timedelta
from time import sleep
from typing import List, Union  # for type hinting

from byteblowerll.byteblower import ByteBlower
from pandas import DataFrame

from ._endpoint.ipv4.nat import NattedPort  # for type hinting
from ._endpoint.port import Port  # for type hinting
from ._host.server import Server  # for type hinting
from ._report.byteblowerreport import ByteBlowerReport  # for type hinting
from ._traffic.flow import Flow  # for type hinting


class Scenario(object):
    """ByteBlower Test Scenario interface."""

    __slots__ = (
        '_flows',
        '_servers',
        '_bb_reports',
    )

    def __init__(self) -> None:
        """Make a base test scenario."""
        self._flows: List[Flow] = []
        self._servers: List[Server] = []
        self._bb_reports: List[ByteBlowerReport] = list()

    def __del__(self) -> None:
        """Cleanup of test scenario."""

    def add_report(self, report: ByteBlowerReport) -> None:
        self._bb_reports.append(report)

    def add_flow(self, flow: Flow) -> None:
        if flow.source.failed or flow.destination.failed:
            logging.debug(
                'Flow %r is not added to the scenario because either'
                ' source or destination address configuration failed.',
                flow.name)
            return
        self._flows.append(flow)
        # Check if we know the server. If not, add it.

        for server in (flow.source.server, flow.destination.server):
            if server in self._servers:
                # We have nothing to do
                logging.debug('Test:Server already in list')
            else:
                logging.debug('Test:Adding new server.')
                self._servers.append(server)

    def run(
        self,
        duration: timedelta = timedelta(seconds=10),
        wait_for_finish: timedelta = timedelta(seconds=5)
    ) -> None:
        self._start(duration)
        self._wait_until_finished(duration, wait_for_finish)
        self._stop()
        self._analyse()
        logging.info('Test is done')

    def _start(self, duration: timedelta) -> None:
        for flow in self._flows:
            flow.apply(duration=duration)
        for server in self._servers:
            server.start()

    def _wait_until_finished(self, duration: timedelta,
                             wait_for_finish: timedelta) -> None:
        previous = datetime.now()
        start_time = previous
        iteration = 0
        # TODO: Purpose of statement? This will probably never be executed.
        #       Was the initial intention to perform
        #       this *after* the while loop?
        if (datetime.now() - previous) > timedelta(seconds=1):
            for flow in self._flows:
                flow.process()
                flow.updatestats()
        while (previous - start_time) < duration:
            # sleep 1 miliseconds
            sleep(0.001)
            if (datetime.now() - previous) > timedelta(seconds=1):
                logging.debug('Update stats, iteration is %u', iteration)
                for flow in self._flows:
                    flow.updatestats()
                iteration += 1
                previous = datetime.now()
            else:
                for flow in self._flows:
                    flow.process()

        # Wait for TCP to finish if flow uses TCP
        finish_time = datetime.now() + wait_for_finish
        for flow in self._flows:
            remaining_wait_time = finish_time - datetime.now()
            if remaining_wait_time > timedelta(seconds=0):
                flow.wait_until_finished(remaining_wait_time)

            if datetime.now() >= finish_time:
                break

    def _stop(self) -> None:
        for server in self._servers:
            server.stop()
        sleep(1)

    def _analyse(self) -> None:
        for flow in self._flows:
            flow.analyse()

    def _port_list(self) -> DataFrame:
        ports: List[Union[Port, NattedPort]] = []
        for flow in self._flows:
            if flow.source not in ports:
                ports.append(flow.source)
            if flow.destination not in ports:
                ports.append(flow.destination)

        df = DataFrame(
            columns=[
                'IP address',
                'Gateway',
                'Network',
                'VLAN (PCP / DEI)',
                'Public IP',
            ],
            index=[port.name for port in ports],
        )
        for port in ports:
            if port.is_natted:
                public_ip = port.public_ip
            else:
                public_ip = '-'
            vlan_configs = port.vlan_config
            if vlan_configs:
                vlan_info = 'Outer ' + ' > '.join(
                    (f'{vlan_id} ({vlan_pcp} / {vlan_dei})'
                     for vlan_id, vlan_dei, vlan_pcp in vlan_configs))
            else:
                vlan_info = 'No'
            df.loc[port.name] = [
                port.ip,
                port.gateway,
                port.network,
                vlan_info,
                public_ip,
            ]
        return df

    def report(self) -> None:
        for bb_report in self._bb_reports:
            bb_report.clear()

        for flow in self._flows:
            for bb_report in self._bb_reports:
                bb_report.add_flow(flow)

        for bb_report in self._bb_reports:
            bb_report.render(ByteBlower.InstanceGet().APIVersionGet(),
                             self._port_list())

            report_file_url = bb_report.report_url
            logging.info('Stored report for %s to %r', bb_report,
                         report_file_url)
