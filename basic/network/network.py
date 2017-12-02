import urllib.request as req

def get_html(url):
    page = req.urlopen(url)
    html = page.read("utf-8")
    print(html.decode("utf-8"))


get_html("http://blog.csdn.net/")