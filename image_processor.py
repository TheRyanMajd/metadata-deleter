import sys
import subprocess
from PIL import Image, ExifTags


Image.MAX_IMAGE_PIXELS = 933120000
# Set the maximum number of pixels for an image to prevent decompression bomb DOS attacks
Image.MAX_IMAGE_PIXELS = 933120000


class ImageProcessor:
    """
    A class to process images, including loading, displaying resolution, displaying EXIF data, stripping metadata, and comparing metadata with another image.

    Attributes:
        path (str): The file path of the image.
        image (PIL.Image.Image or None): The loaded image object.

    Methods:
        __init__(path):
            Initializes the ImageProcessor with the given image path and loads the image.

        load_image():
            Loads the image from the given path. Returns the image object if successful, otherwise returns None.

        print_resolution():
            Prints the resolution (width x height) of the loaded image.

        display_exif():
            Displays the EXIF data of the loaded image, if available.

        strip_metadata():
            Calls an external script (strip.py) to remove metadata from the image.

        compare_metadata(other_path):
            Compares the EXIF metadata of the loaded image with another image specified by the other_path.
    """

    def __init__(self, path):
        self.path = path
        self.image = self.load_image()

    def load_image(self):
        import subprocess
        try:
            return Image.open(self.path)
        except (FileNotFoundError, IOError):
            print("Error: Unable to load image. Please check the file path and format.")
            return None

    def print_resolution(self):
        if self.image:
            # self.image.size returns a tuple (width, height)
            width, height = self.image.size
            print(f"Resolution: {width} x {height}")

    def display_exif(self):
        if not self.image:
            return
        exif_data = self.image._getexif()
        if exif_data:
            print("EXIF Data:")
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                print(f"{tag_name:25}: {value}")
        else:
            print("No EXIF data found.")

    def strip_metadata(self):
        print("\nBringing you to strip.py...")
        try:
            subprocess.run(['python3', 'strip.py', self.path], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to call strip.py for metadata removal.")

    def compare_metadata(self, other_path):
        try:
            other_image = Image.open(other_path)
            exif1 = self.image._getexif()
            exif2 = other_image._getexif()
            if exif1 is None and exif2 is None:
                print("Both images have no EXIF data. ✅")
                return
            elif exif1 is None:
                print("The first image has no EXIF data. ❌")
                return
            elif exif2 is None:
                print("The second image has no EXIF data. ❌")
                return

            exif1_dict = {ExifTags.TAGS.get(
                tag, tag): value for tag, value in exif1.items()}
            exif2_dict = {ExifTags.TAGS.get(
                tag, tag): value for tag, value in exif2.items()}

            all_tags = set(exif1_dict.keys()).union(set(exif2_dict.keys()))

            print(f"\n{'Tag':<30} {'Image 1':<40} {'Image 2'}")
            print("-" * 80)
            for tag in sorted(all_tags):
                value1 = exif1_dict.get(tag, 'N/A')
                value2 = exif2_dict.get(tag, 'N/A')
                print(f"{tag:<30} {str(value1):<40} {str(value2)}")

            if exif1_dict == exif2_dict:
                print("\nThe metadata of both images is identical. ✅")
            else:
                print("\nThe metadata of the images is different. ❌")

        except (FileNotFoundError, IOError):
            print("Error: Unable to load one of the images for comparison.")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 image_processor.py <image_path> <option>")
        return

    path = sys.argv[1]
    option = sys.argv[2]
    processor = ImageProcessor(path)

    if option == '-i':
        print("\n********************************\n Image Stripper!\n********************************\n")
        processor.print_resolution()
        processor.display_exif()
        processor.strip_metadata()
    elif option == '-c':
        print("\n********************************\nWelcome to Checker!\n********************************\n")
        processor.print_resolution()
        processor.display_exif()
    elif option == '-cmp':
        if len(sys.argv) != 4:
            print("Usage: python3 image_processor.py <image1> -cmp <image2>")
            return
        print("\n********************************\nWelcome to Compare!\n********************************\n")
        other_path = sys.argv[3]
        processor.compare_metadata(other_path)
    else:
        print("Invalid option. Use -i, -c, or -cmp.")


if __name__ == "__main__":
    main()
