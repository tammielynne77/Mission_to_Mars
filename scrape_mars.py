from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/Users/tamaradaniels/Desktop/Python/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)



def scrape():
    browser = init_browser()
    mars = {}

#Scrape news and teaser
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars['news_title'] = soup.find('div', class_= 'content_title').text
    mars['news_p'] = soup.find('div', class_= 'article_teaser_body').text

#Scrape featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    image = browser.find_by_id('full_image')
    image.click()
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    featured_image_url = soup.find('div',class_='fancybox-inner')
    mars['featured_image_url'] = 'https://www.jpl.nasa.gov' + featured_image_url.find('img',class_='fancybox-image')['src']

#Mars tweet
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars['tweet'] = soup.find(class_ = "js-tweet-text-container").text

#Mars facts
    mars_url = 'https://space-facts.com/mars/'
    mars['table'] = pd.read_html(mars_url)
    
#Mars hemisphere images
    mars_image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_title = []

    for item in soup.find_all(class_= 'description'):
        image_title.append(item.find('h3').text)


    url_for_link = 'https://astrogeology.usgs.gov'

    urls = []

    for link in soup.find_all('a', attrs={"class":"itemLink"}):
        urls.append(url_for_link + link.get('href'))

    final_url = list(set(urls))
    final_url.sort()

    mars['hemisphere_images'] = [{'title': image_title[0], 'img_url': final_url[0] }, {'title': image_title[1], 'img_url': final_url[1] },
                                 {'title': image_title[2], 'img_url': final_url[2] }, {'title': image_title[3], 'img_url': final_url[3] }]

    return mars