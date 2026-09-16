import cv2
import time
import json
import numpy as np
from datetime import datetime, timezone
from ultralytics import YOLO

# Importamos las herramientas de nuestros otros archivos
from publisher import OccupancyPublisher
from occupancy_calculator import count_people
from zone_mapper import map_people_to_zones

def cargar_zonas(ruta_json):
    with open(ruta_json, 'r') as f:
        zonas_dict = json.load(f)
    # OpenCV necesita que los polígonos sean arrays de numpy con formato int32
    return {nombre: np.array(puntos, dtype=np.int32) for nombre, puntos in zonas_dict.items()}

def main():
    # Inicializar herramientas
    model = YOLO("yolov8n.pt")
    publisher = OccupancyPublisher(broker='kafka:9092', topic='afluencia_personas_topic') # Ajusta el topic al tuyo
    
    # Cargar fuente de datos (la ruta relativa dentro de Docker) Ruta absoluta dentro del Docker
    cap = cv2.VideoCapture("/app/Dataset/mall_dataset/frames/seq_%06d.jpg")

    # Cargar las zonas desde el archivo generado
    zonas_poligonos = cargar_zonas("/app/zonas.json")

    # Variable para comprobar si ha habido un cambio en la cantidad de personas en la imágen
    last_estado_zonas = None
    publish_period = 2.0  # <-- 2. Aquí puedes cambiar el tiempo (ej: 0.5, 2.0 segundos)
    last_publish_time = 0.0 # Guarda la hora exacta del último envío

    # 3. Bucle principal de inferencia
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Fin de la secuencia de imágenes
        
        # Detectar con YOLO
        results = model(frame, verbose=False)
        
        # Calcular ocupación total (occupancy_calculator)
        total_people = count_people(results)

        # Mapear personas por zonas (zone_mapper)
        conteo_actual = map_people_to_zones(results, zonas_poligonos)

        # Conteo del tiempo actual
        current_time = time.time()
        
        # 4. Condición de publicación ajustada a diccionarios
        if (conteo_actual != last_estado_zonas) and ((current_time - last_publish_time) >= publish_period):
            tiempo_actual_iso = datetime.now(timezone.utc).isoformat()

            # Estructuramos el payload exacto para enviarlo a Kafka y poder imprimirlo
            mensaje_dict = {
                "camera_id": "zona_centro_comercial",
                "total_people": total_people,
                "zonas_data": conteo_actual,
                "timestamp": tiempo_actual_iso
            }

            # Publicamos el diccionario entero para que el backend tenga el desglose
            publisher.publish(
                camera_id="zona_centro_comercial",
                total_people=total_people,
                zonas_data=conteo_actual,
                timestamp=tiempo_actual_iso
            )
            
            print(f" Zonas actualizadas: {conteo_actual}")

            # Imprimimos el JSON formateado (bonito) en la consola de Docker
            print(" Mensaje JSON enviado a Kafka:")
            print(json.dumps(mensaje_dict, indent=4))

            last_estado_zonas = conteo_actual.copy()
            last_publish_time = current_time

    cap.release()

if __name__ == "__main__":
    main()