import argparse
import os
import shutil
from glob import glob
import cv2


def backup_large_files(input_glob):
    for filename in glob(input_glob, recursive=True):
        image = cv2.imread(filename)
        height, width, _ = image.shape

        if max(height, width) > 1024:
            backup_file = filename.replace('.jpg', '.original.jpg')
            # Create backup if none exists
            if ".original" not in filename and not os.path.exists(backup_file):
                shutil.move(filename, backup_file)


def create_small_versions(input_glob):
    for filename in [f for f in glob(input_glob, recursive=True) if '.original.' in f]:
        image = cv2.imread(filename)
        height, width, _ = image.shape

        longest_edge = 600
        img_scale = longest_edge / max(width, height)
        new_img = cv2.resize(image, (int(width * img_scale), int(height * img_scale)))
        cv2.imwrite(filename.replace(".original", ""), new_img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a template hugo post from a directory of images')
    parser.add_argument('--input', default="hugo/static/**/*.jpg", help='A glob for the input files')
    args = parser.parse_args()

    backup_large_files(input_glob=args.input)
    create_small_versions(input_glob=args.input)
