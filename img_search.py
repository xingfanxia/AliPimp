#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-15 06:18:28
# @Author  : Xingfan Xia (xiax@carleton.edu)
# @Link    : http://xiax.tech
# @Version : $1.1

from cookielib import CookieJar
import os, re, urlhelper, time, urllib2, lxml, requests
from lxml import html, etree

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def image_lookup(path):
    google_path = 'http://images.google.com/searchbyimage?image_url=' + path
    source = opener.open(google_path).read()
    # open('test.html', 'w').write(source) #debug
    tree = etree.HTML(source)
    internal_url = tree.xpath(".//*[@id='imagebox_bigimages']/g-section-with-header/div[2]/h3/a/@href")
    image_page = "http://www.google.com/" + internal_url[0]
    image_source = opener.open(image_page).read()
    links = re.findall(r'"ou":"(.*?)","ow"', image_source)
    return links

def image_scrape(links, path):
    counter = 0
    for link in links:
        counter += 1
        filename = "image" + str(counter)
        ext = '.' + link.split('.')[-1]

        print "Link : " + link

        # Save Image
        try:    # Try to Download Image and print if error
            img = urllib2.urlopen(link)
            filepath = os.path.join(path, filename + ext)
            if not os.path.exists(path):
                os.makedirs(path)
            print filepath
            try:
                with open(filepath, 'wb') as local_file:
                    local_file.write(img.read())
                    print "Saved: " + filename
            except:
                print "not standard URL"

        except urllib2.URLError, err:   # TODO Why are some links "Bad Request"
            # print err.read()
            print err.reason
            print "Error"

def valid_url(url):
    validation = re.findall(urlhelper.URL_REGEX, url)
    return validation

def main():	
    '''
    Some imgs to be used:
    http://7xqpdw.com1.z0.glb.clouddn.com/mi_faker.jpg
    http://7xqpdw.com1.z0.glb.clouddn.com/menggou.png
    http://7xqpdw.com1.z0.glb.clouddn.com/dchen.jpeg
    http://7xqpdw.com1.z0.glb.clouddn.com/feizao.png
    '''
    url =  "http://photocdn.sohu.com/20151231/mp51708433_1451565460566_44.jpeg"
    path = "similar_Images"
    if not valid_url(url):
        print "Error: Not valid URL"
    start = time.time()
    links = image_lookup(url)   # search for similar
    image_scrape(links, path)         # save results
    end = time.time()   # Debug runtime
    print "Search Time: " + str(end - start) + ' seconds'
if __name__ == '__main__':
    main()
