# import pika
# import json
# credentials = pika.PlainCredentials('shunzi', 'z960520@')
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     '192.168.0.112', 5672, '/', credentials))
# channel = connection.channel()
#
# # You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# # We could avoid that if we were sure that the queue already exists. For example if send.py program
# # was run before. But we're not yet sure which program to run first. In such cases it's a good
# # practice to repeat declaring the queue in both programs.
# channel.exchange_declare(exchange='shunzi', exchange_type='fanout')
# result = channel.queue_declare(exclusive=True) #不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
# queue_name = result.method.queue
# channel.queue_bind(exchange='shunzi', queue=queue_name)
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % json.loads(body.decode()))
#
#
# channel.basic_consume(callback,
#                       queue=queue_name,
#                       no_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print(type(properties.message_id))


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()