import os
import re
import requests


class ImageHelper:
    def __init__(self, images_dir, images_url_root):
        self.images_url_root = images_url_root
        self.images_dir = images_dir
        self.image_pattern = re.compile(r'src="([^\"<>]*?(.png|.jpg|.jpeg|.gif))"', re.IGNORECASE)

    def find_all_images(self, content):
        images = [name for (name, extension) in re.findall(self.image_pattern, content)]
        return images

    def find_first_image(self, content):
        images = self.find_all_images(content)
        return images[0] if images else ""

    def convert_image(self, original_url):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        fn = original_url.split('/')[-1]
        image_url = "{0}/{1}".format(self.images_url_root, fn)
        image_file = "{0}/{1}".format(self.images_dir, fn)
        if not os.path.exists(image_file):
            print("Downloading {0}\nto {1}\nUrl {2}".format(original_url, image_file, image_url))
            self.download_image(image_file, original_url)
        else:
            print("{0} already downloaded".format(image_file))
        return image_url

    @staticmethod
    def download_image(image_file, url):
        r = requests.get(url, stream=True, headers={"User-Agent": "Dante Crazy Browse 2.6"})
        if r.status_code == 200:
            with open(image_file, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

            return True
        else:
            print("ERROR {0}".format(r.status_code))
            return False
