#
# Author Sainbayar S.
#

import sys
import Queue
import urllib2

def getTokens(src):
    tokens = list()
    ind = 0
    while ind < len(src):
        li = src.find("<", ind)
        if src[ind] in {" ", "\n", "\t", "\r"}:
            ind += 1            
        elif li == -1:            
            tokens.append(src[ind:len(src)].strip())
            ind = len(src)
        elif ind < li:
            tokens.append(src[ind:li].strip())
            ind = li
        else:       
            ri = src.find(">", li)
            assert ri != -1
            tokens.append(src[ind:ri+1].strip())
            ind = ri+1

    return tokens


class Node:
    def __init__(self):
        self.child_nodes = list()
        self.value = None
        self.type = None

# will not use (bugs)
def parse(tokens, ind, depth):
    n = Node()
    t = tokens[ind]

    if t[0] != "<":
        n.value = t
        n.type = "txt"
    elif t.startswith("<!"):
        n.value = t
        n.type = "!"
    elif t.startswith("<meta"):
        n.value = t
        n.type = "meta"
    elif t.startswith("<link"):
        n.value = t
        n.type = "link"
    elif t[-2:] == "/>":
        e = t[1:-2].split()
        n.type = e[0]
    else:
        e = t[1:-1].split()
        n.type = e[0]
        print (" " * depth) + n.type
        ind += 1
        while tokens[ind][0:2] != "</":
            (child, ind) = parse(tokens, ind, depth+1)
            n.child_nodes.append(child)

        type2 = tokens[ind][2:-1].strip()
        if n.type != type2:
            print n.type + " <> " + type2
            assert False

    print (" " * depth) + n.type
    return n, ind+1                    

def getLinks(tokens):
    links = list()
    for t in tokens:
        if t.startswith("<a") == False:
            continue
        si = t.find("href=\"")
        if si == -1:
            si = t.find("href='")
        if si == -1:
            continue
        si += len("href='")
        ei = t.find("\"",si)
        if ei == -1:
            ei = t.find("'",si)
        if ei == -1:
            continue
        l = t[si:ei]
        if l.startswith("http://") == False:
            continue
        links.append(l)
            
    return links

assert len(sys.argv) == 2
links = Queue.Queue()
links.put(sys.argv[1])
while links.empty() == False:
    try:
        c = urllib2.urlopen(links.get())
        content = c.read()
        tokens = getTokens(content)
        ls = getLinks(tokens)
        for l in ls:
            print l
            links.put(l)
    except urllib2.URLError as e:
        pass
