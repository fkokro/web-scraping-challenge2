#----------------------------------------------------------
#Webpage Scrape Function
#----------------------------------------------------------

def scrape():
    
    #Import Relevant Libraries
    import pandas as pd
    from bs4 import BeautifulSoup as BS
    import requests
    from splinter import Browser
    import pymongo
    from Driver import chromedriver
    
    
    executable_path = {'executable_path': 'chromedriver' }
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_facts_data = {}
    
    #-------------------------------------------------
    # NASA Mars News
    #-------------------------------------------------
    
    #URL to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    #Retrieve page with request module
    response = requests.get(url)
    #Create a Beautiful Soup object
    mars_soup = BS(response.text, 'lxml')
    
    #Loop with a try and catch error block that pasres through the NASA data soup to print all titles and summary paragraphs
    for i in range(0, len(mars_soup.find_all('div',{'class':'content_title'}))):
        #error handling
        try:
            #Identitfy title and return
            news_title = mars_soup.find_all('div', {'class':'content_title'})[i].text.strip()
            #Find and return and article descriptions
            news_p = mars_soup.find_all('div',{'class':'rollover_description_inner'})[i].text.strip()
    
            #Print if title and paragraph are available
            if (news_title and news_p):
                mars_facts_data['news_title'] = news_title
                mars_facts_data['news_paragraph'] = news_p 
    
        except AtrributeError as e:
            print(e)
     
    #-------------------------------------------------
    #JPL Mars Space Images - Featured Image (Splinter)
    #-------------------------------------------------
    
    
    #URL to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #Retrieve page with request module
    browser.visit(url)
    #Create html object
    html = browser.html
    #Create soup from html
    jpl_soup = BS(html, 'lxml')
    # pull images from website
    images = jpl_soup.find_all('a', class_="fancybox")
    
    # pull image link
    image_url = []

    #Loop through image list and capture urls of large images
    for image in images:
        #Try and catch block to catch all image links and print if not throw an error
        try:
            pic = image['data-fancybox-href']
            image_url.append(pic)
    
            if(pic):
                featured_image_url = 'https://www.jpl.nasa.gov' + pic
                mars_facts_data['featured_image_url'] = featured_image_url
        
       
        except AtrributeError as e:
            print(e)
            
    #-------------------------------------------------
    #Mars Weather (Splinter)
    #-------------------------------------------------
    base_weather_url = 'https://twitter.com/marswxreport?lang=en'
    weather_url='https://twitter.com/MarsWxReport/status/1233751572125028354'
    Browser.visit(weather_url)
    # create html object and parse with beautifulsoup
    time.sleep(1)
    weather_html = Browser.html
    weather_soup = bs(weather_html, 'lxml')
    # scrape the weather information
    weather = weather_soup.find('title')
    weather = weather.text       
    
    #-------------------------------------------------
    #Mars Facts (Pandas)
    #-------------------------------------------------
    
    url = 'https://space-facts.com/mars/'
    #Retrieve page with request module
    mars_facts = pd.read_html(url)
    #Print response list
    mars_facts
    #Convert response list to dataframe
    df = mars_facts[0]
    #Convert dataframe to html
    mars_facts_html = df.to_html()
    #Mars facts html into df
    mars_facts_data['mars_facts_html'] = mars_facts_html 
    
    
    #-------------------------------------------------
    #Mars Hemispheres (Splinter)
    #-------------------------------------------------
    # Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    #Create html object
    html2 = browser.html
    #Create soup from html
    hemi_soup = BS(html2, 'lxml')
    # Retrieve items that contain hemisphere info
    items = hemi_soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Define anchor url 
    hemisphere_base_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for ext in items: 
        try:
            # Store title
            title = ext.find('h3').text
    
            # Store link appendage for full image link
            append_img_url = ext.find('a', class_='itemLink product-item')['href']
    
            # Visit full image website 
            browser.visit(hemisphere_base_url + append_img_url)
    
            # Create HTML object of individual hemisphere information website 
            append_img_html = browser.html
    
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BS(append_img_html, 'html.parser')
    
            # Build full image url 
            img_url = hemisphere_base_url + soup.find('img', class_='wide-image')['src']
    
            if(title and img_url):
                # Append to a list of dictionaries 
                hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
                mars_facts_data["title"] = title
                mars_facts_data["img_url"] = img_url
       
        except AtrributeError as e:
            print(e)
        
    return mars_facts_data