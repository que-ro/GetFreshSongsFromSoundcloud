# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver;
from webdriver_manager.chrome import ChromeDriverManager;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import logging;
from selenium.webdriver.remote.remote_connection import LOGGER
import time;
from scrapy.utils.python import to_bytes;
from scrapy.http import HtmlResponse;

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class GivemefreshsongsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GivemefreshsongsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        
        if(spider.name != 'song_chasing_spidy' or 'robots.txt' in request.url):
            return None;
        
        #Init of the selenium webdriver
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install());
        
        #Selenium logs set to warning
        LOGGER.setLevel(logging.WARNING);
        
        #Execute request
        driver.get(request.url);
        
        #Wait until links to favorite songs of profile is displayed
        link_to_favorites = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "sidebarHeader ")]')));
        
        #Navigate to favorite songs page
        link_to_favorites.click();
        
        # Scroll to bottom of the page
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight");
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
        
            # Wait to load page
            time.sleep(0.5);
        
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight");
            if new_height == last_height:
                break;
            
            last_height = new_height;
            
        #Set return parameters
        body = to_bytes(driver.page_source);
        url = driver.current_url;
        
        #Close driver
        driver.close();
        
        #Return response to spider
        return HtmlResponse(url, body=body, encoding='utf-8', request=request)
    

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name);
