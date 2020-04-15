import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from post_converter import PostConverter


def get(root, element):
    return root.find(element).string.strip()


def find_first_image(content):
    images = find_all_images(content)
    return images[0] if images else ""


image_pattern = re.compile(r'src="([^\"<>]*?(.png|.jpg|.jpeg|.gif))"', re.IGNORECASE)


def find_all_images(content):
    images = [name for (name, extension) in re.findall(image_pattern, content)]
    return images


def write_header(f, first_image, published, title):
    f.write('\n---\n')
    f.write('title: "{0}"\n\n'.format(title))
    f.write('date: "{0}"\n\n'.format(published))
    f.write('featured_image: "{0}"'.format(first_image))
    f.write('\n---\n\n\n')


def write_post(item):
    posts_dir = 'content/posts'
    images_url_root = '/images/{0}'.format(get(item, 'post_name'))
    images_dir = 'static/images/{0}'.format(get(item, 'post_name'))
    filename = '{0}/{1}.md'.format(posts_dir, get(item, 'post_name'))

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

    first_image = find_first_image(content)

    images = find_all_images(content)
    for url in images:
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        fn = url.split('/')[-1]
        image_url = "{0}/{1}".format(images_url_root, fn)
        image_file = "{0}/{1}".format(images_dir, fn)

        if not os.path.exists(image_file):
            print("Downloading {0}\nto {1}\nUrl {2}".format(url, image_file, image_url))
            download_image(image_file, url)
        else:
            print("{0} already downloaded".format(image_file))

        content = content.replace(url, image_url)

    print("\n\nCONVERTING POST: {0}\n\nFilename: {1}\nPost Date: {2}\nStatus: {3}".format(title, filename, published,
                                                                                          status))

    with open(filename, 'w') as f:
        write_header(f, first_image, published, title)
        f.write(content)


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


def check_hugo_dir():
    if not os.path.exists('hugo'):
        os.makedirs('hugo')


def convert_blog():
    # Need to use "xml" not "lxml" here (as suggested by most tutorials) because lxml can't handle CDATA's
    soup = BeautifulSoup(open("blog.xml"), features="xml")
    items = soup.find_all('item')

    check_hugo_dir()

    pwd = os.getcwd()
    os.chdir('hugo')
    try:
        for i in items:
            if get(i, "post_type") == "post":
                write_post(i)
    finally:
        os.chdir(pwd)


if __name__ == "__main__":
    convert_blog()
