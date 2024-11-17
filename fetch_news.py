import requests
import json
import os
from jinja2 import Template

# Your CryptoCompare API key
API_KEY = '1048c9d7ef0df6358f984e6be9466c9b5d83eb5f26a0a57741be7f3f7bd6eb03'
URL = 'https://min-api.cryptocompare.com/data/v2/news/'

params = {
    'feeds': 'cryptocompare,cointelegraph,coindesk',
    'api_key': API_KEY,
    'lang': 'EN',
    'categories': 'BTC,ETH,regulation',
    'excludeCategories': 'Sponsored',
    'extraParams': 'CryptoNewsSite'
}

# Fetch data from CryptoCompare API
response = requests.get(URL, params=params)
news_data = response.json()

# Prepare news articles
articles = news_data.get('Data', [])

# Set up output directory for HTML pages
output_dir = 'news_pages'
os.makedirs(output_dir, exist_ok=True)

# HTML template for the articles with ads
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords }}">
    <meta name="author" content="Crypto News">
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:image" content="{{ image_url }}">
    <meta property="og:url" content="{{ url }}">
    <title>{{ title }}</title>
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
        <p>Published on: {{ published_on }}</p>
    </header>
    <section>
        <img src="{{ image_url }}" alt="{{ title }}">
        <p>{{ body }}</p>
        <a href="{{ url }}" target="_blank">Read more...</a>
    </section>

    <!-- Ad Scripts -->
    <script async="async" data-cfasync="false" src="//pl25032274.profitablecpmrate.com/12caf3e1b967c725bc896a6a73caf0b6/invoke.js"></script>
    <div id="container-12caf3e1b967c725bc896a6a73caf0b6"></div> 
    <script type='text/javascript' src='//pl25032294.profitablecpmrate.com/0f/9f/9c/0f9f9c5c85bb14b4da3ce62b002175ec.js'></script> 
    <script type="text/javascript">
        atOptions = {
            'key' : 'f6669a79207268aad812db292d6b5470',
            'format' : 'iframe',
            'height' : 90,
            'width' : 728,
            'params' : {}
        };
    </script>
    <script type="text/javascript" src="//www.highperformanceformat.com/f6669a79207268aad812db292d6b5470/invoke.js"></script>
</body>
</html>
"""

# Generate HTML files for each article
for article in articles:
    title = article['title']
    url = article['url']
    body = article['body']
    published_on = article['published_on']
    image_url = article.get('imageurl', '')
    description = body[:150]  # Short description for meta description
    keywords = ', '.join(article['tags'].split('|'))  # Tags for meta keywords

    # Render HTML content using Jinja2 template
    template = Template(html_template)
    html_content = template.render(
        title=title,
        url=url,
        body=body,
        published_on=published_on,
        image_url=image_url,
        description=description,
        keywords=keywords
    )

    # Save the HTML content to a file
    file_name = f"{output_dir}/{article['id']}.html"
    with open(file_name, 'w') as file:
        file.write(html_content)
