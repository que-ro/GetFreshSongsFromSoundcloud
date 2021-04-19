# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 08:22:05 2021

@author: Quentin
"""

from scrapy.spiders import Spider;
from selenium import webdriver;
from webdriver_manager.chrome import ChromeDriverManager;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import logging;
from selenium.webdriver.remote.remote_connection import LOGGER
import time;

class ProfileChasingSpidy(Spider):
    
    name = "profile_chasing_spidy";
    allowed_domains= ['soundcloud.com'];
    
    #To run the spidy: scrapy crawl myspider -a url=yoursoundcloudurl 
    def __init__(self, url='', **kwargs):
        
        #Init starting urls
        self.start_urls = [url];
        
        #Init of the selenium webdriver
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),);
        
        #Selenium logs set to warning
        LOGGER.setLevel(logging.WARNING);
        
        #Execute init of mother class
        super().__init__(**kwargs)
        
        
    def parse(self, response):
        
        #Execute request
        self.driver.get(response.url);
        
        #Wait until play button is clickable to pause it if it plays automatically
        playButton = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "playButton")]')));
        
        titleOfPlayButton = playButton.get_attribute('title');
        
        if(titleOfPlayButton == 'Mettre en pause'):
            playButton.click();
                
        #Wait until the link to go to list of people who liked the music is available
        linkToPeopleWhoLiked = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "sc-ministats-likes")]')));
        
        #Go to the list of people who like the music
        linkToPeopleWhoLiked.click();
        
        #Wait until the first profiles are displayed
        randomUserProfile = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "userBadgeListItem__image")]')));
        
        # Scroll to bottom
        self.scrollToBottom();
        
        #When the page is fully loaded, retrieve all a element containing profile urls
        allUsersWhoLiked = self.driver.find_elements_by_xpath('//a[contains(@class, "userBadgeListItem__image")]');
        
        list_of_url_profiles = []
        
        for user in allUsersWhoLiked:
            list_of_url_profiles.append(user.get_attribute('href'));
         
        #Writing the profiles url in a text file
        file_containing_profiles_url = open("profileUrls.txt", "w+");
        file_containing_profiles_url.writelines(url + '\n' for url in list_of_url_profiles);
        file_containing_profiles_url.close();
        
        #Closing the webdriver
        self.driver.close();
            
        
    def scrollToBottom(self):
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight");
        
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
        
            # Wait to load page
            time.sleep(0.5);
        
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight");
            if new_height == last_height:
                break;
            
            last_height = new_height;
            
            