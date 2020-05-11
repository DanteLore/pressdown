import argparse
import os
import shutil
from glob import glob
from datetime import datetime

template = """
---
title: "{title}"

date: "{post_date}"

featured_image: "{featured_image}"
---

Happy typing!

{body}

"""


def post_from_pics(input_glob, title="New Post", post_date=None):
    files = glob(input_glob)
    files.sort()

    if not post_date:
        post_date = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")

    post_name = title.lower().replace(' ', '-')
    post_file = "hugo/content/posts/{0}.md".format(post_name)

    images_base_url = '/images/{0}/'.format(post_name)
    filenames = [f.split('/')[-1] for f in files]

    urls = [images_base_url + f for f in filenames]
    tags = ['<img src="{0}"/>'.format(u) for u in urls]
    body = "\n\n".join(tags)
    featured_image = urls[0]

    copy_images_to_content(files, post_name)
    post = template.format(body=body, post_date=post_date, title=title, featured_image=featured_image)

    with open(post_file, 'w') as f:
        f.write(post)


def copy_images_to_content(files, post_name):
    images_dir = 'hugo/static/images/{0}/'.format(post_name)

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for src in files:
        dest = images_dir + src.split('/')[-1]
        print("Copying {0} to {1}".format(src, dest))
        shutil.copy(src, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a template hugo post from a directory of images')
    parser.add_argument('--input', default="*.jpg", help='A glob for the input files')
    parser.add_argument('--title', default="New Post", help='The title of the post')
    parser.add_argument('--date', default=None, help='Publication date (default = now)')
    args = parser.parse_args()

    post_from_pics(
        input_glob=args.input,
        title=args.title,
        post_date=args.date
    )
