from amqplib import client_0_8 as cli


def create_queue(ch, q_name):
    result = ch.queue_declare(
        queue=q_name,
        passive=False,
        durable=True,
        exclusive=False,
        auto_delete=False,
        nowait=False,
        arguments=None,
        ticket=None
    )
    return result


def put_message(ch, q_name):
    msg = cli.Message()
    ch.basic_publish(msg=msg,
                     exchange='',
                     routing_key=q_name,
                     mandatory=False,
                     immediate=False,
                     ticket=None)


def prepare(ch, q_name):
    result = create_queue(ch, q_name)

    if result[1] != 1:
        ch.queue_purge(q_name)
        put_message(ch, q_name)

if __name__ == '__main__':
    connection = cli.Connection()
    channel = cli.Channel(connection)
    queue_name = 'lock_queue'

    prepare(channel, queue_name)

