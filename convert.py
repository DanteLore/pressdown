import os

from press_down import PressDown


def check_output_dir():
    if not os.path.exists('hugo'):
        os.makedirs('hugo')


def convert_blog():
    check_output_dir()

    pwd = os.getcwd()
    os.chdir('hugo')
    try:
        PressDown("{0}/blog.xml".format(pwd)).convert()
    finally:
        os.chdir(pwd)


if __name__ == "__main__":
    convert_blog()
