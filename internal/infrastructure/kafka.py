import confluent_kafka as ck
from typing import Callable


class Producer:
    def __init__(self, bootstrap_servers, client_id):
        self.__conf = {
            "bootstrap.servers": bootstrap_servers,
            "client_id": client_id
        }
        self.__producer = ck.Producer(**self.__conf)

    def produce(self, topic, value):
        self.__producer.produce(topic, value.encode('utf-8'))
        self.__producer.flush()


class Consumer:
    def __init__(self, bootstrap_servers, group_id, auto_offset_reset='earliest'):
        self.__conf = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset
        }
        self.__consumer = ck.Consumer(**self.__conf)

    def subscribe(self, topics):
        self.__consumer.subscribe(topics)

    def consume(self):
        return self.__consumer.poll(1, 0)

    def close(self):
        self.__consumer.close()

    def __del__(self):
        self.close()


def consume_messages(consumer: Consumer, msg_callback: Callable[[str], None], success_callback: Callable[[str], None] = None, error_callback: Callable[[str], None] = None):
    def safe_callback(callback, value):
        if callback is not None:
            callback(value)

    try:
        while True:
            msg = consumer.consume()
            if msg is None:
                continue
            if msg.error() and msg.error().code != ck.KafkaError._PARTITION_EOF:
                safe_callback(error_callback,
                              f"Error while consuming message: {msg.error()}")
                continue
            safe_callback(msg_callback, msg.value())
            safe_callback(success_callback, f"Received message: {msg.value()}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
