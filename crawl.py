import re
import urllib
import Queue
import threading

def parse_url():
    while True:
        url = urls.get()
        try:
            src = urllib.urlopen(url).read()

            links = re.findall(r"<a [^>]*href=\"([^\"]+)\"[^>]*>", src, re.M)

            src = src.decode("utf-8")
            cyr_words.extend(re.findall(r"(["+cyr_chars+"]+)", src, re.M))

            if len(cyr_words) > 0:
                for l in links:
                    if l.startswith("http://"):
                        urls.put(l)

            print "words %d , links %d" % (len(cyr_words), urls.qsize())
        except:
            pass

        urls.task_done()

cyr_chars = open("mn_chars.txt").read().strip().decode("utf-8")
cyr_words = list()
urls = Queue.Queue()
urls.put("http://www.gogo.mn")

workers = list()
for i in range(10):
    worker = threading.Thread(target = parse_url)
    worker.setDaemon(True)
    worker.start()
    workers.append(worker)

urls.join()
