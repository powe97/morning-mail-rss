import sys
import bs4
import json
import rfeed
import datetime

BeautifulSoup = lambda data: bs4.BeautifulSoup(data, features="lxml")


def append_p(p):
    n = p.find_next("p")
    if n is not None and n.find_previous("h3") == p.find_previous("h3"):
        return f"{str(p)}{append_p(n)}"
    else:
        return str(p)


now = datetime.datetime.now()


with open(sys.argv[1]) as md_f:
    soup = BeautifulSoup(md_f.read())

    # remove tracking image
    soup.find_all("img")[-1].parent.clear()

    feed = rfeed.Feed(
        title="Morning Mail",
        description=soup.find("h1").find_next("p").get_text(),
        language="en-US",
        items=[
            rfeed.Item(
                title=p.find_previous("h3").get_text(),
                link=p.find_previous("h3").find("a").get("href"),
                description=append_p(p),
                guid=rfeed.Guid(p.find_previous("h3").find("a").get("href")),
                pubDate=now,
                author=p.find_previous("h2").get_text(),
            )
            for p in soup.find_all("p")
            if p.find_previous("h3") is not None
            and p.find_previous("p").find_previous("h3") != p.find_previous("h3")
        ],
        link="https://morningmail.rpi.edu/",
        lastBuildDate=now,
    )

    print(feed.rss())
