from bs4 import BeautifulSoup

soup = BeautifulSoup (open("blog.xml"), features="lxml")


items = soup.find_all('item')
for item in items:
    title = item.find_all('title')[0].contents
    print(title)
