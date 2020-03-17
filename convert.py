import re

from bs4 import BeautifulSoup
from datetime import datetime


def get(root, element):
    return root.find(element).string.strip()


# Need to use "xml" not "lxml" here (as suggested by most tutorials) because lxml can't handle CDATA's
soup = BeautifulSoup(open("blog.xml"), features="xml")

items = soup.find_all('item')


def convert_content(c):
    # Wordpress tags
    c = c.replace('&nbsp;', ' ')
    c = c.replace('&quot;', '"')
    c = c.replace('&gt;', '>')
    c = c.replace('&lt;', '<')
    c = re.sub(r'<!-- /?wp:paragraph.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:heading.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:image.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:code.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:gallery.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:list.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:separator.*?-->', '', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- /?wp:quote.*?-->', '', c, flags=re.MULTILINE)

    # HTML elements
    c = re.sub(r'<h1>(.*?)</h1>', r'# \g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h2>(.*?)</h2>', r'## \g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h3>(.*?)</h3>', r'### \g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<h4>(.*?)</h4>', r'#### \g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'</?p>', '', c, flags=re.MULTILINE)
    c = re.sub(r'</?p .*?>', '', c, flags=re.MULTILINE)
    c = re.sub(r'</?div.*?>', '', c, flags=re.MULTILINE)
    c = re.sub(r'<br.*?>', '\n', c, flags=re.MULTILINE)
    c = re.sub(r'<ul.*?>(.*?)</ul>', '\g<1>', c, flags=re.MULTILINE)
    c = re.sub(r'<li.*?>(.*?)</li>', '* \g<1>\n', c, flags=re.MULTILINE)
    c = re.sub(r'<em>(.*?)</em>', '*\g<1>*', c, flags=re.MULTILINE)
    c = re.sub(r'<strong>(.*?)</strong>', '**\g<1>**', c, flags=re.MULTILINE)
    c = re.sub(r'<b>(.*?)</b>', '**\g<1>**', c, flags=re.MULTILINE)
    c = re.sub(r'<del>(.*?)</del>', '~~\g<1>~~', c, flags=re.MULTILINE)
    c = re.sub(r'</?figure.*?>', '', c, flags=re.MULTILINE)
    c = re.sub(r'<figcaption>.*?</figcaption>', '', c, flags=re.MULTILINE)
    c = re.sub(r'<hr.*?>', '\n---\n', c, flags=re.MULTILINE)

    #YouTube
    c = re.sub(r'<!-- wp:core-embed/youtube.*?-->[\S\s]*?https://youtu.be/([^\s]*)[\S\s]*?<!-- /wp:core-embed/youtube -->',
               r'\n{{< youtube \g<1> >}}\n', c, flags=re.MULTILINE)

    # Images and galleries
    c = re.sub(r'<li class="blocks-gallery-item">.*?<img.*?src="([^\"]*)".*?/>.*?</li>',
               r'<img src="\g<1>" class="gallery"/>', c, flags=re.MULTILINE)
    c = re.sub(r'<img.*?src="([^\"]*)".*?/>', '<img src="\g<1>"/>', c, flags=re.MULTILINE)

    # Clean up hyperlinks
    c = re.sub(r'<a.*href="(.*?)".*?>(.*?)</a>', r'<a href="\g<1>">\g<2></a>', c, flags=re.MULTILINE)

    # Code blocks
    c = re.sub(r'<code.*?>(.*?)</code>', r'```\g<1>```', c) # Inline code block
    c = re.sub(r'<code.*?>([\S\s]*?)</code>', r'\n```\n\g<1>\n```\n', c, flags=re.MULTILINE) # Multi-line code block
    c = re.sub(r'<pre.*?>([\S\s]*?)</pre>', r'\n```\n\g<1>\n```\n', c, flags=re.MULTILINE) # Preformatted
    c = re.sub(r'<!-- wp:syntaxhighlighter/code {"language":"(.*?)"} -->\n?([\S\s]*?)\n?<!-- /wp:syntaxhighlighter/code -->',
               r'\n```\g<1>\n\g<2>\n```\n', c, flags=re.MULTILINE)
    c = re.sub(r'\[sourcecode lang[^=]*?="(.*?)"\]\n?([\S\s]*?)\[/sourcecode\]',
               r'\n```\g<1>\n\g<2>\n```\n', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- wp:syntaxhighlighter/code -->\n?([\S\s]*?)\n?<!-- /wp:syntaxhighlighter/code -->',
               r'```\n\g<1>\n```', c, flags=re.MULTILINE)
    c = re.sub(r'<!-- wp:preformatted -->([\S\s]*?)<!-- /wp:preformatted -->',
               r'```\n\g<1>\n```', c, flags=re.MULTILINE)
    c = re.sub(r'```jscript', r'```javascript', c)

    # Excessive newlines
    c = re.sub(r'\n\n\n', r'\n', c, flags=re.MULTILINE)
    return c


def find_first_image(content):
    images = [name for (name, extension) in re.findall(r'(http://[^\"<>]*?(.png|.jpg))', content)]
    return images[0] if images else ""


def write_post(item):
    title = get(item, 'title')
    published = datetime.strptime(get(item, 'post_date'), '%Y-%m-%d %H:%M:%S').isoformat()
    status = get(item, 'status')
    filename = 'output/{0}.md'.format(get(item, 'post_name'))
    content = convert_content(get(item, 'content:encoded'))

    first_image = find_first_image(content)

    print("\n\nCONVERTING POST: {0}\n\nFilename: {1}\nPost Date: {2}\nStatus: {3}".format(title, filename, published, status))

    with open(filename, 'w') as f:
        f.write('\n---\n')
        f.write('title: "{0}"\n\n'.format(title))
        f.write('date: "{0}"\n\n'.format(published))
        f.write('featured_image = "{0}"'.format(first_image))
        f.write('\n---\n\n\n')
        f.write(content)


if __name__ == "__main__":

    for item in items:
        t = get(item, "post_type")

        if t == "post":
            write_post(item)
