# import pika
# import json
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.exchange_declare(exchange='shunzni',exchange_type='fanout')
# # channel.queue_declare(queue='shunzi')
#
# message = ['dhsj','sdskds']
# print(type(json.dumps(message)))
#
# channel.basic_publish(exchange='shunzi',
#                       routing_key=json.dumps(['hehe','he']).encode(),
#                       body=json.dumps(message))
# print('1')

import pika
import random

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='hello')

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      properties=pika.BasicProperties(
                          message_id=str(random.randint(0,10))
                      ),
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")