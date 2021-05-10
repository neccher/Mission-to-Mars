#Import Depencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set up executable
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Visit Mars Data site
url ='https://redplanetscience.com'
browser.visit(url)
#Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#Set up HTML Parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#Find Titles
slide_elem.find('div', class_='content_title')

#Use parent element to find first a tag and save it as news_title
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#Use parent element to find first a tag and save it as summary
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

#Visit url
url = 'https://spaceimages-mars.com'
browser.visit(url)

#Find and click button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#Parse resuling html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#Find relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#grabbing table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()
