import requests
from .command_base import CliCommand
from .utils import error
from tabulate import tabulate
import websockets
import asyncio

from .app_sdk.app_init_command import AppInitCommand
from .app_sdk.app_build_command import AppBuildCommand
from .app_sdk.app_install_command import AppInstallCommand


class AppCommand(CliCommand):
    @staticmethod
    def help():
        return 'Operations on apps installed on Auterion device'

    def __init__(self, config):
        self._config = config
        self._apps_api_endpoint = f"http://{config['device_address']}/api/apps/v1.0"
        self._apps_api_endpoint_ws = f"ws://{config['device_address']}/api/apps/v1.0"

        self._subcommand_modules = {
            'init': AppInitCommand(config),
            'build': AppBuildCommand(config),
            'install': AppInstallCommand(config)
        }

    def setup_parser(self, parser):

        command_subparsers = parser.add_subparsers(title='command', metavar='<command>', dest='app_command',
                                                   required=True)
        list_parser = command_subparsers.add_parser('list', aliases=['ls'], help='List all installed apps')
        list_parser.add_argument('app_name', nargs='?', default=None)

        rm_parser = command_subparsers.add_parser('remove', aliases=['rm'], help='Remove an installed app')
        rm_parser.add_argument('app_name', help='The name of the app to be removed')

        logs_parser = command_subparsers.add_parser('logs', help='Show logs of a running app')
        logs_parser.add_argument('app_name', help='The name of the app to show logs for')
        logs_parser.add_argument('-f', '--follow', action='store_true', help='Live follow the logs from selected app')
        logs_parser.add_argument('-t', '--tail', type=int, help='Number of log lines to fetch', default=20)
        logs_parser.add_argument('-a', '--all', action='store_true', help='Get all available logs')

        start_parser = command_subparsers.add_parser('start', help='Start an app')
        start_parser.add_argument('app_name', help='The name of the app to start')

        stop_parser = command_subparsers.add_parser('stop', help='Stop an app')
        stop_parser.add_argument('app_name', help='The name of the app to stop')

        restart_parser = command_subparsers.add_parser('restart', help='Restart an app')
        restart_parser.add_argument('app_name', help='The name of the app to restart')

        enable_parser = command_subparsers.add_parser('enable', help='Enable an app')
        enable_parser.add_argument('app_name', help='The name of the app to enable')

        disable_parser = command_subparsers.add_parser('disable', help='Disable an app')
        disable_parser.add_argument('app_name', help='The name of the app to disable')

        status_parser = command_subparsers.add_parser('status', help='Get status from an app')
        status_parser.add_argument('app_name', help='The name of the app to get status from')

        for name, command in self._subcommand_modules.items():
            parser = command_subparsers.add_parser(name, help=command.help())
            command.setup_parser(parser)

    def needs_device(self, args):
        command = args.app_command
        if command in self._subcommand_modules:
            return self._subcommand_modules[command].needs_device(args)
        return True

    def run(self, args):
        command = args.app_command
        aliases = {
            'ls': 'list',
            'rm': 'remove'
        }

        if command in aliases:
            command = aliases[command]

        if command in self._subcommand_modules:
            self._subcommand_modules[command].run(args)

        else:
            func = getattr(self, command)
            if func is None:
                raise RuntimeError(f'Func for command {args.app_command} is not implemented')
            func(args)

    def handle_exception(self, exception):
        try:
            raise exception
        except requests.ConnectionError:
            error(f"Could not connect to device.")

    def list(self, args):
        if args.app_name is not None:
            self._print_apps([self._get_app(args.app_name)])
        else:
            self._print_apps(self._get_apps())

    def remove(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/remove')
        self._print_app_result(data, args.app_name, "removed")

    def logs(self, args):
        if args.follow:
            async def printer():
                try:
                    async with websockets.connect(f'{self._apps_api_endpoint_ws}/apps/{args.app_name}/logs/feed') as ws:
                        async for message in ws:
                            print(message.decode('utf-8'), end='')
                except asyncio.exceptions.CancelledError:
                    # This is expected. Happens as soon as user does no longer want logs.
                    return

            loop = asyncio.get_event_loop()
            task = loop.create_task(printer())
            try:
                loop.run_until_complete(task)
            except KeyboardInterrupt:
                print("Stopping..")
                task.cancel()
                loop.run_until_complete(task)
            finally:
                loop.close()
        else:
            tail = 'all' if args.all else str(args.tail)
            data = requests.get(f'{self._apps_api_endpoint}/apps/{args.app_name}/logs', params={
                'tail': tail
            })
            if data:
                print(data.text)
            else:
                error(f"App {args.app_name} is not installed")

    def start(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/start')
        self._print_app_result(data, args.app_name, "started")

    def stop(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/stop')
        self._print_app_result(data, args.app_name, "stopped")

    def restart(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/restart')
        self._print_app_result(data, args.app_name, "restarted")

    def enable(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/enable')
        self._print_app_result(data, args.app_name, "enabled")

    def disable(self, args):
        data = requests.post(f'{self._apps_api_endpoint}/apps/{args.app_name}/disable')
        self._print_app_result(data, args.app_name, "disabled")

    def status(self, args):
        data = requests.get(f'{self._apps_api_endpoint}/apps/{args.app_name}/status')
        self._print_app_result(data, args.app_name, "status")

    def _get_app(self, app):
        data = requests.get(f'{self._apps_api_endpoint}/apps/{app}')
        try:
            body = data.json()
        except:
            body = {}
        if data:
            return body
        else:
            if "message" in body:
                error(body["message"])
            else:
                error(f"App {app} is not installed")

    def _get_apps(self):
        apps = requests.get(f'{self._apps_api_endpoint}/apps')
        if apps:
            return apps.json()
        else:
            error(f"Failed to get apps")

    def _print_apps(self, apps):
        headers = ["Name", "Version", "Status", "Enable", "Services", "Status", "Enable"]
        matrix = []
        for app in apps:
            row = [app['name'], app['version'], app['status'], app['enable']]
            if len(app['services']) > 0:
                row.append(app['services'][0]["name"])
                row.append(app['services'][0]["status"])
                row.append(app['services'][0]["enable"])
            else:
                row.append("")
                row.append("")
            matrix.append(row)
            for s in app['services'][1:]:
                matrix.append(["", "", "", "", s["name"], s["status"], s["enable"]])
        print(tabulate(matrix, headers=headers))

    def _print_app_result(self, data, app, success_message):
        try:
            body = data.json()
        except:
            body = {}

        if data:
            if "message" in body:
                print(body["message"])
            else:
                print(f'App {app} {success_message}')
        else:
            if "message" in body:
                error(body["message"])
            else:
                error(f"App {app} is not installed")
