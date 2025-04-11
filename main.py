import math
import argparse
import colors
from PIL import Image


# Find the corresponding RGB values of pixel
def find_block_values(rgb_tuple, palette):
    min_distance = math.inf
    closest_block = None

    # Euclidean distance for closest RGB value
    for block in palette.values():
        distance = math.sqrt(
            (rgb_tuple[0] - block[0])**2 +
            (rgb_tuple[1] - block[1])**2 +
            (rgb_tuple[2] - block[2])**2
            )

        if distance < min_distance:
            min_distance = distance
            closest_block = block

    return closest_block


# Get the pixels of image
def pixelate_image(image):
    pixel_image = image.resize((64, 64), Image.BILINEAR)  # Change image.resize() values for different dimensions
    result_image = pixel_image.resize(image.size, Image.NEAREST)

    pixel_map = result_image.load()
    width, height = result_image.size

    return result_image, pixel_map, width, height


# Map every pixel into corresponding block
def pixel_to_block(image, pixel_map, width, height, palette):
    for i in range(width):
        for j in range(height):

            r, g, b = image.getpixel((i, j))

            corresponding_rgb_values = find_block_values((r, g, b), palette)

            pixel_map[i, j] = corresponding_rgb_values

    return image


# Scale the image into desired size by reducing number of pixels to process
def scale_image(image, scale_factor):
    width, height = image.size

    # Calculate new dimensions
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    # Scale the image to desired size
    scaled_image = image.resize((new_width, new_height))

    return scaled_image


def main():
    # Parser to change image
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='image0.jpg')
    args = parser.parse_args()

    # Load the image
    try:
        image = Image.open(args.filename)
    except FileNotFoundError:
        print("Error: Input file not found")
        return

    # Scale the image (integer is scale factor)
    scaled_image = scale_image(image, 1 / 3.0)

    # Get the pixelated values
    result_image, pixel_map, image_width, image_height = pixelate_image(scaled_image)

    # Map to blocks
    final_image = pixel_to_block(result_image, pixel_map, image_width, image_height, colors.palette)

    # Output image
    final_image.show()


if __name__ == '__main__':
    main()
