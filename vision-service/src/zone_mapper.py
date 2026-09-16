# Map detections
# vision-service/src/zone_mapper.py
import cv2

def map_people_to_zones(results, zonas_poligonos):
    # Inicializamos el diccionario a 0
    conteo = {nombre: 0 for nombre in zonas_poligonos.keys()}
    
    # Extraemos coordenadas y comprobamos intersecciones
    for r in results:
        for box in r.boxes:
            # Clase 0 es persona en COCO
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                centro_x = int((x1 + x2) / 2)
                base_y = int(y2)
                punto_pies = (centro_x, base_y)

                # Mapear el punto a su zona
                for nombre_zona, poligono in zonas_poligonos.items():
                    if cv2.pointPolygonTest(poligono, punto_pies, False) >= 0:
                        conteo[nombre_zona] += 1
                        break # Asumimos que no se solapan
                        
    return conteo