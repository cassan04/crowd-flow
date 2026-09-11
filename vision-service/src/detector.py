import cv2
import time
import json
import numpy as np
from datetime import datetime, timezone
from ultralytics import YOLO

# Importamos las herramientas de nuestros otros archivos
from publisher import OccupancyPublisher
from occupancy_calculator import count_people

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
        
        # 2. Inicializar el contador para las zonas de este frame
        conteo_actual = {nombre: 0 for nombre in zonas_poligonos.keys()}
        
        total_people = count_people(results)

        # 3. Extraer coordenadas y comprobar intersecciones
        for r in results:
            for box in r.boxes:
                # Comprobar que la detección es una persona (clase 0 en COCO)
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Calcular el punto de los pies (centro de la base de la caja)
                    centro_x = int((x1 + x2) / 2)
                    base_y = int(y2)
                    punto_pies = (centro_x, base_y)

                    # Comprobar en qué zona cae el punto
                    for nombre_zona, poligono in zonas_poligonos.items():
                        # pointPolygonTest devuelve >= 0 si el punto está dentro o en el borde
                        if cv2.pointPolygonTest(poligono, punto_pies, False) >= 0:
                            conteo_actual[nombre_zona] += 1
                            break # Asumimos que las zonas no se solapan

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