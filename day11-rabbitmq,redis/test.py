import pika
#
# credentials = pika.PlainCredentials('shunzi', 'z960520@')
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     '192.168.189.129', 5672, '/', credentials))
# channel = connection.channel()
#
# # 声明queue
# channel.queue_declare(queue='hello')
#
# # n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# # connection.close()
# import socket
# import fcntl
# import struct
#
# def get_ip_address(ifname):
#     skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     pktString = fcntl.ioctl(skt.fileno(), 0x8915, struct.pack('256s', ifname[:15].encode('utf-8')))
#     ipString = socket.inet_ntoa(pktString[20:24])
#     return ipString
# get_ip_address('wlp15s0')

# import subprocess
# try:
    #    out_bytes = subprocess.check_output(['netstat','-a'])
# except Exception as e:
#     print(out_bytes.decode())
#
# print(out_bytes.decode())
import random

a = {}
for i in range(0,5):
    try:
        a[1].append(1)
    except Exception:
        a[1] = []
        a[1].append(2)


print(a)

string = '"df -h"'
print(string[1:-1].split(' '))
