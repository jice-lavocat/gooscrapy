#!/usr/bin/python
# -*- coding: latin-1 -*-
'''Saves the result of a google query for a given query into a CSV

DONE : 
-- Format the csv file to save :
 * domain | url | keyword_searched_for | serp | city | job
ex : graphemeride.com | http://www.graphemeride.com/contact | seo+france+inurl:contact | 2 | Paris | seo
TODO : 
-- Automatize for all main US city
'''

import sys # Used to add the BeautifulSoup folder the import path
import urllib2 # Used to read the html document
import csv
import time
import random
import os 


if not os.path.exists("output"):    #Will save all data in folder "output"
    os.mkdir("output")

def html_escape(text):
    """Produce entities within text."""
    html_escape_table = {
    "&": "",
    '"': "",
    "'": "",
    ">": "",
    "<": "",
    ":": "",
    "é":"e",
    "è":"e",
    "ê":"e",
    }
    return "".join(html_escape_table.get(c,c) for c in text)
     
     
settings = {
    "extension" : "fr",
    "nb_result" : 10,
    "nb_page" : 1,
    "custom_search" : "0",
    "query" : "Google Scrapy",
    "filename" : "google_scrapy.csv", }

def interface():
    """
    Ask the user about the search to be done
    """
    
    # Query
    print "Enter a query to be searched (default query is '"+settings['query']+"') : ",
    query = raw_input()
    if (query!=""):
        # If the query is empty, keep the default
        settings['query'] = str(query)
    query = settings['query']
    keyword = query.replace(" ","+")
    print "The searched query will be : '"+query+"'"
    print "\n \n"
    
    # Filename
    # we prepare the default filename
    date=time.strftime("%d_%m_%Y")
    filename_default = html_escape(query.replace(" ", "_"))+"_"+str(date)+".csv"
    settings['filename'] = filename_default
    print "Enter a file name (default name is '"+settings['filename']+"') : ",
    filename = raw_input()
    if (filename!=""):
        # If a name if given,
        # We check that an extension was given
        if (filename[-4:]==".csv"):
            settings['filename'] = str(filename)
        else:
            settings['filename'] = str(filename)+".csv"
    filename = "output/"+settings['filename']
    print "The output data will be saved under "+filename
    print "\n \n"
    
    # Result number
    print "Enter a number of results per page (default results is '"+str(settings['nb_result'])+"')"
    print "You can select a number in the following list : 10, 20, 30, 40, 50 or 100 : "
    nb_result = raw_input()
    if (nb_result!=""):
        try:
            nb_result_int = int(nb_result)
            settings['nb_result'] = nb_result_int
        except:
            print "You should provide an integer number for the number of results"
            print "(we keep the default value.)"
            pass
        # Check if number of results is correct for google
        if (settings['nb_result'] not in [10,20,30,40,50,100]):
            print "You made a mistake. We keep the default value"
            settings['nb_result'] = 10
    nb_result = settings['nb_result']
    print "The number of results will be : "+str(nb_result)
    print "\n \n"
    
    # Page number
    print "Enter a number of page to scrape (default number is '"+str(settings['nb_page'])+"') : ",
    nb_page = raw_input()
    if (nb_page!=""):
        try:
            nb_page_int = int(nb_page)
            settings['nb_page'] = nb_page_int
        except:
            print "You should provide an integer number for the number of pages"
            print "(we keep the default value.)"
            pass      
    nb_page = settings['nb_page']
    print "The number of scraped pages will be : "+str(nb_page)
    
    print "***********************"
    print "***********************"
    print "Starting Scraping"
    print "***********************"
    print "***********************"
    url_extract(settings['extension'],nb_result,nb_page,keyword,filename)

    
#if __name__ == "__main__":
def url_extract(extension,nb_result,nb_page,keyword,filename,proxyip=["127.0.0.1"]):
    ### Import Beautiful Soup
    ### Here, I have the BeautifulSoup folder in the level of this Python script
    ### So I need to tell Python where to look.
    #sys.path.append("./BeautifulSoup")
    from BeautifulSoup import BeautifulSoup

    serp = 0 #position of keyword found
    dc = "http://www.google."+str(extension) #datacenter
    
    file_serp = csv.writer(open(filename,"wb"))
    
    useragent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17', 'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)', 'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1', 'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)']

    ### Create opener with Google-friendly user agent with a proxy
    opener = urllib2.build_opener()

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.
    for start in range(0,nb_page):
        #$url="http://$google_ip/search?q=search_string&amp;ie=utf-8&as_qdr=all&amp;aq=t&amp;rls=org:mozilla:us:official&amp;client=firefox&num=100";
        #url = dc+"/search?q="+str(keyword)+"&start=" + str(start*10)+"#sclient=psy-ab&oq=seo+webmarketing"
        url = dc+"/search?q="+str(keyword)+"&amp;ie=utf-8&as_qdr=all&amp;aq=t&amp;rls=org:mozilla:us:official&amp;client=firefox&num="+str(nb_result)+"&hl=fr"
        opener.addheaders = [('User-agent', useragent[start%len(useragent)])]
        print url
        try:
            page = opener.open(url)
            soup = BeautifulSoup(page)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found!"
                break
            elif err.code == 403:
                print "Access denied!"
                break
            elif err.code == 400:
                print "Google recognized the wrong query... try to adapt it!"
                break
            else:
                print "Something happened! Error code", err.code  
                break
        explanation_txt = "# Scraping of Google using Gooscrapy.py "
        url_searched = "# URL queried : "+ url
        explanation_csv = "# Host , URL, SERP, Keyword"
        file_serp.writerow([explanation_txt])
        file_serp.writerow([url_searched])
        file_serp.writerow([explanation_csv])
        ### Parse and find
        ### Looks like google contains URLs in <cite> tags.
        ### So for each cite tag on each page (10), print its contents (url)
        '''for cite in soup.findAll('cite'):
            print cite.text
            serp=serp+1
            file_serp.writerow([serp,cite.text])'''
        for h3 in soup.findAll("h3", {"class": "r"}):
            for a in h3.findAll("a", {"href": True}):
                href=a["href"]
                serp=serp+1
                # Get host and path
                protocol, url = urllib2.splittype(href) # 'http://www.xxx.de/3/4/5' => ('http', '//www.xxx.de/3/4/5')
                host, path =  urllib2.splithost(url)    # '//www.xxx.de/3/4/5' => ('www.xxx.de', '/3/4/5')
                # Save in the following format : domain | url | keyword_searched_for | serp | keyword
                file_serp.writerow([host,href,serp,keyword])
        print str(start+1)+" sur "+str(nb_page)+" page(s) traitee(s)"
    
    #If there is another page to scrape, add a pause
    if (start!=(nb_page-1)):
        print str(start)
        print str(nb_page)
        time.sleep(random.uniform(25,60))

if __name__ == "__main__":
    """ When programm is called, send interface"""
    interface()