import os
import pika

if __name__ == '__main__':
    host = os.getenv('RABBIT_HOST', 'rabbitmq')
    port = os.getenv('RABBIT_PORT', '5672')
    password = os.getenv('RABBIT_PASS', '')
    username = os.getenv('RABBIT_USER', '')

    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host=host, port=int(port), credentials=credentials)

    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    exchange = 'harvests'
    routing_key = 'ConceptAll.HarvestTrigger'

    channel.exchange_declare(exchange=exchange, exchange_type='topic')

    channel.basic_publish(exchange=exchange, routing_key=routing_key, body='{}', properties=pika.BasicProperties(
            content_type='application/json'
        ))
    print(" [x] Sent %r:%r" % (routing_key, '{}'))
    connection.close()
