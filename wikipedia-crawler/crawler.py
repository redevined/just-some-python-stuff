#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import httplib2, re
from bs4 import BeautifulSoup
from various import debug, CharSequence


class Status() :
	OK = 0
	NOLINK = 1
	LOOP = 2
	URLERR = 3
	HTTPERR = 4
	UNKNOWN = 5
	
	def __call__(self, index) :
		return self.getMsg(index)
	
	def getMsg(self, index) :
		return {
			0 : "'Philosophy' distance to the article '{titles[0]}' is {distance}",
			1 : "Article 'Philosophy' is not reachable from {titles[0]}, because {last_title} has no links",
			2 : "Path contains a loop, therefore 'Philosophy' is not reachable from '{titles[0]}'",
			3 : "URL error on page '{last_title}'",
			4 : "HTTP error, please check your connection settings",
			5 : "Unknown error, site trace: {titles}"
		}[index]


# Do some link finding magic
def findValidLink(lines, host = "http://de.wikipedia.org") :
	for line in lines :
		# Save links of all <a>-tags
		hrefs = [tag["href"] for tag in line("a")]
		
		# Replace all Brackets with <bracket>-tags
		line = BeautifulSoup(
			str(line).replace("[", "(").replace("]", ")").replace("(", "<bracket>").replace(")", "</bracket>")
		)
		
		# Restore links, in case they're broken through the last step
		for tag, href in zip(line("a"), hrefs) :
			tag["href"] = href
		
		# Remove all <decompose>-tags
		for name in ["bracket", "i", "b", "sub", "sup"] :
			for tag in line(name) :
				tag.decompose()
		for tag in line(style = re.compile("display:\s?none")) + line(class_ = ["geo", "coordinates", "microformat"]) :
			tag.decompose()
		
		# Return first still existing link
		for tag in line("a") :
			if tag.text :
				return host + tag["href"]


def crawl(url, titles, key, http) :
	try :
		response, content = http.request(url)
		source = BeautifulSoup(content)
	except Exception :
		code = Status.HTTPERR
	else :
		try :
			h1 = source.body.find("h1", id = "firstHeading")
			title = h1.text if h1 else str()
			titles.append(title)
			content = source.body.find("div", id = "mw-content-text")
			lines = content(["p", "ol", "ul"], recursive = False)
			
			if not title :
				code = Status.URLERR
			elif title == key :
				code = Status.OK
			elif title in titles[:-1] :
				code = Status.LOOP
			else :
				link = findValidLink(lines)
				if link :
					return crawl(link, titles, key, http)
				else :
					code = Status.NOLINK
		except Exception as e :
			code = Status.UNKNOWN
	return code, titles


def main(url = "http://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite", http_proxy = None, http_proxy_port = 80, verbose = False) :
	if http_proxy :
		http = httplib2.Http(proxy_info = httplib2.ProxyInfo(3, http_proxy, http_proxy_port))
	else :
		http = httplib2.Http()
	
	statusMsg = Status()
	res = { st : [] for st in range(6) }
	for i in range(1000) :
		status, visited = crawl(url, [], "Philosophie", http)
		visited = [s.encode("ascii", "ignore") for s in visited]
		if verbose :
			print "\n  -> ".join(visited)
			print statusMsg(status).format(titles = visited, last_title = visited[-1], distance = len(visited))
			print
		res[status].append(len(visited))
		if res[Status.OK] :
			rel = len(res[Status.OK]) / sum(len(res[st]) for st in range(3)) * 100
			avg = sum(res[Status.OK]) / len(res[Status.OK])
			print "=> {0:.6}% of {1} articles lead to the article 'Philosophy' in an average of {2:.4} steps".format(rel, i + 1, avg)
	print "Statistics:\n  OK: {0[0]}\n  NOLINK: {0[1]}\n  LOOP: {0[2]}\n  URLERR: {0[3]}\n  HTTPERR: {0[4]}\n  UNKNOWN: {0[5]}".format({key : len(val) for key, val in res.items()})
	print res[Status.UNKNOWN]
		

if __name__ == "__main__" :
	main()