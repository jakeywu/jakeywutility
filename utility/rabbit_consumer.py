# __author__ = 'jakey'

import pika
from pika.credentials import PlainCredentials


class AsyConsumer:
    """
    rabbit_mq connections parameters object is selected
    """
    def __init__(self,
                 host,
                 port=5672,
                 user_name="guest",
                 password="guest",
                 connection_attempts=3,
                 heartbeat_interval=60*60,
                 channel_max=200,
                 virtual_host="/",
                 ssl=False):
        """
            connect to rabbit mq
            :param str host: Hostname or IP Address to connect to
            :param int port: TCP port to connect to
            :param str user_name: default is guest
            :param str password:  default is guest
            :param int connection_attempts: Maximum number of retry attempts
            :param int heartbeat_interval: How often to send heartbeats.
                                          Min between this value and server's proposal
                                          will be used. Use 0 to deactivate heartbeats
                                          and None to accept server's proposal.
            :param int channel_max: Maximum number of channels to allow
            :param str virtual_host: RabbitMQ virtual host to use
            :param bool ssl: Enable SSL
            :return:
        """
        self.host = host
        self.port = port
        self.connection_attempts = connection_attempts
        self.channel_max = channel_max
        self.heartbeat_interval = heartbeat_interval
        self.credentials = PlainCredentials(username=user_name, password=password)
        self.virtual_host = virtual_host
        self.ssl = ssl
        self.__connection = self.__connection_rabbit()

    def __connection_rabbit(self):
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            channel_max=self.channel_max,
            connection_attempts=self.connection_attempts,
            heartbeat_interval=self.heartbeat_interval,
            virtual_host=self.virtual_host,
            ssl=self.ssl
        )
        return pika.BlockingConnection(parameters)

    def consumer_single(self, queue_name, function, no_ack=False):
        """
        consume message from rabbit_mq broker, single is one producer 2 one consumer
        :param queue_name: str assign a name as queue_name
        :param no_ack: bool decision a message is recall or not
        :param function: function is real messages where you can receive
        :return:
        """
        if not queue_name or not isinstance(queue_name, str) or not isinstance(no_ack, bool):
            raise TypeError("参数有误, 请重新输入")

        connection = self.__connection
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(function, queue=queue_name, no_ack=no_ack)
        channel.start_consuming()

    def consumer_work_queue(self, queue_name, function, prefetch_count=1, durable=True):
        """
        consume message from rabbit_mq broker, work queue is distributed task system
        :param queue_name: str assign a name as queue_name
        :param function: function is real messages where you can receive
        :param durable: boolean set queue be persistence
        :param prefetch_count: how many messages you can put in buffer
        :return:
        """
        if not prefetch_count or not isinstance(prefetch_count, int) or not isinstance(durable, bool):
            raise TypeError("参数有误, 请重新输入")

        connection = self.__connection
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=durable)
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(function, queue=queue_name)
        channel.start_consuming()

    def consumer_subscribe(self, exchange, function):
        """
        consumer message from rabbit_mq broker, subscribe is publish/subscribe
        :param exchange: string set exchange name
        :param function: function is real messages where you can receive
        :return:
        """
        if not exchange or not isinstance(exchange, str):
            raise TypeError("参数有误, 请重新输入")

        connection = self.__connection
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, type='fanout')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange, queue=queue_name)
        channel.basic_consume(function, queue=queue_name, no_ack=True)
        channel.start_consuming()

    def consumer_routing(self, exchange, binding_keys, function):
        """
        consumer message from rabbit_mq broker, routing is combine by sure key
        :param exchange: string set exchange name
        :param binding_keys: list(str or unicode)
        :param function: function is real messages where you can receive
        :return:
        """
        if not exchange or not isinstance(exchange, str):
            raise TypeError("参数有误, 请重新输入")
        if not binding_keys or not isinstance(binding_keys, list):
            raise TypeError("参数有误, 请重新输入")

        connection = self.__connection
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        for binding_key in binding_keys:
            if not binding_key or not isinstance(binding_key, str):
                raise TypeError("参数有误, 请重新输入")
            channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=binding_key)
        channel.basic_consume(function, queue=queue_name)
        channel.start_consuming()

    def consumer_topics(self, exchange, binding_keys, function):
        """
        consumer message from rabbit_mq broker, consumer_topics is fuzzy matching
        :param exchange: string set exchange name
        :param binding_keys: list(str or unicode)
        :param function: function is real messages where you can receive
        :return:
        """
        if not exchange or not isinstance(exchange, str):
            raise TypeError("参数错误, 请重新输入")
        if not binding_keys or not isinstance(binding_keys, list):
            raise TypeError("参数错误, 请重新输入")

        connection = self.__connection
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, type='topic')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        for binding_key in binding_keys:
            if not binding_key or not isinstance(binding_key, str):
                raise TypeError("参数错误, 请重新输入")
            channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=binding_key)

        channel.basic_consume(function, queue=queue_name, no_ack=True)
        channel.start_consuming()

if __name__ == "__main__":
    pass
    """
    asy_consumer = AsyConsumer(host="192.168.31.114", user_name="sc-admin", password="1qaz2wsx")
    def callback(ch, method, properties, body):
        print(body)
        # ============================
        # 只有消费分布式任务模型才会
        # ch.basic_ack(delivery_tag=method.delivery_tag)
        #  ============================
    # 消费一对一模型
    asy_consumer.consumer_single("single", callback)
    # 消费分布式任务模型(ch.basic_ack(delivery_tag=method.delivery_tag))
    asy_consumer.consumer_work_queue("task_queue", callback)
    # 消费订阅式模型
    asy_consumer.consumer_subscribe("begin-publish-subscribe", callback)
    # routing_key 模型
    asy_consumer.consumer_routing("routing_test", ["error"], callback)
    # topics 模型
    asy_consumer.consumer_topics(exchange="topics_test", binding_keys=["*.info", "*.sys"], function=callback)
    """
