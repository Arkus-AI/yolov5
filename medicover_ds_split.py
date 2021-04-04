from pathlib import Path
import numpy as np
import os
import shutil

yolo_ds_path = Path("/Datasets/medicover/processed/train/yolo/synthetic")
yolo_split_output_path = yolo_ds_path/"split"
train_path = yolo_ds_path/"train"
val_path = yolo_ds_path/"val"

src_img_dir = yolo_ds_path/"images"
src_lbl_dir = yolo_ds_path/"labels"
all_files = list(src_img_dir.glob("*.png"))

val_ratio = 0.1
n_samples = len(all_files)
n_val_samples = int(val_ratio*n_samples)
n_train_samples = n_samples-n_val_samples

val_samples = np.random.choice(all_files, n_val_samples, replace=False)
train_samples = set(all_files).difference(set(val_samples))

print(n_train_samples)

print(len(train_samples))
print(len(val_samples))
print(len(train_samples)+len(val_samples), "=", n_samples)

dst_img_dir = train_path/"images"
dst_lbl_dir = train_path/"labels"
if dst_img_dir.exists():
    shutil.rmtree(dst_img_dir)
    shutil.rmtree(dst_lbl_dir)

dst_img_dir.mkdir(exist_ok=True, parents=True)
dst_lbl_dir.mkdir(exist_ok=True, parents=True)
for img_path in train_samples:
    f_name = img_path.stem
    lbl_path = src_lbl_dir/f"{f_name}.txt"
    os.symlink(str(img_path), str(dst_img_dir/f"{f_name}.png"))
    os.symlink(str(lbl_path), str(dst_lbl_dir/f"{f_name}.txt"))

dst_img_dir = val_path/"images"
dst_lbl_dir = val_path/"labels"
dst_img_dir.mkdir(exist_ok=True, parents=True)
dst_lbl_dir.mkdir(exist_ok=True, parents=True)
for img_path in val_samples:
    f_name = img_path.stem
    lbl_path = src_lbl_dir/f"{f_name}.txt"
    os.symlink(str(img_path), str(dst_img_dir/f"{f_name}.png"))
    os.symlink(str(lbl_path), str(dst_lbl_dir/f"{f_name}.txt"))
