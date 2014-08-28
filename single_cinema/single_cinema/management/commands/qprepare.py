from django.core.management.base import BaseCommand, CommandError
from amqplib import client_0_8 as cli


class Command(BaseCommand):
    help = 'Check queue and message existence.'

    def handle(self, *args, **options):
        self.connection = cli.Connection()
        self.channel = cli.Channel(self.connection)
        self.queue_name = 'lock_queue'

        self.prepare()

    def create_queue(self):
        result = self.channel.queue_declare(
            queue=self.queue_name,
            passive=False,
            durable=True,
            exclusive=False,
            auto_delete=False,
            nowait=False,
            arguments=None,
            ticket=None
        )
        return result

    def put_message(self):
        msg = cli.Message()

        self.channel.basic_publish(
            msg=msg,
            exchange='',
            routing_key=self.queue_name,
            mandatory=False,
            immediate=False,
            ticket=None)

    def prepare(self):
        result = self.create_queue()

        if result[1] != 1:
            self.channel.queue_purge(self.queue_name)
            self.put_message()