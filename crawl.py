import re
import urllib

cyr_chars = open("mn_chars.txt").read().strip().decode("utf-8")

url = "http://www.gogo.mn"
src = urllib.urlopen(url).read()

links = re.findall(r"<a [^>]*href=\"([^\"]+)\"[^>]*>", src, re.M)
for l in links:
    print l

src = src.decode("utf-8")
cyr_words = re.findall(r"(["+cyr_chars+"]+)", src, re.M)
for w in cyr_words:
    print w
