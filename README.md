# python 常用的公共模块

------

project作者jakeywu   python只需要pip install https://github.com/jakeywu/jakeywutility.git

### 截止目前为止, 有如下公用方法:
> * 通用日志logging
> * 发送邮件(文本右键, 富文本邮件, 附件)
> * 代码方法检测(检测方法体运行的时间)
> * rabbit_mq的生产和消费


### 1. 通用日志logging 

```python
from jakeywutility.logger import get_logger
logger = get_logger()
logger.info("info")
```

### 2. 发送邮件
```python
from jakeywutility.emails import send_email
from jakeywutility.emails import send_attach
send_email(content="<p>Python 邮件发送测试...</p>", tos=["1226231147@qq.com"], subtype="html")
send_attach(content="<p>Python 邮件发送测试...</p>", tos=["1226231147@qq.com"], subtype="html", file_path="/home/jakey/pythonProjects/jakeywutility/jakeywutility/logger.py")
```

### 3. rabbit_mq的生产和消费
```python
# 生产者, 没有RPC远程方法调用, 因为我觉得RPC没太大的舞台了．
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
    
# 生产者, 没有RPC远程方法调用, 因为我觉得RPC没太大的舞台了．
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
```

