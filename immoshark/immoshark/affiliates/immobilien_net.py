'''
Created on Aug 21, 2012

@author: zking
'''
from immoshark.utils import downloader
import urllib
from immoshark import config
from BeautifulSoup import BeautifulSoup
import re
from immoshark.object import RealEstateObject

class ImmobilienNet(object):
    '''
    classdocs
    '''
    
    ###############################################################################
    # CONFIG
    ###############################################################################
    base_url   = 'http://www.immobilien.net'
    search_url = 'treffer.aspx'
    
    __name__   = 'immobilien.net'


    def __init__(self):
        self.search_url = '/'.join([self.base_url, self.search_url])
        self.session = config.db_session()
          
   
    def crawl(self, **param):
        '''
        '''
        for item in self.item_list(self.search_url, **param):
            item = self.item_details(item=item)
            self.session.add(item)
        
    
    def item_details(self, url=None, item=None):
        '''
        '''
        if item is None: item=RealEstateObject(affiliate=self.__name__, url=url)
        
        #download page and cook some soup
        html = downloader.download_page(item.url, config.http_request_retries, config.http_request_sleep).read()
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        
        for griditem in soup.findAll('div', {'class': 'detailGrid'}):
            key = griditem.find('dt').text
            value = griditem.find('dd').text
            print key, value
            
        print soup.find('title').text.strip()
        
        print soup.find('div', {'class': 'panel'})
            
        
        return item
        
        
    
    
    def item_list(self, url, **param):
        '''
        url               http://www.immobilien.net/treffer.aspx
        eCult             at
        eDB               DBImmobiliensuche
        egeo0             39926
        egeo1             39882
        etype0            352
        etype1            354
        iskauf            true
        kaufpreisbis      500000
        nutzflaechevon    200
        '''
        #download page and cook some soup
        html = downloader.download_page('?'.join([url, urllib.urlencode(param)]) if param else url, config.http_request_retries, config.http_request_sleep).read()
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        
        #yield the item links and ids
        for item in soup.findAll('a', id=re.compile('majorContent_sbContainer_ctl00_resCTXContainer_ctl00_LoginView2_Tab3_resultList_LinkLiteral1')):
            item_url = self.base_url + item['href']
            yield RealEstateObject(affiliate=self.__name__, url=item_url, id=re.search('/([0-9]+-[0-9]+)/', item_url).group(1))
        
        #if there's a next page, do the same for that one too    
        next_page = soup.find('a', id=re.compile('majorContent_sbContainer_ctl00_resCTXContainer_ctl00_LoginView2_Tab3_nextLink'))
        
        if next_page and next_page.has_key('href'):
            next_page_url = self.base_url + next_page['href']
            for item in self.item_list(next_page_url): yield item
        
        

a = ImmobilienNet()
a.crawl(eCult='at', eDB='DBImmobiliensuche', etype0='354', etype1='352', egeo0='39926', egeo1='39882', iskauf='true', kaufpreisbis='400000', nutzflaechevon='200')