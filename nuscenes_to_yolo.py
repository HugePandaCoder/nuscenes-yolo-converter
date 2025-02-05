import os
import json

# =====================================
# User-configurable variables
# =====================================
# 1. Directory where all the JSON files are located.
JSON_DIR = "./path/to/json/files"

# 2. Output directory for YOLO annotations.
OUTPUT_DIR = "./yolo_annotations"

# 3. Which sample_data keys to process (e.g., all key frames).
#    By default, we only process if sample['is_key_frame'] == True.
PROCESS_ONLY_KEY_FRAMES = True

# =====================================
# Main script
# =====================================

def load_json(filename):
    """Helper function to load a JSON file."""
    with open(os.path.join(JSON_DIR, filename), 'r') as f:
        return json.load(f)

def main():
    # Load JSON files
    categories = load_json('category.json')
    object_anns = load_json('object_ann.json')
    sample_data = load_json('sample_data.json')

    # Create a mapping from category token to a numeric class ID
    category_to_class_id = {cat['token']: idx for idx, cat in enumerate(categories)}

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process each sample in 'sample_data'
    for sample in sample_data:
        # If PROCESS_ONLY_KEY_FRAMES is True, skip samples that are not key frames
        if PROCESS_ONLY_KEY_FRAMES and not sample['is_key_frame']:
            continue

        image_width = sample['width']
        image_height = sample['height']
        image_filename = sample['filename']
        image_token = sample['token']

        # Get all object annotations for this image
        object_annotations = [ann for ann in object_anns if ann['sample_data_token'] == image_token]

        # Prepare YOLO annotation filename
        base_name = os.path.splitext(os.path.basename(image_filename))[0]
        yolo_annotation_file = os.path.join(OUTPUT_DIR, base_name + '.txt')

        # Write annotations in YOLO format
        with open(yolo_annotation_file, 'w') as f:
            for ann in object_annotations:
                # Get category ID and class ID
                category_id = ann['category_token']
                class_id = category_to_class_id.get(category_id, -1)
                if class_id == -1:
                    # If category not found in mapping, skip or handle differently
                    continue

                # Get bounding box coordinates (x_min, y_min, x_max, y_max)
                x_min, y_min, x_max, y_max = ann['bbox']

                # Convert to YOLO format (center_x, center_y, width, height) normalized by image size
                center_x = ((x_min + x_max) / 2) / image_width
                center_y = ((y_min + y_max) / 2) / image_height
                width = (x_max - x_min) / image_width
                height = (y_max - y_min) / image_height

                # Write a single line for each object in YOLO format
                f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")

    print(f"YOLO annotations have been saved to {OUTPUT_DIR}.")

if __name__ == "__main__":
    main()
