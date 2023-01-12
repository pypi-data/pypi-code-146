#!/usr/local/env python3
from .configer import (CalculatePrime, EndlessConfig, GostConfig,
                       StatusMonitorConfig, QbittorrentConfig, SystemConfig,
                       Shadowsocks, Sar)
from .installer import AutoRemove, CoreAppInstaller, StatAppInstaller, PythonPackageInstaller
from .piper import DependencyDownloader


def main():
    exec_classes = [
        SystemConfig, CoreAppInstaller, StatAppInstaller, AutoRemove, PythonPackageInstaller,
        EndlessConfig,
        # StatusMonitorConfig, GostConfig,
        # CalculatePrime,
        DependencyDownloader, Shadowsocks, Sar 
    ]
    for ec in exec_classes:
        ec().run()


if __name__ == '__main__':
    main()
