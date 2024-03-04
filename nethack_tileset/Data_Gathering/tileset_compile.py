import pandas as pd # library for data analysis
import requests # library to handle requests
import logging # library to handle logging
from bs4 import BeautifulSoup # library to parse HTML documents
import requests # library to handle requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# Make a request to the website
logging.info('Making request to website')
url = "https://nethackwiki.com/wiki/List_of_vanilla_NetHack_tiles"
response = requests.get(url)

# Parse the HTML content
logging.info('Parsing HTML content')
soup = BeautifulSoup(response.text, 'html.parser')

# Find all img tags
logging.info('Finding img tags')
img_tags = soup.find_all('img')

# Initialize lists to store the data
titles = []
hrefs = []
srcs = []

# Loop through the img tags and extract the data
logging.info('Extracting data from img tags')
for img in img_tags:
    if 'png' in img['src']:
        titles.append(img.get('alt'))
        hrefs.append(img.parent.get('href'))
        srcs.append(img.get('src'))

# Create a DataFrame from the data
logging.info('Creating DataFrame')
tileset = pd.DataFrame({
    'Title': titles,
    'Wiki_link': hrefs,
    'Image_link': srcs
})

#  Replace the .png in the Title column
logging.info('Replacing .png in Title column')
tileset['Title'].replace('.png', '', regex=True, inplace=True)

# Remove 2 bottom rows
tileset = tileset[:-2]

#  Save to csv file
logging.info('Saving DataFrame to CSV file')
tileset.to_csv('tileset_vanilla.csv', index=False)

# Save only the first column into a csv file
logging.info('Saving only the first column into a csv file')
tileset['Title'].to_csv('tileset_vanilla_titles.csv', index=False)
logging.info('Done')
