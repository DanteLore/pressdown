import os
from datetime import datetime

from bs4 import BeautifulSoup

from image_helper import ImageHelper
from post_converter import PostConverter


def get(root, element):
    return root.find(element).string.strip()


class PressDown:
    def __init__(self, source_file="blog.xml"):
        # Need to use "xml" not "lxml" here (as suggested by most tutorials) because lxml can't handle CDATA's
        self.soup = BeautifulSoup(open(source_file), features="xml")

    def convert(self):
        for i in self.soup.find_all('item'):
            if get(i, "post_type") == "post":
                self.write_post(i)

    @staticmethod
    def write_header(f, first_image, published, title):
        f.write('\n---\n')
        f.write('title: "{0}"\n\n'.format(title))
        f.write('date: "{0}"\n\n'.format(published))
        f.write('featured_image: "{0}"'.format(first_image))
        f.write('\n---\n\n\n')

    def write_post(self, item):
        posts_dir = 'content/posts'
        filename = '{0}/{1}.md'.format(posts_dir, get(item, 'post_name'))

        img = ImageHelper(
            images_dir='static/images/{0}'.format(get(item, 'post_name')),
            images_url_root='/images/{0}'.format(get(item, 'post_name'))
        )

        if not os.path.exists(posts_dir):
            os.makedirs(posts_dir)

        title = get(item, 'title')
        published = datetime.strptime(get(item, 'post_date'), '%Y-%m-%d %H:%M:%S').isoformat()
        status = get(item, 'status')

        content = PostConverter(get(item, 'content:encoded')) \
            .convert_wordpress_tags() \
            .convert_images_and_galleries() \
            .convert_html_elements() \
            .convert_youtube() \
            .clean_hyperlinks() \
            .convert_code_blocks() \
            .strip_excessive_newlines() \
            .to_string()

        first_image = img.find_first_image(content)

        for url in img.find_all_images(content):
            image_url = img.convert_image(url)
            content = content.replace(url, image_url)

        print("\n\nCONVERTING: {0}\n\nFilename: {1}\nDate: {2}\nStatus: {3}".format(title, filename, published, status))

        with open(filename, 'w') as f:
            self.write_header(f, first_image, published, title)
            f.write(content)