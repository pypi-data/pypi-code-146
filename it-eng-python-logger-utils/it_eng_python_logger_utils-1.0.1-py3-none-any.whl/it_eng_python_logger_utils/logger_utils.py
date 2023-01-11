import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

config_integration.trace_integrations(["requests"])



class LoggerHelper:
    def __init__(
        self, logger_name, app_insights_token, level="INFO", send_to_azure=True
    ):
        self.logger_name = logger_name
        self.app_insights_token = app_insights_token
        self.level = level
        self.logger = logging.getLogger(self.logger_name)
        level = eval("logging." + self.level.upper())

        logging.basicConfig(level=level)
        if send_to_azure:
            try:
                self.logger.addHandler(
                    AzureLogHandler(
                        connection_string="InstrumentationKey="
                        + self.app_insights_token
                    )
                )
            except Exception as e:
                print("Azure Add Handler error: ", e)
                raise e

    def trace(self):
        """
        Trace your API calls and send them to Azure App Insights.
        """
        try:
            return Tracer(
                exporter=AzureExporter(
                    connection_string="InstrumentationKey=" + self.app_insights_token
                ),
                sampler=ProbabilitySampler(1.0),
            )
        except Exception as e:
            print("Tracer Error: ", e)
            raise e

    def info(
        self,
        message: any,
        structured=True,
    ):

        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""

        if structured:
            return self.logger.info(
                f'{{"Logger": "{self.logger_name}", "Severity": "Info", "Message": {message}}}'
            )
        return self.logger.info(message)

    def debug(
        self,
        message: any,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""

        if structured:
            return self.logger.debug(
                f'{{"Logger": "{self.logger_name}", "Severity": "Debug", "Message": {message}}}'
            )
        return self.logger.debug(message)

    def warning(
        self,
        message: any,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            return self.logger.warning(
                f'{{"Logger": "{self.logger_name}", "Severity": "Warning", "Message": {message}}}'
            )
        return self.logger.warning(message)

    def critical(
        self,
        message: any,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            return self.logger.critical(
                f'{{"Logger": "{self.logger_name}", "Severity": "Critical", "Message": {message}}}'
            )
        return self.logger.critical(message)

    def error(
        self,
        message: any,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            return self.logger.error(
                f'{{"Logger": "{self.logger_name}", "Severity": "Error", "Message": {message}}}'
            )
        return self.logger.error(message)
