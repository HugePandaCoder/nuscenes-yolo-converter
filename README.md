# NuScenes to YOLO Converter

This repository provides a simple script to convert [nuScenes](https://www.nuscenes.org/) (or [nuImages](https://www.nuscenes.org/nuimages)) annotation data into the [YOLO](https://github.com/ultralytics/yolov5) format.  
It includes an **example** using a **mini subset** (about 50 images) from [nuImages](https://www.nuscenes.org/nuimages#download), so you can explore or test the data without downloading the entire dataset.

---

## Contents
1. `nuscenes_to_yolo.py` - The main conversion script.
2. `README.md` - Usage instructions (this file).
3. (Optional) A small **example subset** of the dataset:
   - **`sample_data.json`** (mini version)
   - **`category.json`** (mini version)
   - **`object_ann.json`** (mini version)
   - Other metadata files (as needed) in a mini form.

---

## 1. How to Obtain the Mini Subset

- Go to [nuImages Download Page](https://www.nuscenes.org/nuimages#download).
- Download one of the smaller “mini” subsets (e.g., `nuimages-vX.X-mini.tgz`).
- Unzip the files somewhere on your computer.

> **Note**: This subset should include the necessary JSON metadata files (like `sample_data.json`, `category.json`, `object_ann.json`, etc.) and enough image files to test the script.

---

## 2. Repository File Structure

Below is a recommended structure for your repository:

```
nuscenes_to_yolo/
├── nuscenes_to_yolo.py
├── README.md
├── example_data/              # (Optional) Example mini subset placed here
│   ├── category.json
│   ├── object_ann.json
│   ├── sample_data.json
│   ├── ... other *.json files ...
│   └── samples/               # directory containing the actual images
├── yolo_annotations/          # output folder (auto-created by the script if desired)
└── ...
```

- **`nuscenes_to_yolo.py`**: The main script where you’ll configure file paths and run the conversion.  
- **`example_data/`**: A sample folder containing the mini dataset JSON files (and optional images).  
- **`yolo_annotations/`**: The directory where the YOLO `.txt` files will be saved after conversion.

---

## 3. Script Configuration and Usage

1. **Clone or Download the Repository**  
   ```bash
   git clone https://github.com/HugePandaCoder/nuscenes_to_yolo.git
   cd nuscenes_to_yolo
   ```

2. **Prepare Python Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or on Windows: .\venv\Scripts\activate
   ```

3. **Place or Verify the Mini Subset**  
   - Ensure the JSON files (`category.json`, `object_ann.json`, `sample_data.json`, etc.) are in `example_data/` (or another folder of your choice).
   - Make sure the folder structure matches how the JSON references the images (e.g., `samples/` folder).

4. **Configure the Script**  
   Open `nuscenes_to_yolo.py` and set the following variables at the top:
   ```python
   JSON_DIR = "./example_data"        # Path to the mini dataset JSON files
   OUTPUT_DIR = "./yolo_annotations"  # Where YOLO .txt files will be saved
   PROCESS_ONLY_KEY_FRAMES = True     # Set to False if you want to process ALL frames
   ```

5. **Run the Script**  
   ```bash
   python nuscenes_to_yolo.py
   ```

6. **Check the Output**  
   - Look in the `yolo_annotations/` folder. You should see `.txt` files corresponding to the images in the mini dataset.
   - Each line in these `.txt` files will follow the YOLO format:
     ```
     <class_id> <center_x> <center_y> <width> <height>
     ```
     where all coordinates are **normalized** by image width and height.

---

## 4. Expected Output (Example)

If you have a single image named `something.jpg`, you might get a `.txt` file in `yolo_annotations/something.txt` with lines like:

```
0 0.50312 0.44723 0.11250 0.20567
3 0.65298 0.51230 0.20412 0.17540
```

Here:
- `0` and `3` are the class IDs mapped from `category.json`.
- `0.50312` is the `center_x` coordinate, etc., all normalized.

---

## 5. Notes and Tips

- **Category Mapping**:  
  The script enumerates categories from `category.json` in the order they appear. If you want a more custom mapping (e.g., always `car = 0`, `pedestrian = 1`), you can modify the `category_to_class_id` dictionary accordingly.

- **Skipping Unrecognized Categories**:  
  If any annotation references a category token **not** found in `category.json`, the script will skip it (or handle it based on your preferences).

- **Images Not Required**:  
  Technically, the conversion can run even if the images aren’t present (it just needs the image width/height from the JSON). But to verify bounding boxes visually, you’ll need the images.

- **PROCESS_ONLY_KEY_FRAMES**:  
  By default, we only convert annotations for frames marked as “key frames.” If you want **all** frames in the subset, set `PROCESS_ONLY_KEY_FRAMES = False`.

---

## 6. License

[MIT License](LICENSE)  
Feel free to modify and distribute under the terms of the MIT License.

---

**Happy converting!**  
If you have any questions or feedback, please open an issue or contact me directly.
