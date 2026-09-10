import cv2
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

    # 3. Bucle principal de inferencia
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Fin de la secuencia de imágenes
        
        # A. Detectar con YOLO
        results = model(frame, verbose=False)
        
        # B. Calcular métricas usando el módulo externo
        personas_detectadas = count_people(results)
        
        # C. Publicar a Kafka usando el módulo externo
        tiempo_actual = datetime.now(timezone.utc).isoformat()
        publisher.publish(
            camera_id="zona_centro_comercial",
            total_people=personas_detectadas,
            timestamp=tiempo_actual
        )
        
        print(f"Enviado: {personas_detectadas} personas detectadas.")

    cap.release()

if __name__ == "__main__":
    main()