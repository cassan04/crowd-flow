# Calculate density/occupation here

def count_people(results):
    """
    Recibe los resultados de YOLO y devuelve el número total de personas (clase 0).
    """
    total = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # 0 es el ID de la clase 'persona' en COCO
                total += 1
    return total