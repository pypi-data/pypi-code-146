
import pika, logging, time, os

from pika.exchange_type import ExchangeType
LOG = logging.getLogger(__name__)
import queue

import ssl

class BasicPikaConnection(object):
    EXCHANGE_TYPE = ExchangeType.fanout
    def __init__(self,host,port,user,password,connectionName,callbackData,callbackControl,component,ssl_activate=False,ca_certificate=None,client_certificate=None,client_key=None,certificate_password=''):
        self.ssl_activate = ssl_activate
        self.ca_certificate = ca_certificate
        self.certificate_password = certificate_password
        self.client_certificate = client_certificate
        self.client_key = client_key
        self.credentials = pika.PlainCredentials(user, password)
        self.host = host
        self.port = port
        self.component = component
        self.connectionName  = connectionName
        self.callbackData    = callbackData
        self.callbackControl = callbackControl

        self._connectionConsumer = None
        self._connectionPublisher = None
        
        self._channelConsumer = None
        self._channelPublish = None
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self.consumerRun = False
        self.publisherRun = False
        self.reconnectingTimeout = 10.0
        self.queSendData = queue.Queue()

    def bindExchangeConsumer(self,exchange,callback):
        queue_name =  f'{self.connectionName}_{exchange}'
        result = self._channelConsumer.queue_declare(queue=queue_name, exclusive=False)
        self._channelConsumer.exchange_declare(exchange=exchange,  exchange_type='fanout')
        self._channelConsumer.queue_bind(exchange=exchange, queue=queue_name)
        self._channelConsumer.basic_consume(queue=queue_name,
                            auto_ack=True,
                            on_message_callback=callback)
    
    def publishData(self,msg):
        topic = f'component.{self.component}.data.input'
        LOG.info(f'{topic}=>{msg}')
        self.queSendData.put_nowait({topic:msg})

    def publishControl(self,msg):
        topic = f'component.{self.component}.control.input'
        LOG.info(f'{topic}=>{msg}')
        self.queSendData.put_nowait({topic:msg})
            
    
    def startPublisher(self):
        # Bestimmte Fehlerbeahndlung not notwendig
        self.publisherRun = True
        while self.publisherRun :
            try:
                self.runPublisher()
            except (pika.exceptions.IncompatibleProtocolError, pika.exceptions.StreamLostError):
                desc = f'Loosing Connection from {self.host}:{self.port}'
                LOG.warning(desc)
            except Exception as e:
                if self.publisherRun:
                    desc = f'Exception Connection from {self.host}:{self.port} '
                    LOG.exception(desc)
                #self.publisherRun = False
            time.sleep(self.reconnectingTimeout )
            LOG.info(f'Try to reconnect!')
        
    def getSSLOptions(self):
        try:
            ca_certificate = os.path.abspath(self.ca_certificate)
            client_certificate = os.path.abspath(self.client_certificate)
            client_key = os.path.abspath(self.client_key)
            context = ssl.create_default_context(cafile=ca_certificate)
            context.load_default_certs()
            context.check_hostname = False
            context.load_cert_chain(certfile=client_certificate,keyfile=client_key,password=self.certificate_password)
            sslOpt = pika.SSLOptions(context, self.host)
            return sslOpt
        except:
            LOG.exception('Error while generating ssl-Options')
        return None
    
    def ConnectionParameters(self):
        if self.ssl_activate:
            return pika.ConnectionParameters(host=self.host,port=self.port,credentials=self.credentials,ssl_options=self.getSSLOptions())
        else:
            return pika.ConnectionParameters(host=self.host,port=self.port,credentials=self.credentials)
    
    def runPublisher(self):
        LOG.info(f'Create pika Publish-Connection with: host={self.host}, post={self.port}')
        self._connectionPublisher = pika.BlockingConnection(self.ConnectionParameters())
        self._channelPublish = self._connectionPublisher.channel()
        
        while self.publisherRun :
            item = self.queSendData.get()
            for topic in item.keys():
                msg = item[topic]
                LOG.info(f'publish data {topic}@{msg}')
                self._channelPublish .basic_publish(exchange=topic,
                        routing_key='',
                        body=msg)
                self.queSendData.task_done()
    
    def runConsumer(self):
        LOG.info(f'Create pika Consumer-Connection with: host={self.host}, post={self.port}')
        self._connectionConsumer = pika.BlockingConnection(self.ConnectionParameters())
        self._channelConsumer = self._connectionConsumer.channel()
        topicData = f'component.{self.component}.data.output'
        topicControl = f'component.{self.component}.control.output'
        self.bindExchangeConsumer(exchange=topicData,callback=self.callbackData)
        self.bindExchangeConsumer(exchange=topicControl,callback=self.callbackControl)
        LOG.info('self._channel.start_consuming()')
        self._channelConsumer.start_consuming()
        

    def startConsumer(self):
        self.consumerRun = True
        while self.consumerRun :
            try:
                self.runConsumer()
            except (pika.exceptions.IncompatibleProtocolError, pika.exceptions.StreamLostError):
                desc = f'Loosing Connection from {self.host}:{self.port}'
                LOG.warning(desc)
            except Exception as e:
                if self.consumerRun:
                    desc = f'Exception Connection from {self.host}:{self.port}'
                    LOG.exception(desc)
                #self.consumerRun = False
            time.sleep(self.reconnectingTimeout )
            LOG.info(f'Try to reconnect!')
        
        
    def stop(self):
        self.consumerRun = False
        self.publisherRun = False
        self._channelConsumer.stop_consuming()
        pass
        
        