'''
Created on Feb 23, 2012

@author: zking
'''

import urllib2
import urllib
from flimmit.exception.http import HttpException
import logging
import time


def download_page(url, retries=3, sleep=0.5):
    """
    Tries to download a page for <retries> times
    @return: response object
    """
    if isinstance(url, urllib2.Request): url_str = url.get_full_url()
    else: url_str = url
    logging.getLogger('flimmit.utils.downloader.download_page').info('GET ' + str(url_str))
    attempts = 0
    while True:  
        try: 
            time.sleep(sleep)
            return urllib2.urlopen(url)
        except urllib2.URLError as e:
            attempts += 1
            if attempts == retries: raise HttpException(e)


def post(url, values):
    
    logging.getLogger('flimmit.utils.downloader.post').info('POST ' + url + ' ' + str(values))
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    return urllib2.urlopen(req)



