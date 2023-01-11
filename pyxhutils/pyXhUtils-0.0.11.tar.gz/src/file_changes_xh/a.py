from kafka import KafkaConsumer
import datetime as dt
if __name__ == "__main__":
    consumer = KafkaConsumer(
        bootstrap_servers=['stunning-lioness-11895-us1-kafka.upstash.io:9092'],
        sasl_mechanism='SCRAM-SHA-256',
        security_protocol='SASL_SSL',
        sasl_plain_username='c3R1bm5pbmctbGlvbmVzcy0xMTg5NSSe5bc8GX6KTQuG_8JxipLUeY8zqKq_7bk',
        sasl_plain_password='6679c9467f6d4abe9b1b1a5a15d0a790',
        group_id='$GROUP_NAME',
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000*30,
    )
    consumer.subscribe("web-access-log")
    consumer.poll(timeout_ms=100)
    consumer.seek_to_beginning()

    last_date = dt.datetime.now()
    with open("log-processed.log", "w") as f:

        for msg in consumer:
            data = msg.value
            print(data, end="")
            f.write(data)
    # ...
    # consumer.close()

    # consumer.seek(0, 0)

