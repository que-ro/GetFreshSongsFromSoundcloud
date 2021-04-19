# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 07:53:35 2021

@author: Quentin
"""


import scrapy;
from scrapy.spiders import Spider;
from selenium import webdriver;
from webdriver_manager.chrome import ChromeDriverManager;
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import time;
from bs4 import BeautifulSoup;

class ProfileChasingSpidy(Spider):
    
    name = "temp";
    allowed_domains= ['soundcloud.com'];
    
    #To run the spidy: scrapy crawl myspider -a url=yoursoundcloudurl 
    def __init__(self, url='', **kwargs):
        self.start_urls = [url];
        chromeOptions = Options();
        chromeOptions.add_argument('--log-level=3');
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chromeOptions);
        LOGGER.setLevel(logging.WARNING);
        super().__init__(**kwargs)
        
    def parse(self, response):
        self.driver.get(response.url);
        
        playButton = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "playButton")]')));
        
        titleOfPlayButton = playButton.get_attribute('title');
        
        if(titleOfPlayButton == 'Mettre en pause'):
            playButton.click();
                
        linkToPeopleWhoLiked = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "sc-ministats-likes")]')));
        
        linkToPeopleWhoLiked.click();
        
        randomUserProfile = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "userBadgeListItem__image")]')));
        
        # Scroll to bottom
        self.scrollToBottom();
            
        allUsersWhoLiked = self.driver.find_elements_by_xpath('//a[contains(@class, "userBadgeListItem__image")]');
        
        list_of_url_profiles = []
        
        for user in allUsersWhoLiked:
            list_of_url_profiles.append(user.get_attribute('href'));
            
        i = 0;
        while(i < 1):
            yield scrapy.Request(url=list_of_url_profiles[i], callback=self.parse_profile);
            i += 1;
            
        
    def parse_profile(self, response):
        
        self.driver.get(response.url);
        
        link_to_favorites = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "sidebarHeader ")]')));
        
        link_to_favorites.click();
        
        # Scroll to bottom
        self.scrollToBottom();
        
        #get all songs web elements
        song_web_elements = self.driver.find_elements_by_xpath('//div[contains(@class, "sound__content")]');
        
        #extact info of songs
        self.extractSongsInfo();
        
        
    def scrollToBottom(self):
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        stop_idx = 0;
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(0.5)
        
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            if stop_idx > 2:
                break
            stop_idx += 1;
            last_height = new_height
            
            
    def extractSongsInfo(self):
        
        print('EXTRACTION //////////////////////')
        
        soup = BeautifulSoup(self.driver.page_source, 'lxml');
        
        song_rows = soup.find_all('div', class_='sound__content');
        
        print('EXTRRACTION LOOPING ///////////////');
        
        for song_row in song_rows:
            
            print('SONG ///////')
            print(song_row)
            
            author = song_row.find('span', class_='soundTitle__usernameText').text;
            song_name = song_row.select_one('a.soundTitle__title span');
            upload_date = song_row.find('time', class_='relativeTime').get('datetime');
            genre = song_row.select_one('a.soundTitle__tag span')
            nb_likes = song_row.find('button', class_='sc-button-like').text;
            nb_reposts = song_row.find('button', class_='sc-button-repost').text;
            nb_of_times_listened = song_row.select('ul.soundStats li')[0];
            #nb_comments = song_row.select('ul.soundStats li')[1];
            
            print("//////////////////////////////////// !!!!!!!!!!!!!!!!!!! ///////////////////////////////////////")
            
            print(author)
            print(song_name)
            print(upload_date)
            print(genre)
            print(nb_likes)
            print(nb_reposts)
            print(nb_of_times_listened)
            #print(nb_comments)
            