from pathlib import Path
import argparse
import shutil
import logging
import cv2
import math

CFD = Path(__file__).parent
# >>> Configuring logger
log_file = Path(__file__).stem + ".log"
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename=log_file, level=logging.INFO, filemode="a")
logger = logging.getLogger(__name__)

def crop_image(img, label: str):
    label = [float(lbl) for lbl in label.split(" ")]
    logger.debug(label)

    h,w,c = img.shape
    class_, x_center, y_center, width, height = label
    x_start = math.floor((x_center-width/2)*w)
    x_end = math.ceil((x_center+width/2)*w)
    y_start =   math.floor((y_center-height/2)*h)
    y_end =     math.ceil((y_center+height/2)*h)

    crop = img[y_start:y_end,x_start:x_end,  :]


    logger.debug([x_start, x_end, y_start, y_end])

    return crop, int(class_)


def main( in_image_path, in_label_path, out_data_path,):

    logger.info(f"Starting processing {in_image_path}")

    for out_path in [out_data_path]:
        if out_path.exists():
            shutil.rmtree(out_path)
        out_path.mkdir(parents=True)
    
    labels_in = in_label_path.glob("*.txt")

    for label in labels_in:
        sample_name = label.stem
        # Find corresponding image
        image_path = next(iter(in_image_path.glob(f"{sample_name}*")))
        img_ext = image_path.suffix
        
        logger.debug(sample_name)
        logger.debug(image_path)

        # Read image and label
        img = cv2.imread(str(image_path))

        with open(label) as infile:
            labels = [line.strip() for line in infile.readlines()]
        
        for i, label in enumerate(labels):
            crop, class_ = crop_image(img, label)
            cv2.imwrite(str(out_data_path/f"{sample_name}_{i}_{class_}{img_ext}"), crop)


if __name__ == "__main__":
    # Arg parser
    parser = argparse.ArgumentParser()

    parser.add_argument("--in_image_path",
                        type=Path,
                        required=True,
                        help="Path to directory for the input images")
    parser.add_argument("--in_label_path",
                        type=Path,
                        required=True,
                        help="Path to directory for the input labels")
    parser.add_argument("--out_data_path",
                        type=Path,
                        required=True,
                        help="Path to directory for the ouput data")

    args = parser.parse_args()

    # Checking that path exists
    for path_ in [args.in_image_path, args.in_label_path]:
        assert path_.exists(), \
            f"No input path, {path_}"

    main(
        args.in_image_path,
        args.in_label_path,
        args.out_data_path,
    )
