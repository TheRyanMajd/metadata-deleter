# Import Statements
import sys
import os
from PIL import Image

# Maximum number of pixels to allocate for a single image
Image.MAX_IMAGE_PIXELS = 933120000
print("\n********************************\nWelcome to Strip!\n********************************\n")

# Get the image file path from command-line arguments
path = sys.argv[1]
pwd = os.getcwd()
try:
    # Open the image
    image = Image.open(path)

    # Save the image without metadata by creating a new file named the same but adding 'stripped_' at the beginning.
    stripped_image_path = "stripped_" + path.split('/')[-1]
    image.save(stripped_image_path)
    absImgPath = os.path.join(pwd, stripped_image_path)
    # Output if functions correctly.
    print(f"Original Image: {path}")
    print(f"Image saved without metadata (stripped) to: {absImgPath}")
except FileNotFoundError:  # File not found
    print("File not found. Please check the file path.")
except IOError:  # IO error
    print("Cannot process the image file. Please ensure it's a valid image format.")
