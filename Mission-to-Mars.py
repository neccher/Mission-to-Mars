#Import Depencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set up executable
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    #Visit Mars Data site
    url ='https://redplanetscience.com'
    browser.visit(url)
    #Optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Set up HTML Parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except block for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #Use parent element to find first a tag and save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #Use parent element to find first a tag and save it as summary
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    #Visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find and click button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse resuling html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add error handling
    try:
        #Find relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
   
    return img_url

def mars_facts():
    #try/except block
    try:
        #grabbing table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    #Assign columns and set index  
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #convert dataframe to html. add bootstrap    
    return df.to_html()

browser.quit()
