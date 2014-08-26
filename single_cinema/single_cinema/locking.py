from amqplib import client_0_8 as cli

QUEUE_NAME = 'lock_queue'
QUEUE_SIZE = 1

class Queue(object):
    def __init__(self):
        self.connection = cli.Connection()
        self.channel = cli.Channel(self.connection)
        self.channel.queue_delete(queue=QUEUE_NAME)
        self.channel.queue_declare(queue=QUEUE_NAME)
        # for item in xrange(QUEUE_SIZE):
        self.channel.basic_publish(exchange='', routing_key=QUEUE_NAME, msg=cli.Message())

class Mutex(object):
    def __init__(self):
        self.owner = None
        self.busy = False
        self.connection = cli.Connection()
        self.channel = cli.Channel(self.connection)
        # self.channel.queue_declare(queue=QUEUE_NAME)

    def aquire(self, owner):
        if not self.busy:
            self.msg = self.channel.basic_get(queue=QUEUE_NAME)
            if self.msg:
                self.busy = True
                self.owner = owner

    def release(self, owner):
        if self.busy and self.owner == owner:
            self.channel.basic_reject(delivery_tag=self.msg.delivery_tag, requeue=True)
            self.msg = None
            self.busy = False
            self.owner = None

# if __name__ == '__main__':
    # server = LockServ()
    # client = LockCli()

