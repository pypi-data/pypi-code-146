# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pms',
 'pms.core',
 'pms.extra',
 'pms.sensors',
 'pms.sensors.bosch_sensortec',
 'pms.sensors.honeywell',
 'pms.sensors.novafitness',
 'pms.sensors.plantower',
 'pms.sensors.sensirion',
 'pms.sensors.winsen']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0', 'pyserial>=3.5', 'typer>=0.6.1']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata>=3.6'],
 'docs': ['mkdocs>=1.2.3', 'mkdocs-material>=8.2.5', 'pymdown-extensions>=9.5'],
 'influxdb': ['influxdb>=5.2.0'],
 'mqtt': ['paho-mqtt>=1.4.0'],
 'test': ['pytest>=7.1.2',
          'pytest-cov>=2.12.1',
          'packaging>=21.3,<22.0',
          'mock_serial>=0.0.1']}

entry_points = \
{'console_scripts': ['pms = pms.cli:main'],
 'pypms.extras': ['bridge = pms.extra.bridge:cli',
                  'influxdb = pms.extra.influxdb:cli',
                  'mqtt = pms.extra.mqtt:cli'],
 'pypms.sensors': ['HPMA115C0 = pms.sensors.honeywell.hpma115c0',
                   'HPMA115S0 = pms.sensors.honeywell.hpma115s0',
                   'MCU680 = pms.sensors.bosch_sensortec.mcu680',
                   'MHZ19B = pms.sensors.winsen.mhz19b',
                   'PMS3003 = pms.sensors.plantower.pms3003',
                   'PMS5003S = pms.sensors.plantower.pms5003s',
                   'PMS5003ST = pms.sensors.plantower.pms5003st',
                   'PMS5003T = pms.sensors.plantower.pms5003t',
                   'PMSx003 = pms.sensors.plantower.pmsx003',
                   'SDS01x = pms.sensors.novafitness.sds01x',
                   'SDS198 = pms.sensors.novafitness.sds198',
                   'SPS30 = pms.sensors.sensirion.sps30',
                   'ZH0xx = pms.sensors.winsen.zh0xx']}

