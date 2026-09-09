# Here you load YOLO and run inference.

import cv2
from ultralytics import YOLO
from kafka import KafkaProducer
import json
import datetime

# 1. Crear el publicador (equivalente a tu nodo en ROS2)
# Tus compañeros te indicarán la IP y el puerto (por defecto suele ser localhost:9092)
producer = KafkaProducer(
    bootstrap_servers=['kafka_broker:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# El nombre del canal donde publicas (equivalente al topic)
topic_ocupacion = "afluencia_eventos_topic"

# Cargar el modelo (la versión Nano es ideal para probar la integración rápido)
model = YOLO("yolov8n.pt")      # Probar distintos modelos para la detección

# El patrón %06d le dice a OpenCV que busque números de 6 dígitos
ruta_secuencia = "Dataset/mall_dataset/frames/seq_%06d.jpg"
cap = cv2.VideoCapture(ruta_secuencia)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break # Fin de la secuencia de imágenes

    # Inferencia de YOLO filtrando solo personas (clase 0)
    results = model(frame, classes=[0], verbose=False) 
    
    total_personas = len(results[0].boxes)

    # Generación del contrato de datos
    datos_ocupacion = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "camera_id": "zona_centro_comercial",
        "total_people": total_personas
    }

    # # Esta parte hay que cambiarla por el POST del JSON
    # # Salida por consola para simular el envío al backend
    print(json.dumps(datos_ocupacion))

    # 2. Publicar el mensaje en el topic
    # Esto envía el JSON sin bloquear tu bucle de visión
    producer.send(topic_ocupacion, value=datos_ocupacion)

producer.flush() # Asegura que los últimos mensajes salgan antes de apagar
cap.release()
