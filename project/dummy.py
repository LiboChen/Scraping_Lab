import json
import sys
import re
import urllib

from bs4 import BeautifulSoup
import string

def add(a, b):
    return a + b

def mycomp(a, b):
    x = str(a[7].text)
    y = str(b[7].text)
    #print x;
    #print y;
    s1 = string.replace(x, ",", "")
    s2 = string.replace(y, ",", "")
    return int(s2) - int(s1)


def contractAsJson(filename):
    jsonQuoteData = "[]"
    #return jsonQuoteData
    fh = open(filename)
    soup = BeautifulSoup(fh)

    #price = soup.find_all("yfs_l84")
    cur_price = soup.find(class_="time_rtq_ticker")
    currPrice = float(cur_price.find(id=re.compile("yfs")).text)

    #urls = soup.find_all("a", {"href": re.compile("/q/op?")});
    #urls = soup.find_all("a");
    urls = soup.find_all("a", href = re.compile("\/q\/o[s,p]\?s=[A-Za-z]+&m"));
    dateUrls = []

    #print urls
    for link in urls:
	    #print link.get("href")
	    link["href"] = "http://finance.yahoo.com" + link["href"]
	    new_link = string.replace(link["href"], '&', '&amp;')
	    #print new_link
	    dateUrls.append(new_link)
#print dateUrls

################find options################################
    tables = soup.find_all(class_="yfnc_datamodoutline1")

    table1 = tables[0].find_all("tr")
    table2 = tables[1].find_all("tr")
    mytable = []

    for row_index in range(2, len(table1)):
        row = table1[row_index]
        info_list = row.find_all("td")
        #for i in range(0, len(info_list)):
            #print info_list[i].text
        mytable.append(info_list)

    for row_index in range(2, len(table2)):
        row = table2[row_index]
        info_list = row.find_all("td")
        #for i in range(0, len(info_list)):
            #print info_list[i].text
        mytable.append(info_list)

    #print mytable
    mytable.sort(mycomp)
    option_list = []
    #print "table row lenth", len(mytable)
    for row_index in range(0, len(mytable)):
        option = dict()
        option["Strike"] = str(mytable[row_index][0].text)
        symbol = str(mytable[row_index][1].text)
        start = symbol.find("1")
        option["Symbol"] = symbol[:start]
        rest = symbol[start:]
        option["Date"] = re.split('[A-Z]', rest)[0]
        option["Type"] = rest[len(option["Date"])]
        option["Last"] = str(mytable[row_index][2].text)
        option["Change"] = str(mytable[row_index][3].text)
#        if(mytable[row_index][4].text != None):
#            option["Bid"] = str(mytable[row_index][4].text)
#        else:
#            option["Bid"] = "N/A"     
        option["Bid"] = str(mytable[row_index][4].text)
        option["Ask"] = str(mytable[row_index][5].text)
        option["Vol"] = str(mytable[row_index][6].text)
        option["Open"] = str(mytable[row_index][7].text)
        option_list.append(option)

    #print option_list
    
    summary = dict()
    summary["currPrice"] = currPrice
    summary["dateUrls"] = dateUrls
    summary["optionQuotes"] = option_list
    #jsonQuoteData = json.dumps(sorted(summary.iterkeys()))
    #jsonQuoteData = json.dumps(summary)
    jsonQuoteData = json.dumps(summary, sort_keys = True, indent = 4, separators=(',', ': '))

    return jsonQuoteData




