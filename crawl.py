import re
import urllib
import Queue
import threading

def parse_url():
    while True:
        url = urls.get(True)
        try:
            src = urllib.urlopen(url).read()

            links = re.findall(r"<a [^>]*href=\"([^\"]+)\"[^>]*>", src, re.M)

            src = src.decode("utf-8")
            words = re.findall(r"(["+cyr_chars+"]+)", src, re.M)
            for w in words:
                cyr_words.put(w)

            if len(cyr_words) > 0:
                for l in links:
                    if l.startswith("http://"):
                        urls.put(l)

            print "words %d , links %d" % (len(cyr_words), urls.qsize())
        except:
            pass

        urls.task_done()

def write_words():
    while True:
        w = cyr_words.get(True)
        out.write(w + "\n")

char_file = open("mn_chars.txt")
cyr_chars = char_file.read().strip().decode("utf-8")
char_file.close()
cyr_words = Queue.Queue()
urls = Queue.Queue()
urls.put("http://www.gogo.mn")

workers = list()
for i in range(100):
    worker = threading.Thread(target = parse_url)
    worker.setDaemon(True)
    worker.start()
    workers.append(worker)

out = open("./output.txt", "w")
writer = threading.Thread(target = write_words)
writer.setDaemon(True)
writer.start()

urls.join()
out.close()