setup_kwargs = {
    'name': 'pypms',
    'version': '0.7.1',
    'description': 'Data acquisition and logging for Air Quality Sensors with UART interface',
    'long_description': '# Serial Air Quality Sensors\n\nData acquisition and logging for Air Quality Sensors with UART interface\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypms)](https://pypi.org/project/pypms)\n[![PyPI](https://img.shields.io/pypi/v/pypms)](https://pypi.org/project/pypms)\n[![Build Status](https://github.com/avaldebe/PyPMS/actions/workflows/test.yml/badge.svg)](https://github.com/avaldebe/PyPMS/actions)\n[![GitHub issues](https://img.shields.io/github/issues/avaldebe/PyPMS)](https://github.com/avaldebe/PyPMS/issues)\n[![GitHub license](https://img.shields.io/github/license/avaldebe/PyPMS)](https://github.com/avaldebe/PyPMS/blob/master/LICENSE)\n[![DOI](https://zenodo.org/badge/203110737.svg)](https://zenodo.org/badge/latestdoi/203110737)\n\n[project site]: https://avaldebe.github.io/PyPMS\n\n## Installation\n\nThis package can be pip installed.\nPlease visit [project site] for detailed instructions.\n\n## Command Line Tools\n\nThis package provides tools for requesting new measurements from the sensors\nand print them on different formats, save them to a CSV file,\nor push them to an external service such as an MQTT or InfluxDB server.\nMQTT or InfluxDB server support requires additional packages.\nPlease visit [project site] for details.\n\n## Particulate Matter Sensors\n\n| Sensor            | `--sensor-model` |  PM1  | PM2.5 |  PM4  | PM10  | size bins | Other                  | Tested |\n| ----------------- | ---------------- | :---: | :---: | :---: | :---: | :-------: | ---------------------- | :----: |\n| [Plantower]       |\n| PMS1003 (aka G1)  | [PMSx003]        |   ✔️   |   ✔️   |       |   ✔️   |     6     |                        |        |\n| PMS3003 (aka G3)  | [PMS3003]        |   ✔️   |   ✔️   |       |   ✔️   |           |                        |   ✔️    |\n| PMS5003 (aka G5)  | [PMSx003]        |   ✔️   |   ✔️   |       |   ✔️   |     6     |                        |        |\n| PMS5003T          | [PMS5003T]       |   ✔️   |   ✔️   |       |   ✔️   |     4     | temp. & rel.hum.       |   ✔️    |\n| PMS5003S          | [PMS5003S]       |   ✔️   |   ✔️   |       |   ✔️   |     6     | HCHO concentration     |        |\n| PMS5003ST         | [PMS5003ST]      |   ✔️   |   ✔️   |       |   ✔️   |     6     | HCHO, temp. & rel.hum. |        |\n| PMS7003 (aka G7)  | [PMSx003]        |   ✔️   |   ✔️   |       |   ✔️   |     6     |                        |   ✔️    |\n| PMSA003 (aka G10) | [PMSx003]        |   ✔️   |   ✔️   |       |   ✔️   |     6     |                        |   ✔️    |\n| [NovaFitness]     |\n| SDS011            | [SDS01x]         |       |   ✔️   |       |   ✔️   |           |                        |   ✔️    |\n| SDS018            | [SDS01x]         |       |   ✔️   |       |   ✔️   |           |                        |        |\n| SDS021            | [SDS01x]         |       |   ✔️   |       |   ✔️   |           |                        |        |\n| SDS198            | [SDS198]         |       |       |       |       |           | PM100                  |   ✔️    |\n| [Honeywell]       |\n| HPMA115S0         | [HPMA115S0]      |       |   ✔️   |       |   ✔️   |           |                        |        |\n| HPMA115C0         | [HPMA115C0]      |   ✔️   |   ✔️   |   ✔️   |   ✔️   |           |                        |   ✔️    |\n| [Sensirion]       |\n| SPS30             | [SPS30]          |   ✔️   |   ✔️   |   ✔️   |   ✔️   |     5     | typical particle size  |   ✔️    |\n| [Winsen]          |\n| ZH03B             | [ZH0xx]          |   ✔️   |   ✔️   |   ✔️   |       |           |                        |        |\n| ZH06-I            | [ZH0xx]          |   ✔️   |   ✔️   |   ✔️   |       |           |                        |        |\n\n[plantower]:  https://avaldebe.github.io/PyPMS/sensors/Plantower\n[PMS3003]:    https://avaldebe.github.io/PyPMS/sensors/Plantower/#pms3003\n[PMSx003]:    https://avaldebe.github.io/PyPMS/sensors/Plantower/#pmsx003\n[PMS5003T]:   https://avaldebe.github.io/PyPMS/sensors/Plantower/#pms5003t\n[PMS5003S]:   https://avaldebe.github.io/PyPMS/sensors/Plantower/#pms5003s\n[PMS5003ST]:  https://avaldebe.github.io/PyPMS/sensors/Plantower/#pms5003st\n\n[NovaFitness]:https://avaldebe.github.io/PyPMS/sensors/NovaFitness\n[SDS01x]:     https://avaldebe.github.io/PyPMS/sensors/NovaFitness/#sds01x\n[SDS198]:     https://avaldebe.github.io/PyPMS/sensors/NovaFitness/#sds198\n\n[Honeywell]:  https://avaldebe.github.io/PyPMS/sensors/Honeywell\n[HPMA115S0]:  https://avaldebe.github.io/PyPMS/sensors/Honeywell/#hpma115s0\n[HPMA115C0]:  https://avaldebe.github.io/PyPMS/sensors/Honeywell/#hpma115c0\n\n[Sensirion]:  https://avaldebe.github.io/PyPMS/sensors/Sensirion\n[SPS30]:      https://avaldebe.github.io/PyPMS/sensors/Sensirion/#sps30\n\n[Winsen]:     https://avaldebe.github.io/PyPMS/sensors/Winsen\n[ZH0xx]:      https://avaldebe.github.io/PyPMS/sensors/Winsen/#zh0xx\n[MHZ19B]:     https://avaldebe.github.io/PyPMS/sensors/Winsen/#mhz19b\n\n## Other Sensors\n\n- [MCU680]:\n  chinese module with a [BME680] sensor, a mirocontroller (μC) and 3.3V low-dropout regulator (LDO).\n  The μC acts as I2C/UART bridge, providing outputs from the [closed source integration library][BSEC].\n- [MHZ19B]:\n  infrared CO2 sensor module from [Winsen].\n\n[MCU680]:   https://avaldebe.github.io/PyPMS/sensors/mcu680/#mcu680\n[BME680]:   https://avaldebe.github.io/PyPMS/sensors/mcu680/#bme680\n[BSEC]:     https://www.bosch-sensortec.com/software-tools/software/bsec/\n\n## Want More Sensors\n\nFor more Air Quality sensors [open an issue][issue].\n\n[issue]: https://github.com/avaldebe/PyPMS/issues\n\n## Use as a library\n\nPyPMS/pms is meant as a command line application.\nThe [project site] contain some help for those brave enough to use its internals as a [library].\n\n[library]: https://avaldebe.github.io/PyPMS/library_usage\n\n## Changelog\n\n- 0.7.1\n  - disable logging unless CLI is running [PR#37](https://github.com/avaldebe/PyPMS/pull/37)\n- 0.7.0\n  - add Python 3.11 support and drop Python 3.7 support\n  - pre-heat for PMSx003 sensors [PR#35](https://github.com/avaldebe/PyPMS/pull/35)\n  - `open`/`close` methods for granular SensorReader operation [PR#33](https://github.com/avaldebe/PyPMS/pull/33)\n  - fix HPMA115C0 header [#26](https://github.com/avaldebe/PyPMS/issues/26)\n- 0.6.2\n  - move logger config to CLI module [PR#28](https://github.com/avaldebe/PyPMS/pull/28)\n- 0.6.1\n  - fix `pms.sensors.sensirion` module name and docs\n  - reliably recognize SPS30 sensor [#25](https://github.com/avaldebe/PyPMS/issues/25)\n- 0.6.0\n  - [project site]\n  - reorganize internal modules\n    - `pms.core`: core functionality, such as `Sensor` and `SensorReader`\n    - `pms.sensors`: sensor modules grouped by manufacturer\n    - `pms.extra`: extra cli utilities, such as `pms influxdb` and `influxdb mqtt`\n    - importing from `pms.sensor` is deprecated, import from `pms.core` instead\n  - plugin architecture\n    - load sensor modules from entry points advertized as `"pypms.sensors"`\n    - load extra cli commands from entry points advertized as `"pypms.extras"`\n  - support [Winsen] PM sensors and [MHZ19B] infrared CO2 sensor.\n  - pm1/pm4/raw2_5/pm2_5 properties, [#17](https://github.com/avaldebe/PyPMS/issues/17)\n- 0.5.0\n  - set username/password with environment variables:\n    - `$MQTT_USER` sets `--mqtt-user` on `pms mqtt` and `pms bridge`\n    - `$MQTT_USER` sets `--mqtt-user` on `pms mqtt` and `pms bridge`\n    - `$DB_USER` sets `--db-user` on `pms influxdb` and `pms bridge`\n    - `$DB_PASS` sets `--db-pass` on `pms influxdb` and `pms bridge`\n- 0.4.1\n  - info about the sensor observations with `pms info`\n  - fix [MCU680] obs.pres typo [#16](https://github.com/avaldebe/PyPMS/issues/16)\n- 0.4.0\n  - capture raw messages with `pms csv --capture`\n  - decode captured messages with `pms serial --capture`\n  - hexdump format with `pms serial --format hexdump`\n  - deprecate subset observation method\n- 0.3.1\n  - fix influxdb default tags\n- 0.3.0\n  - option for a fix number of samples\n  - PMSx003 consistency check after sleep/wake\n- 0.2.*\n  - widen project scope from PM sensors to AQ sensors in general\n  - support [BME680] sensor ([MCU680] module)\n- 0.1.*\n  - widen project scope beyond [Plantower] PM sensors\n  - support [NovaFitness], [Honeywell] and [Sensirion]\xa0PM sensors\n  - cli for logging to csv file, InfluxDB server or MQTT server\n',
    'author': 'Alvaro Valdebenito',
    'author_email': 'avaldebe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://avaldebe.github.io/PyPMS',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
