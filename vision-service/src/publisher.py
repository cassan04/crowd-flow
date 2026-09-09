# Here you manage how you send the data obtained from the video (API POST or MOM, better to use Kafka)

import json
import uuid
from kafka import KafkaProducer

class OccupancyPublisher:
    def __init__(self, broker='kafka:9092', topic='occupancy_topic'):
        self.topic = topic
        # Inicializa la conexión a Kafka
        self.producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def publish(self, camera_id, total_people, timestamp):
        # Genera el JSON con el ID único
        mensaje = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "camera_id": camera_id,
            "total_people": total_people
        }
        self.producer.send(self.topic, value=mensaje)