import sys
import bs4
import json
import rfeed

BeautifulSoup = lambda data: bs4.BeautifulSoup(data, features="lxml")


def append_p(p):
    n = p.find_next("p")
    if n is not None and n.find_previous("h3") == p.find_previous("h3"):
        return f"{str(p)}{append_p(n)}"
    else:
        return str(p)


with open(sys.argv[1]) as md_f:
    soup = BeautifulSoup(md_f.read())

    feed = rfeed.Feed(
        title="Morning Mail",
        description=soup.find("h1").find_next("p").get_text(),
        language="en-US",
        items=[
            rfeed.Item(
                title=p.find_previous("h3").get_text(),
                link=p.find_previous("h3").find("a").get("href"),
                description=append_p(p),
                author=p.find_previous("h2").get_text(),
                guid=rfeed.Guid(p.find_previous("h3").find("a").get("href")),
            )
            for p in soup.find_all("p")
            if p.find_previous("h3") is not None
            and p.find_previous("p").find_previous("h3") != p.find_previous("h3")
        ],
        link="https://morningmail.rpi.edu/",
    )

    print(feed.rss())
