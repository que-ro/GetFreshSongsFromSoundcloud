# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 07:54:18 2021

@author: Quentin
"""

from scrapy.spiders import Spider;
from giveMeFreshSongs.items import Song;

class songChasingSpidy(Spider):
    
    name = "song_chasing_spidy";
    allowed_domains= ['soundcloud.com'];
    
    def __init__(self, **kwargs):
        
        #Init starting urls
        with open("profileUrls.txt", "r+") as file_containing_profiles_url:
            profile_urls = (profile_url.rstrip() for profile_url in file_containing_profiles_url.readlines()); # All lines including the blank ones
            profile_urls = (profile_url for profile_url in profile_urls if profile_url); # Non-blank lines
            self.start_urls = profile_urls;
        
        #Execute init of mother class
        super().__init__(**kwargs)
        
    
    def parse(self, response):
        
        song_rows = response.css('div.sound__content');
        
        for song_row in song_rows:
            
            #Extract song info
            author = song_row.css('span.soundTitle__usernameText::text').extract_first();
            song_name = song_row.css('a.soundTitle__title span::text').extract_first();
            upload_date = song_row.css('time.relativeTime::attr(datetime)').extract_first();
            genre = song_row.css('a.soundTitle__tag span::text').extract_first();
            nb_likes = song_row.css('button.sc-button-like::text').extract_first();
            nb_reposts = song_row.css('button.sc-button-repost::text').extract_first();
            nb_of_times_listened = song_row.css('ul > li:nth-child(1) > span > span:nth-child(2)::text').extract_first();
            nb_comments = song_row.css('ul > li:nth-child(2) > a > span:nth-child(2)::text').extract_first();
            href = song_row.css('div.soundTitle__usernameTitleContainer > a::attr(href)').extract_first();
            
            #Format info
            author = StringFormatter.GetStrWithoutLinebreaksAndWhitespace(author);
            song_name = StringFormatter.GetStrWithoutLinebreaksAndWhitespace(song_name);
            upload_date = StringFormatter.GetStrWithoutLinebreaksAndWhitespace(upload_date);
            genre = StringFormatter.GetStrWithoutLinebreaksAndWhitespace(genre);
            nb_likes = StringFormatter.GetIntegerFromStr(nb_likes);
            nb_reposts = StringFormatter.GetIntegerFromStr(nb_reposts);
            nb_of_times_listened = StringFormatter.GetIntegerFromStr(nb_of_times_listened);
            nb_comments = StringFormatter.GetIntegerFromStr(nb_comments);
            href = StringFormatter.GetCompleteSoundcloudUrl(href);
            
            #Score of song
            score = (nb_likes / nb_of_times_listened) * 100;
            
            #Extract song url if score is superior to a threshold
            if(score > 6.5):
                song = Song();
                song['href'] = href;
                yield song;
            
            
class StringFormatter:
    
    @staticmethod
    def GetStrWithoutLinebreaksAndWhitespace(string_to_format):
        if(string_to_format):
            string_to_format = string_to_format.replace('\n', '');
            string_to_format = string_to_format.strip();
            return string_to_format;
        else:
            return "";
        
    @staticmethod
    def GetIntegerFromStr(string_to_format):
        string_to_format = StringFormatter.GetStrWithoutLinebreaksAndWhitespace(string_to_format);
        if(string_to_format == ""):
            return 0;
        else:
            if('K' in string_to_format):
                string_to_format = string_to_format.replace('K', '');
                if(',' in string_to_format):
                    string_to_format = string_to_format.replace(',', '');
                    string_to_format = string_to_format + "00";
                else:
                    string_to_format = string_to_format + "000";
            else:
                if('.' in string_to_format):
                    string_to_format = string_to_format.replace('.', '');
                    
            return int(string_to_format);
        
    @staticmethod
    def GetCompleteSoundcloudUrl(url_suffix):
        return 'https://soundcloud.com/' + url_suffix;            
