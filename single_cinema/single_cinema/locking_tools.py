from amqplib import client_0_8 as cli

QUEUE_NAME = 'lock_queue'


def get_message():
    queue_name = QUEUE_NAME
    connection = cli.Connection()
    channel = cli.Channel(connection)
    msg = channel.basic_get(queue=queue_name, no_ack=True)

    return msg


def put_message():
    queue_name = QUEUE_NAME
    connection = cli.Connection()
    channel = cli.Channel(connection)

    channel.basic_publish(msg=cli.Message(), exchange='', routing_key=queue_name)
