import urllib2
from xml.dom import minidom
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'IE')]
urllib2.install_opener(opener)
adr = 'http://en.wiktionary.org/wiki/Category:English_uncountable_nouns'
f = urllib2.urlopen(adr)
t = f.read()
f.close()

def getData(link):
	f = urllib2.urlopen(link)
	t = f.read()
	f.close()
	return t

def getNextLink(data):
	pref = 'http://en.wiktionary.org'
	dom = minidom.parseString(data)
	aas = dom.getElementsByTagName('a')
	for a in aas:
		c = a.firstChild
		if (not c) or (not (c.nodeName == '#text')):
			continue
		text = c.data
		if text == u'next 200':
			#print text, '\t', a.getAttribute('href')
			return pref + a.getAttribute('href')

		
def getWords(data):
	ws = []
	dom = minidom.parseString(data)
	ts = dom.getElementsByTagName('td')
	for tb in ts:
		if tb.getAttribute('width') == "33.3%":
			aas = tb.getElementsByTagName('a')
			for a in aas:
				ws.append(a.firstChild.nodeValue)
	return ws

def pageProc(firstLink):
	words = []
	next = firstLink
	while next:
		data = getData(next)
		words = words + getWords(data)
		next = getNextLink(data)
		#print next
	return words

ws = pageProc(adr)
print len(ws)