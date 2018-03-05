import pika
import json
import socket
import fcntl
import struct
import subprocess

def get_ip_address(ifname):
    # 获得计算机的外网地址
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pktString = fcntl.ioctl(skt.fileno(), 0x8915, struct.pack('256s', ifname[:15].encode('utf-8')))
    ipString = socket.inet_ntoa(pktString[20:24])
    return ipString

def callback(ch, method, properties, body):
    # 对客户端发送来的命令进行处理
    command_list = body.decode().split(' ',1)
    # 除去列表中的空字符
    for i in command_list:
        if i == '':
            del command_list[i]

    if command_list[0] == 'run':
        # 除去双引号(切片)
        command = command_list[1][1:-1]
        # 提取命令的每个参数,放进一个列表中
        command = command.split(' ')
        #执行命令
        try:
            result = subprocess.check_output(command)
        except Exception as e:
            result = e

        # 将结果发送给结果队列
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(
                             message_id=properties.message_id
                         ),
                         body=result)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    elif command_list[0] == 'check_task':
        pass

    print(result)


def main():
    # 连接远程计算机的rabbitmq
    credentials = pika.PlainCredentials('shunzi', 'z960520@')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.112', 5672,
                                                                   '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='shuhai', exchange_type='direct', )
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    ipAdress = get_ip_address('wlp15s0')

    channel.queue_bind(exchange='shuhai', queue=queue_name, routing_key=ipAdress)
    # 接受客户端发送来的信息
    channel.basic_consume(callback,
                          queue=queue_name)

    channel.start_consuming()

main()





