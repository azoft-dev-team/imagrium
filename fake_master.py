import pika
from itertools import cycle

testcaseName = cycle(["testhelperFollowUser", "testhelperUnfollowUser"])

def _dummyConsume(ch, method, properties, body):
    ch.stop_consuming()

connection = pika.BlockingConnection(pika.ConnectionParameters(
host="localhost"))
channel = connection.channel()
channel.queue_declare(queue='requests', durable=True)
channel.queue_declare(queue='responses', durable=True)
channel.basic_consume(_dummyConsume, queue='responses', no_ack=True)

while True:
    channel.basic_publish(exchange='', routing_key='requests', body=testcaseName.next(),
                  properties=pika.BasicProperties(
                     delivery_mode = 2, # make message persistent
                  ))
    
    channel.queue_purge(queue='responses')
    channel.start_consuming()

connection.close()