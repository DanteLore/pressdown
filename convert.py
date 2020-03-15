import re

from bs4 import BeautifulSoup
from datetime import datetime


def get(root, element):
    return root.find(element).string.strip()


# Need to use "xml" not "lxml" here (as suggested by most tutorials) because lxml can't handle CDATA's
soup = BeautifulSoup(open("blog.xml"), features="xml")

items = soup.find_all('item')


def convert_content(c):
    c = re.sub(r'<!-- /?wp:paragraph -->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:heading.*-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:image.*-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<h1>(.*)</h1>', r'#\g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h2>(.*)</h2>', r'##\g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h3>(.*)</h3>', r'###\g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h4>(.*)</h4>', r'####\g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'</?p[^>]*>', '', c, flags=re.MULTILINE)
    c = re.sub(r'</?div[^>]*>', '', c, flags=re.MULTILINE)
    c = re.sub(r'</?figure[^>]*>', '', c, flags=re.MULTILINE)
    c = re.sub(r'<figcaption>.*</figcaption>', '', c, flags=re.MULTILINE)
    c = re.sub(r'<img.*src="([^\"]*)"[^>]*/>', '![](\g<1>)', c, flags=re.MULTILINE)
    c = re.sub(r'<em>(.*)</em>', '*\g<1>*', c, flags=re.MULTILINE) # <-- probably way better to do this with beautiful soup, as the regexes are unsubtle
    c = re.sub(r'\n\n', r'\n', c, flags=re.MULTILINE)
    return c


def write_post(item):
    title = get(item, 'title')
    published = datetime.strptime(get(item, 'post_date'), '%Y-%m-%d %H:%M:%S').isoformat()
    status = get(item, 'status')
    filename = 'output/{0}.md'.format(get(item, 'post_name'))
    content = convert_content(get(item, 'content:encoded'))
    print("\n\nCONVERTING POST: {0}\n\nFilename: {1}\nPost Date: {2}\nStatus: {3}".format(title, filename, published, status))

    with open(filename, 'w') as f:
        f.write("\n---\ntitle: {0}\ndate: {1}\ndraft: {2}\n---\n\n".format(title, published, status != 'publish'))
        f.write(content)


if __name__ == "__main__":

    for item in items:
        t = get(item, "post_type")

        if t == "post":
            write_post(item)
