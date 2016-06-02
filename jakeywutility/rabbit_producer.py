# -*- coding:utf-8 -*-
# __author__ = 'jakey'

import pika
from pika.credentials import PlainCredentials


class AsyProducer:
    def __init__(self,
                 host,
                 port=5672,
                 user_name="guest",
                 password="guest",
                 connection_attempts=3,
                 heartbeat_interval=60 * 60,
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
        self.__channel_single = self.__connection.channel()
        self.__channel_work_queue = self.__connection.channel()
        self.__channel_subscribe = self.__connection.channel()
        self.__channel_routing = self.__connection.channel()
        self.__channel_topics = self.__connection.channel()

    def producer_single(self, queue_name, message):
        """
        push message to rabbit_mq broker, one-2-one is basic rabbit_mq
        :param message: str something you want to push
        :param queue_name: str assign a name as queue_name and routing_key
        :return:
        """
        if not queue_name or not isinstance(queue_name, str) or not isinstance(message, str):
            raise TypeError("参数有误, 请重新输入")

        self.__channel_single.queue_declare(queue=queue_name, durable=True)
        self.__channel_single.basic_publish(exchange='',
                                            routing_key=queue_name,
                                            body=message)

    def producer_work_queue(self, queue_name, message, durable=True, exchange=""):
        """
        push message to rabbit_mq broker, work queue is  distributed task system
        :param queue_name: str assign a name as queue_name
        :param message: str something you want to push
        :param durable: bool set queue be persistence
        :param exchange: string set exchange name default is ""
        :return:
        """
        if not isinstance(message, str):
            raise TypeError("推送数据类型为String")

        if not queue_name or not message:
            raise TypeError("参数有误, 请重新输入")

        self.__channel_work_queue.queue_declare(queue=queue_name, durable=durable)
        if exchange:
            self.__channel_work_queue.exchange_declare(exchange=exchange, type="direct")

        self.__channel_work_queue.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="text/plain"
            )
        )

    def producer_subscribe(self, message, exchange):
        """
        push message to rabbit_mq broker, this is publish/subscribe
        :param message: str something you want to push
        :param exchange:　string set exchange name
        :return:
        """
        if not exchange or not isinstance(exchange, str):
            raise TypeError("参数有误, 请重新输入")

        self.__channel_subscribe.exchange_declare(exchange=exchange, type="fanout")
        self.__channel_subscribe.basic_publish(
            exchange=exchange,
            routing_key="",
            body=message,
        )

    def producer_routing(self, message, exchange, routing_key):
        """
        push message to rabbit_mq broker, this is routing key
        :param message: str something you want to push
        :param routing_key: str or unicode
        :param exchange: string set exchange name
        :return:
        """
        if not exchange or not isinstance(exchange, str):
            raise TypeError("参数错误, 请重新输入")
        if not routing_key or not isinstance(routing_key, str) or not isinstance(message, str):
            raise TypeError("参数错误, 请重新输入")

        self.__channel_routing.exchange_declare(exchange=exchange, type="direct")
        self.__channel_routing.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message
        )

    def producer_topics(self, message, exchange, routing_key):
        """
        push message to rabbit_mq broker, this is fuzzy matching
        :param message: str something you want to push
        :param exchange: string set exchange name
        :param routing_key: str or unicode
        :return:
        """
        if not exchange or not isinstance(exchange, str) or not isinstance(message, str):
            raise TypeError("参数错误, 请重新输入")
        if not routing_key or not isinstance(routing_key, str) or '.' not in routing_key:
            raise TypeError("参数错误, 请重新输入")

        self.__channel_topics.exchange_declare(exchange=exchange, type="topic")
        self.__channel_topics.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

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

    def close(self):
        """
        断开链接
        :return:
        """
        self.__connection.close()


if __name__ == "__main__":
    import json
    message1 = json.dumps({"companyName": "杭州誉存科技有限公司"})
    connection = AsyProducer(host="192.168.31.114", user_name="sc-admin", password="1qaz2wsx")
    for i in range(201):
        connection.producer_work_queue(queue_name="task_queue", message=message1)
    connection.close()
    """
    for i in range(5):
        message1 = "testing_data"
        connection = AsyProducer(host="192.168.31.114", user_name="sc-admin", password="1qaz2wsx")
        # 基本用法
        connection.producer_single(queue_name='single', message=message1)
        # 分布式任务调度  从queue里面读取消息
        connection.producer_work_queue(queue_name="task_queue", message="admin")
        # 推送订阅系统　　绑定exchange和queue
        connection.producer_subscribe(message=message1, exchange="begin-publish-subscribe")
        # 按照准确routing_key发送接收消息
        connection.producer_routing(message=message1, routing_key="error", exchange="routing_test")
        # 按照不完全匹配发送接收消息
        connection.producer_topics(message=message1, routing_key="sys.info", exchange="topics_test")
    """

