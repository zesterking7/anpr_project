import os
import json

def polygon_to_bbox(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    x_min = min(x_coords)
    y_min = min(y_coords)
    x_max = max(x_coords)
    y_max = max(y_coords)
    return x_min, y_min, x_max, y_max

def normalize_bbox(x_min, y_min, x_max, y_max, img_width, img_height):
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height

def save_yolo_format(filename, label, x_center, y_center, width, height):
    with open(filename, 'w') as f:
        f.write(f"{label} {x_center} {y_center} {width} {height}\n")

# Example JSON data (your provided data)
json_data = {
    "boxes": [
        {
            "type": "polygon",
            "label": "number plate",
            "x": "1243.9277",
            "y": "1342.8907",
            "width": "747.7665",
            "height": "263.6948",
            "points": [
                [
                    870.044475470746,
                    1290.3201966727163
                ],
                [
                    1617.810951053679,
                    1211.043269410626
                ],
                [
                    1616.9036946653937,
                    1348.6438216339272
                ],
                [
                    895.2460418120099,
                    1474.7380587105602
                ]
            ]
        }
    ],
    "height": 4144,
    "key": "img_27.jpg",
    "width": 1968
}


image_width = json_data["width"]
image_height = json_data["height"]

# Process each box in the JSON data
for box in json_data["boxes"]:
    points = box["points"]
    x_min, y_min, x_max, y_max = polygon_to_bbox(points)
    x_center, y_center, width, height = normalize_bbox(x_min, y_min, x_max, y_max, image_width, image_height)
    label = 0  # Assuming 'number plate' is class 0
    output_dir = 'dataset/labels/train'  # Directory to save annotations
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.splitext(json_data["key"])[0] + '.txt')
    save_yolo_format(output_file, label, x_center, y_center, width, height)
    print(f"Annotation saved to {output_file}")
