# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 07:19:02 2021

@author: Quentin
"""

import os;
import sys, getopt;


def main(argv):
    
    try:
        opts, left_args = getopt.getopt(argv, "hu:", ["url="]);
    except getopt.GetoptError as err:
        print(err);
        printHelpMessage();
    
    if(len(opts) == 0 or len(left_args) > 0):
        printHelpMessage();
        sys.exit(2);
    
    for opt, arg in opts:
        if opt == "-h":
            printHelpMessage();
        elif opt in ("-u", "--url"):
            launchScripts(arg);
            
        
def printHelpMessage():
    print("python get_fresh_songs.py -u <soundcloud url of the music you like>");
    
def launchScripts(url):
    #run first spider to get list of profiles that liked the music
    launch_first_spider_script = 'scrapy crawl profile_chasing_spidy -a url=' + url;
    os.system(launch_first_spider_script);
    launch_second_spider_script = 'scrapy crawl song_chasing_spidy';
    os.system(launch_second_spider_script);
     
        
if __name__ == "__main__":
    main(sys.argv[1:]);