'''
@author: Nosov Dmitriy
'''
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(
host="172.16.4.155"))
channel = connection.channel()
channel.queue_purge(queue='requests')
channel.queue_declare(queue='responses', durable=True)
channel.basic_publish(exchange='', routing_key='responses', body="done",
              properties=pika.BasicProperties(
                 delivery_mode = 2, # make message persistent
              ))
connection.close()