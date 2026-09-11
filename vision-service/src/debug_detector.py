import cv2
import json
import numpy as np
from ultralytics import YOLO

def cargar_zonas(ruta_json):
    with open(ruta_json, 'r') as f:
        return {nombre: np.array(puntos, dtype=np.int32) for nombre, puntos in json.load(f).items()}

def main():
    model = YOLO("yolov8n.pt")
    
    # 1. Cargar zonas y una única imagen
    zonas_poligonos = cargar_zonas("/app/zonas.json")
    ruta_imagen = "/app/Dataset/mall_dataset/frames/seq_000002.jpg"
    
    # Usamos imread en lugar de VideoCapture para una sola foto
    frame = cv2.imread(ruta_imagen)
    if frame is None:
        print(f"Error: No se pudo cargar la imagen en {ruta_imagen}")
        return

    conteo_actual = {nombre: 0 for nombre in zonas_poligonos.keys()}
    
    # 2. Inferencia de YOLO
    results = model(frame, verbose=False)

    # 3. Dibujar las zonas (Polígonos azules)
    for nombre_zona, poligono in zonas_poligonos.items():
        # cv2.polylines requiere una lista de polígonos
        cv2.polylines(frame, [poligono], isClosed=True, color=(255, 0, 0), thickness=2)
    
    # 4. Procesar detecciones y dibujar personas
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                centro_x = int((x1 + x2) / 2)
                base_y = int(y2)
                punto_pies = (centro_x, base_y)

                # Dibujar la caja delimitadora de la persona (Verde)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)

                # Comprobar si el punto cae dentro de alguna zona
                en_zona = False
                for nombre_zona, poligono in zonas_poligonos.items():
                    if cv2.pointPolygonTest(poligono, punto_pies, False) >= 0:
                        conteo_actual[nombre_zona] += 1
                        en_zona = True
                        break

                # Dibujar el punto de los pies: Naranja si está en zona, Rojo si está fuera
                color_punto = (0, 165, 255) if en_zona else (0, 0, 255)
                cv2.circle(frame, punto_pies, radius=5, color=color_punto, thickness=-1)

    print(f"Resultado del conteo: {conteo_actual}")

    # 5. Guardar la imagen procesada
    ruta_salida = "/app/debug_salida.jpg"
    cv2.imwrite(ruta_salida, frame)
    print(f"Imagen guardada con éxito en: {ruta_salida}")

if __name__ == "__main__":
    main()