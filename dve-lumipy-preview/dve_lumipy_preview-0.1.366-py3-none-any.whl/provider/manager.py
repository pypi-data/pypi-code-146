import time
from typing import Optional

from .api_server import ApiServer
from .base_provider import BaseProvider
from .factory import Factory
from .common import red_print, cyan_print
from lumipy.common.string_utils import indent_str
import re
import traceback


class ProviderManager:
    """Class that manages the configuration and running of python-based Luminesce providers.

    """

    def __init__(
            self,
            *providers: BaseProvider,
            host: Optional[str] = '127.0.0.1',
            port: Optional[int] = 5001,
            dry_run: Optional[bool] = False,
            user: Optional[str] = None,
            domain: Optional[str] = None,
            _fbn_run: Optional[bool] = False
    ):
        """Constructor of the ProviderManager class.

        Args:
            *providers (BaseProvider): local provider instances (classes that inherit from BaseProvider) that
            the server should manage.
            host (Optional[str]): optional server host path. Defaults to localhost.
            port (Optional[int]): optional port for the server to use. Defaults to 5000.
            dry_run (Optional[bool]): whether to only run the web server and not start the local provider factory.
            user (Optional[str]): optional user id, or 'global' to run the providers for. You can also specify 'global'
            to run the provider globally.
            domain (Optional[str]): lusid environment to run in.
            _fbn_run (Optional[bool]): Finbourne-internal. Alternative way to authenticate with RabbitMQ when running in
            Finbourne's k8s clusters.

        """
        if len(providers) == 0:
            raise ValueError(
                "Nothing to run! No providers have been supplied to the provider server constructor"
            )

        if re.match('^[\w._-]+$', host) is None:
            raise ValueError(f"Invalid value for host: {host}")

        if not isinstance(port, int):
            raise ValueError(f"Port number must be an integer. Was {type(port).__name__} ({port})")

        if user is not None and not user.isalnum():
            raise ValueError(f"Invalid user ID ({user}), must be alphanumeric characters only. ")

        if domain is not None and re.match('^[\w_-]+$', domain) is None:
            raise ValueError(f"Invalid value for domain: {domain}")

        self.dry_run = dry_run
        self.api_server = ApiServer(*providers, host=host, port=port)
        self.factory = Factory(host, port, user, domain, _fbn_run)

    def start(self):
        cyan_print(f'Launching providers! 🚀')
        self.api_server.start()

        if not self.dry_run:
            self.factory.start()
        else:
            red_print('⚠️  dry_run=True: only running provider APIs.')

        if not self.dry_run and not self.factory.errored:
            cyan_print('\n🟢 Providers are ready to use.')
            cyan_print('Use ctrl+c or the stop button in jupyter to shut down\n')
        elif not self.dry_run and self.factory.errored:
            red_print("\n💥 Provider factory failed to start!")
            self.api_server.stop()
            raise ValueError(
                'Could not start the factory process due to connection/auth issues during startup. '
                'Check your internet connection / config and try again.'
            )

    def stop(self, exc_type=None, exc_val=None, exc_tb=None):

        if exc_type == KeyboardInterrupt:
            red_print("\n⚠️  Received keyboard interrupt.")

        elif exc_type is not None:
            red_print(f"\n💥 An unexpected {exc_type.__name__} occurred: \"{exc_val}\"")
            red_print("  Traceback (most recent call last):")
            red_print(indent_str(''.join(traceback.format_tb(exc_tb))))
            red_print("  Trying to shut down before rethrow...")

        cyan_print('\n🟡 Providers are shutting down.')
        if not self.dry_run:
            self.factory.stop()
        self.api_server.stop()
        cyan_print(f'\n🔴 Providers are shut down.\n')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop(exc_type, exc_val, exc_tb)

    def run(self):
        """Run the manager instance in the foreground. The manager can be shut down with a KeyboardInterupt (ctrl+C).

        """
        self.start()
        while True:
            try:
                # block
                time.sleep(5)
            except KeyboardInterrupt as ke:
                self.stop(type(ke), None, None)
                raise ke
            except Exception as e:
                self.stop(type(e), str(e), e.__traceback__)
                raise e
