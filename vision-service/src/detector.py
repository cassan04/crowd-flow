import cv2
import time
from datetime import datetime, timezone
from ultralytics import YOLO

# Importamos las herramientas de nuestros otros archivos
from publisher import OccupancyPublisher
from occupancy_calculator import count_people

def main():
    # 1. Inicializar herramientas
    model = YOLO("yolov8n.pt")
    publisher = OccupancyPublisher(broker='kafka:9092', topic='afluencia_personas_topic') # Ajusta el topic al tuyo
    
    # 2. Cargar fuente de datos (la ruta relativa dentro de Docker) Ruta absoluta dentro del Docker
    cap = cv2.VideoCapture("/app/Dataset/mall_dataset/frames/seq_%06d.jpg")

    # Variable para comprobar si ha habido un cambio en la cantidad de personas en la imágen
    last_amount_people = None
    publish_period = 2.0  # <-- 2. Aquí puedes cambiar el tiempo (ej: 0.5, 2.0 segundos)
    last_publish_time = 0.0 # Guarda la hora exacta del último envío

    # 3. Bucle principal de inferencia
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Fin de la secuencia de imágenes
        
        # Detectar con YOLO
        results = model(frame, verbose=False)
        
        # Calcular métricas usando el módulo externo
        personas_detectadas = count_people(results)

        # Comprobación de condiciones para publicar
        current_time = time.time() # Obtenemos el reloj actual en segundos

        # Solo entraremos si ocurren AMBAS cosas
        if (personas_detectadas != last_amount_people) and ((current_time - last_publish_time) >= publish_period):
            tiempo_actual_iso = datetime.now(timezone.utc).isoformat()

            publisher.publish(
                camera_id="zona_centro_comercial",
                total_people=personas_detectadas,
                timestamp=tiempo_actual_iso
            )
            
            print(f" Enviado: {personas_detectadas} personas detectadas.")

            # Actualizamos las variables DENTRO del if
            # Así solo registramos el estado cuando realmente sale un mensaje a Kafka
            last_amount_people = personas_detectadas
            last_publish_time = current_time

    cap.release()

if __name__ == "__main__":
    main()