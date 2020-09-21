import os
import pika
import logging
from pathlib import Path

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).parent.parent
    logfile = Path.joinpath(ROOT_DIR, "jobs", "cron.log")

    logging.basicConfig(
        filename=logfile,
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
    )
    logging.info("Starting cron job")

    host = os.getenv("RABBIT_HOST", "rabbitmq")
    port = os.getenv("RABBIT_PORT", "5672")
    password = os.getenv("RABBIT_PASS", "")
    username = os.getenv("RABBIT_USER", "")

    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(
        host=host, port=int(port), credentials=credentials
    )

    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    exchange = "harvests"
    routing_key = "concept.all.HarvestTrigger"

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body="{}",
        properties=pika.BasicProperties(content_type="application/json"),
    )
    logging.info(" [x] Sent %r:%r" % (routing_key, "{}"))
    connection.close()
