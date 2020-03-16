# Press Down

Convert Wordpress blogs to Markdown for import into more modern platforms like Hugo.

## Usage

Export your Wordpress site to an XML file, move it to `blog.xml` in the same directory as `convert.py`.

```sh
pip3 -r requirements.txt
python3 convert.py
```

Your markdown files are waiting for you in the `output` folder.