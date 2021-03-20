Run detection:
`python detect.py --source data/images --save-txt --device cpu`

Croping images according to the bounding boxes founf:
`python crop_from_labels.py --in_image_path data/images --in_label_path runs/detect/exp/labels --out_data_path debug_output`
