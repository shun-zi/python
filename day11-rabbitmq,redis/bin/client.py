import pika
import random
import json

global taskIDList
global responseDict
global taskIDResult
responseDict = {}
taskIDList = []
taskIDResult = []

def on_response(ch, method, props, body):
    taskID = int(props.message_id)
    if taskID in taskIDList:
        try:
            responseDict[taskID].append(body.decode())
        except Exception:
            responseDict[taskID] = []
            responseDict[taskID].append(body.decode())
        taskIDResult.append(taskID)

def main():

    # 连接rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    # 声明exchange
    channel.exchange_declare(exchange='shuhai', exchange_type='direct')
    #声明接受结果的队列
    result = channel.queue_declare(exclusive=True)
    callback_queue = result.method.queue

    #回调函数
    channel.basic_consume(on_response, no_ack=True,
                            queue=callback_queue)

    # ipTidDict = {}

    while True:
        inputString = input(">>: ")
        if inputString == 'exit':
            break
        else:
            ipList = []
            if '--host' in inputString:
                # run

                # 随机生成一个整数值作为taskID,而且不能重复
                while True:
                    taskID = random.randint(0, 5000)
                    if taskID not in taskIDList:
                        # 分割输入字符串
                        list = inputString.split(' ')
                        list.reverse()
                        # 将ip存入列表中
                        for ip in list:
                            if ip == '--hosts':
                                break
                            elif ip == '':
                                continue
                            # ipTidDict[ip] = taskID
                            ipList.append(ip)
                        taskIDList.append(taskID)
                        break
                    else:
                        # 重新随机taskID值
                        continue

                send_to_serverString = inputString[:inputString.index('--hosts')-1]
                # print(send_to_serverString)

                for ip in ipList:
                    # 向服务端发送消息
                    channel.basic_publish(exchange='shuhai',
                                          routing_key=ip,
                                          properties=pika.BasicProperties(
                                              reply_to=callback_queue,
                                              message_id=str(taskID),
                                          ),
                                          body=send_to_serverString)
                print('task:%d'%taskID)

            else:
                # check_task
                list = inputString.strip().split(' ')
                length = len(list)
                taskID = int(list[length-1])
                if taskID not in taskIDResult:
                    print('该任务不存在')
                else:
                    for id in responseDict.keys():
                        if id == taskID:
                            for i in responseDict[id]:
                                print(i)



        # 接受结果队列中的信息
        connection.process_data_events()


main()