import pika
import base64
import os
import uuid
#from celery import Celery
#os.system("python3 ~/django/ml/worker/listen.py")
#from random import randint
credentials = pika.PlainCredentials('root', '')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials, heartbeat_interval=10)

class MQ:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
        self.corr_id = str(uuid.uuid4())
        result = self.channel.queue_declare(exclusive=False)

        self.callback_queue = result.method.queue

    def response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            print('## DONE TRACKING: ' + body.decode())
        self.channel.stop_consuming()

    def send(self, data, queue):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_publish(exchange='',
                            routing_key=queue,
                            properties=pika.BasicProperties(
                             reply_to = self.callback_queue,
                             correlation_id = self.corr_id,
                             ),
                            body=data)
        print('SENT: '+data)
        data = None
        self.channel.basic_consume(self.response, queue=self.callback_queue, no_ack=True)
        self.channel.start_consuming()

    def sendRel(self, data, queue):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=data)
        print('SENT: '+data)
        data = None
