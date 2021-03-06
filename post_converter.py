import re


class PostConverter:
    def __init__(self, content):
        self.content = content

    def strip_excessive_newlines(self):
        c = self.content
        c = re.sub(r'\n\n\n', r'\n', c, flags=re.MULTILINE)
        c = re.sub(r'>\n#', r'>\n\n#', c, flags=re.MULTILINE)
        return PostConverter(c)

    def convert_code_blocks(self):
        c = self.content
        c = re.sub(r'<code.*?>(.*?)</code>', r'```\g<1>```', c)  # Inline code block
        c = re.sub(r'<code.*?>([\S\s]*?)</code>', r'\n```\n\g<1>\n```\n', c,
                   flags=re.MULTILINE)  # Multi-line code block
        c = re.sub(r'<pre>([\S\s]*?)</pre>', r'\n```\n\g<1>\n```\n', c, flags=re.MULTILINE)  # Simple preformatted block
        c = re.sub(r'<pre.*?wp-block.*?>([\S\s]*?)</pre>', r'\g<1>', c,
                   flags=re.MULTILINE)  # Extra wordpress pre in clode blocks
        c = re.sub(
            r'<!-- wp:syntaxhighlighter/code {"language":"(.*?)"} -->\n?([\S\s]*?)\n?<!-- /wp:syntaxhighlighter/code -->',
            r'\n```\g<1>\n\g<2>\n```\n', c, flags=re.MULTILINE)
        c = re.sub(r'\[sourcecode lang[^=]*?="(.*?)"\]\n?([\S\s]*?)\[/sourcecode\]',
                   r'\n```\g<1>\n\g<2>\n```\n', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- wp:syntaxhighlighter/code -->\n?([\S\s]*?)\n?<!-- /wp:syntaxhighlighter/code -->',
                   r'```\n\g<1>\n```', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- wp:preformatted -->([\S\s]*?)<!-- /wp:preformatted -->',
                   r'```\n\g<1>\n```', c, flags=re.MULTILINE)
        c = re.sub(r'```jscript', r'```javascript', c)
        return PostConverter(c)

    def clean_hyperlinks(self):
        c = self.content
        c = re.sub(r'<a.*href="(.*?)".*?>(.*?)</a>', r'<a href="\g<1>">\g<2></a>', c, flags=re.MULTILINE)
        return PostConverter(c)

    def convert_youtube(self):
        c = self.content
        c = re.sub(
            r'<!-- wp:core-embed/youtube.*?-->[\S\s]*?https://youtu.be/([^\s]*)[\S\s]*?<!-- /wp:core-embed/youtube -->',
            r'\n{{< youtube \g<1> >}}\n', c, flags=re.MULTILINE)
        return PostConverter(c)

    def convert_html_elements(self):
        c = self.content
        c = re.sub(r'<h1>(.*?)</h1>', r'# \g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'<h2>(.*?)</h2>', r'## \g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'<h3>(.*?)</h3>', r'### \g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'<h4>(.*?)</h4>', r'#### \g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'</?p>', '', c, flags=re.MULTILINE)
        c = re.sub(r'</?p .*?>', '', c, flags=re.MULTILINE)
        c = re.sub(r'</?div.*?>', '', c, flags=re.MULTILINE)
        c = re.sub(r'<br.*?>', '\n', c, flags=re.MULTILINE)
        c = re.sub(r'<em>(.*?)</em>', '*\g<1>*', c, flags=re.MULTILINE)
        c = re.sub(r'<strong>(.*?)</strong>', '**\g<1>**', c, flags=re.MULTILINE)
        c = re.sub(r'<b>(.*?)</b>', '**\g<1>**', c, flags=re.MULTILINE)
        c = re.sub(r'<del>(.*?)</del>', '~~\g<1>~~', c, flags=re.MULTILINE)
        c = re.sub(r'</?figure.*?>', '', c, flags=re.MULTILINE)
        c = re.sub(r'<figcaption>.*?</figcaption>', '', c, flags=re.MULTILINE)
        c = re.sub(r'<hr.*?>', '\n---\n', c, flags=re.MULTILINE)
        return PostConverter(c)

    def convert_images_and_galleries(self):
        c = self.content
        c = re.sub(r'<!-- /?wp:gallery.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<ul.*?wp-block-gallery.*?>(.*?)</ul.*?>', '\g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'<ul.*?blocks-gallery-grid.*?>(.*?)</ul.*?>', '\g<1>', c, flags=re.MULTILINE)
        c = re.sub(r'<li.*?blocks-gallery-item.*?>.*?<img.*?src="([^\"]*)".*?/>.*?</li>',
                   r'<GALLERY_IMAGE_HOP class="gallery" src="\g<1>"/>', c, flags=re.MULTILINE)
        c = re.sub(r'<img.*?src="([^\"]*)".*?/>', '<img src="\g<1>"/>', c, flags=re.MULTILINE)
        c = re.sub(r'<GALLERY_IMAGE_HOP(.*?)/>', '<img\g<1>/>', c, flags=re.MULTILINE)
        return PostConverter(c)

    def convert_wordpress_tags(self):
        c = self.content
        c = c.replace('&nbsp;', ' ')
        c = c.replace('&quot;', '"')
        c = c.replace('&gt;', '>')
        c = c.replace('&lt;', '<')
        c = re.sub(r'<!-- /?wp:paragraph.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:heading.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:image.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:code.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:list.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:separator.*?-->', '', c, flags=re.MULTILINE)
        c = re.sub(r'<!-- /?wp:quote.*?-->', '', c, flags=re.MULTILINE)
        return PostConverter(c)

    def to_string(self):
        return self.content