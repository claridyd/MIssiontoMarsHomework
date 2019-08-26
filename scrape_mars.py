# import libraries
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
import requests

def init_browser():
    executable_path = {"executable_path": "c:/DataVisual/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Setup dictionary
    #Mars_data ={}

    # specify NASA Mars site url
    url = "https://mars.nasa.gov/news/8503/robotic-toolkit-added-to-nasas-mars-2020-rover"
    page = urllib.request.urlopen(url)
    soup = bs(page, 'lxml')

    # Get news title 
    news_title = soup.find(class_='article_title').text.strip()
    # print(news_title)
    #Mars_data["news_title"] = news_title

    # Get paragraph texts
    news_p = soup.body.find('p').text
    #Mars_data["news_p"] = news_p

    # Get url for JPL Mars Space image
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19952_hires.jpg'
    browser.visit(featured_image_url)

    # Twitter url to scrape
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    # open the URL using urllib.request and put the HTML into the page variable
    twit_page = urllib.request.urlopen(twit_url)

    # parse the HTML from our url into the BeautifulSoup parse tree format
    twit_soup = bs(twit_page, 'lxml')

    # twit_soup.find_all('p')
    # Get latest Mars weather from Twitter
    mars_weather = twit_soup.find('p', attrs={'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text.strip()

    # Get Mars Facts 
    facts_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(facts_url)
    fact_df = fact_table[1]
    fact_df.columns = ['Metric', 'Measurement']
    fact_html = fact_df.to_html()
    fact_html = fact_html.replace('\n', '')


    hemisphere_image_urls = [
    {"title": "Cereberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"}  
]

    # Store Mars data in dictionary
    Mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": fact_html,
        "hemisphere_image": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return Mars_data
    

