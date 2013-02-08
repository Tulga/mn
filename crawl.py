import re
import urllib
import Queue

cyr_chars = open("mn_chars.txt").read().strip().decode("utf-8")

urls = Queue.Queue()
urls.put("http://www.gogo.mn")

while urls.empty() == False:
    url = urls.get()
    try:
        src = urllib.urlopen(url).read()

        links = re.findall(r"<a [^>]*href=\"([^\"]+)\"[^>]*>", src, re.M)

        src = src.decode("utf-8")
        cyr_words = re.findall(r"(["+cyr_chars+"]+)", src, re.M)
        for w in cyr_words:
            print w

        if len(cyr_words) > 0:
            for l in links:
                if l.startswith("http://"):
                    urls.put(l)

    except:
        pass
