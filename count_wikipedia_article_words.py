from lxml import etree
import re
import csv
import sys

class WordCounter:

    namespace = '{http://www.mediawiki.org/xml/export-0.8/}'
    ns = namespace + 'ns'
    page = namespace + 'page'
    title = namespace + 'title'
    text = namespace + 'text'
    redirect = namespace + 'redirect'
    
    def __init__(self, csvfile):
        self.in_page = False
        self.in_ns = False
        self.in_title = False
        self.title = ""
        self.in_article = False
        self.in_text = False
        self.in_redirect = False
        self.words = 0
        self.csvwriter = csv.writer(csvfile)
    
    def start(self, tag, attrib):
        if tag == WordCounter.page:
            self.in_page = True
        elif tag == WordCounter.ns and self.in_page:
            self.in_ns = True
        elif tag == WordCounter.title and self.in_page:
            self.in_title = True
        elif tag == WordCounter.redirect and self.in_page:
            self.in_redirect = True
        elif tag == WordCounter.text and self.in_article:
            self.in_text = True

    def data(self, data):
        if self.in_redirect:
            pass
        elif self.in_ns == True and data == '0':
            self.in_article = True
        elif self.in_title == True:
            self.title += data
        elif self.in_text == True:
            if data.startswith('#REDIRECT'):
                self.in_redirect = True
            else:
                self.words += len(re.findall(r'\w+', data))
        
    def end(self, tag):
        if tag == WordCounter.page and self.in_page == True:
            self.in_page = False
            self.in_redirect = False
            self.words = 0
            self.title = ""
        elif tag == WordCounter.ns and self.in_ns == True:
            self.in_ns = False
        elif tag == WordCounter.title and self.in_title == True:
            self.in_title = False
        elif tag == WordCounter.text and self.in_text == True:
            self.in_text = False
            self.in_article = False
            if not self.in_redirect:
                self.csvwriter.writerow([self.title.encode('utf-8'),
                                         self.words])

    def close(self):
        return
        

csvfile = open('count.csv', 'w')

target = WordCounter(csvfile)

parser = etree.XMLParser(target = target)

if len(sys.argv) > 1:
    infile = sys.argv[1]
else:
    infile = sys.stdin

etree.parse(infile, parser)

csvfile.close()
