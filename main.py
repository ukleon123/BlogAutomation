import os

from controller import Controller

if __name__ == "__main__":
    controller = Controller()

    working_dir = os.path.join(os.getcwd(), 'images')
    foreground_file_path = os.path.join(working_dir, 'foreground')
    controller.get_response()
    controller.get_images(foreground_file_path)
    controller.init_blog()
    controller.write_blog()
