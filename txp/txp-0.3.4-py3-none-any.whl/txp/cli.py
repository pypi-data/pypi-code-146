import click
from txp.devices.drivers.cli_commands.test_voyager import voyager_test
from txp.common.config import settings
from txp.main import main
from txp.web.run_app import run_st_app
import multiprocessing
from sys import platform
import logging
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


@click.group()
def txp_cli_entrypoint():
    """TXP command line for Tranxpert predictive maintenance solution."""
    pass


@click.command()
@click.argument("device-mac", type=str)
def run_voyager_test(device_mac):
    """Run voyager test

    DEVICE_MAC is the Voyager device string MAC address in Dash-Hexadecimal notation.
    """
    mac_tpl = tuple(device_mac)
    voyager_test(mac_tpl)


@click.command()
def web():
    """Run the streamlit web application"""
    run_st_app()


@click.command()
@click.option('--clear-spilled-packages', is_flag=True, default=False,
              help="If enabled, then the packages found on disk will be discarded.")
@click.option('--packages-queue-memory-limit', default=settings.gateway.queue_memory_size,
              help="Percentage of memory size at which the "
                   "gateway will start to spill packages. Is set to 0, then the Gateway"
                   " will preserver all the sampled packages and it'll operate without "
                   " sending the packages to the cloud.")
# TODO: Only should be necessary 1 topic value and the streaming mode.
@click.option('--telemetry-topic-realtime-template',
              default=settings.gateway.mqtt.telemetry_topic_realtime_template,
              help='The telemetry topic template string to use when sending telemetry '
                   'messages in realtime')
@click.option('--telemetry-topic-batch-template',
              default=settings.gateway.mqtt.telemetry_topic_batch_template,
              help="The telemetry topic template string to use when sending telemetry"
                   "messages in realtime")
@click.option('--streaming-mode', default=settings.gateway.streaming_mode,
              help="The mode to use for telemetry: REALTIME / BATCH")
def run(
        clear_spilled_packages: bool,
        packages_queue_memory_limit: int,
        telemetry_topic_realtime_template: str,
        telemetry_topic_batch_template: str,
        streaming_mode: str
):
    """Run the main application for the Gateway"""

    # Sets the packages queue size to default/received value
    settings.gateway.queue_memory_size = int(packages_queue_memory_limit)

    if packages_queue_memory_limit == 0:
        log.info("--packages-queue-memory-limit equal to 0.  "
                  "The Gateway will operate in offline mode after initialization")
        settings.gateway.queue_memory_size = 0
        settings.gateway.offline_mode = True

    if clear_spilled_packages:
        log.info("--clear-spilled-packages flag enabled. "
                  "Old packages will be deleted.")
        settings.gateway.queue_clean_old_spilled_packages = True

    if telemetry_topic_realtime_template:
        log.info(f"Set telemetry realtime topic template to: {telemetry_topic_realtime_template}")
        settings.gateway.mqtt.telemetry_topic_realtime_template = telemetry_topic_realtime_template

    if telemetry_topic_batch_template:
        log.info(f"Set telemetry batch topic template to: {telemetry_topic_batch_template}")
        settings.gateway.mqtt.telemetry_topic_batch_template = telemetry_topic_batch_template

    if streaming_mode:
        log.info(f"Streaming mode setup to: {streaming_mode}")
        settings.gateway.streaming_mode = streaming_mode

    main()


txp_cli_entrypoint.add_command(run_voyager_test)
txp_cli_entrypoint.add_command(run)
txp_cli_entrypoint.add_command(web)


if __name__ == '__main__':

    # This avoids opencv conflicts that can arise when using multiprocessing with
    # fork in macOS.
    if platform == "Darwin" or platform == "darwin":
        multiprocessing.set_start_method('spawn', force=True)
    run()
