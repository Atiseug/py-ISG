import cv2
import imageio as iio
import os
import random
import string
from natsort import natsorted
from PIL import Image
from shutil import rmtree

# Default Settings
# set 0 to not resize (on 0 files are completely readable after the saving, but YouTube will damage it)
# Videos with higher resolution will be almost the same by size (sometimes even bigger) but they will process faster as
# there are fewer frames to process
RESIZE_TIMES = 4
WIDTH = 1280 if not RESIZE_TIMES else int(1280 / RESIZE_TIMES)
HEIGHT = 720 if not RESIZE_TIMES else int(720 / RESIZE_TIMES)
BYTES_PER_IMAGE = int(WIDTH * HEIGHT / 8)
FPS = 30


def create_temp_dir():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(temp_dir := os.path.join(current_dir, "IMAGE_TEMP"))
    return temp_dir


def get_sorted_filenames_list(dir_path):
    files_sorted_list = natsorted(os.listdir(os.path.normpath(dir_path)))
    return files_sorted_list


def create_images_from_video(video_path, save_path, mode="iio"):
    # cv2 way
    if mode == "cv2":
        vidcap = cv2.VideoCapture(os.path.normpath(video_path))
        count = 0
        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(os.path.join(save_path, f"{count}.jpg"), image)
            count += 1

    # imageIO way
    if mode == "iio":
        for index, frame in enumerate(iio.imiter(os.path.normpath(video_path))):
            iio.imwrite(os.path.join(save_path, f"{index}.jpg"), frame)


def create_video_from_images(img_dir, video_path):
    images_list = get_sorted_filenames_list(img_dir)
    with iio.get_writer(f"{os.path.normpath(video_path)}.mp4", fps=FPS) as writer:
        for image_name in images_list:
            image_file = iio.v2.imread(os.path.join(img_dir, image_name))
            writer.append_data(image_file)


def get_bytes_from_file(file_path):
    with open(os.path.normpath(file_path), "rb") as file:
        file_data = file.read()
        data_len = len(file_data)
        # Make the length of bytes a multiple of the picture size
        if (rest := data_len % BYTES_PER_IMAGE) != 0:
            file_data += b"\x00" * (BYTES_PER_IMAGE - rest)
            data_len = len(file_data)
    return file_data, data_len


def create_picture_from_bytes(byte_data, save_dir, img_name):
    if BYTES_PER_IMAGE != len(byte_data):
        raise ValueError(f"'byte_data' should be equal to BYTES_PER_IMAGE -> {byte_data} != {BYTES_PER_IMAGE}")
    img = Image.frombytes('1', (WIDTH, HEIGHT), byte_data)
    if RESIZE_TIMES:
        img = img.resize((WIDTH * RESIZE_TIMES, HEIGHT * RESIZE_TIMES))
    img.save(os.path.join(save_dir, f"{img_name}.png"), format="png")


def create_bytes_from_picture(picture_path, threshold=128):
    image_file = Image.open(os.path.normpath(picture_path))
    # Grayscale
    image_file = image_file.convert("L")
    # Threshold (avoid read mistakes on image compression), 128 is mid-gray pixel
    image_file = image_file.point(lambda p: 255 if p > threshold else 0)
    # To mono (1 bit per pixel image)
    image_file = image_file.convert('1')
    if RESIZE_TIMES:
        width, height = image_file.size
        image_file = image_file.resize((int(width / RESIZE_TIMES), int(height / RESIZE_TIMES)))
    # Convert pixels to bytes
    image_file = image_file.tobytes()
    return image_file


def generate_random_file_name(size=12):
    return f"output_{''.join(random.choice(string.ascii_letters) for _ in range(size))}"


def generate_unique_file_name(size=12):
    file_name = generate_random_file_name(size)
    while os.path.exists(file_name):
        file_name = generate_random_file_name(size)
    return file_name


def convert_file_to_video(file_path_to_conv, output_path, temp_dir):
    file_data, data_len = get_bytes_from_file(file_path_to_conv)
    file_data_chunk_generator = (file_data[x:x + BYTES_PER_IMAGE] for x in range(0, data_len, BYTES_PER_IMAGE))
    for index, chunk in enumerate(file_data_chunk_generator):  # enumerate is lazy, so it's ok to use it with generator
        create_picture_from_bytes(chunk, temp_dir, index)
    create_video_from_images(temp_dir, output_path)


def convert_video_to_file(video_path_to_conv, output_path, temp_dir):
    create_images_from_video(video_path_to_conv, temp_dir)
    image_names = get_sorted_filenames_list(temp_dir)
    with open(f"{output_path}.zip", "ab") as archive:
        for image_name in image_names:
            data_chunk = create_bytes_from_picture(os.path.join(temp_dir, image_name))
            archive.write(data_chunk)


def main(delete_temp_dir=True):
    while True:
        convert_option = input("Choose an option:\n1. FILE -> VIDEO\n"
                               "2. VIDEO -> FILE\nYour choice: ")
        # input validation
        if convert_option not in ("1", "2"):
            continue
        # FILE -> VIDEO
        if convert_option == "1":
            try:
                TEMP_PATH = create_temp_dir()
                path_file_to_convert = input("Input path of the file you want to convert: ")
                print("\nIn progress. Please wait...")
                output_file_name = generate_unique_file_name()
                convert_file_to_video(path_file_to_convert, output_file_name, TEMP_PATH)
                print(f"\nCreated file: {output_file_name}")
            finally:
                if os.path.exists(TEMP_PATH) and delete_temp_dir:
                    rmtree(TEMP_PATH)
        # VIDEO -> FILE
        if convert_option == "2":
            try:
                TEMP_PATH = create_temp_dir()
                path_file_to_convert = input("Input path of the video you want to convert: ")
                print("\nIn progress. Please wait...")
                output_file_name = generate_unique_file_name()
                convert_video_to_file(path_file_to_convert, output_file_name, TEMP_PATH)
                print(f"\nCreated file: {output_file_name}")
            finally:
                if os.path.exists(TEMP_PATH) and delete_temp_dir:
                    rmtree(TEMP_PATH)
        break


if __name__ == "__main__":
    main()
