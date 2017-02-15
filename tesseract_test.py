import pytesseract
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name')
args = parser.parse_args()

im = Image.open(args.name)
print(pytesseract.image_to_string(im))
im.close()
