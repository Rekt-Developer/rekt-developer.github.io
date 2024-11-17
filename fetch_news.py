import requests
import os
import json
from jinja2 import Template
from datetime import datetime

# API Configuration
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

# Create output directory
output_dir = 'news_pages'
os.makedirs(output_dir, exist_ok=True)

# Ad Script to be included in the page
ad_script = """
<script async="async" data-cfasync="false" src="//pl25032274.profitablecpmrate.com/12caf3e1b967c725bc896a6a73caf0b6/invoke.js"></script>
<div id="container-12caf3e1b967c725bc896a6a73caf0b6"></div> 
<script type='text/javascript' src='//pl25032294.profitablecpmrate.com/0f/9f/9c/0f9f9c5c85bb14b4da3ce62b002175ec.js'></script> 
<script type='text/javascript' src='//pl25013478.profitablecpmrate.com/66/17/d7/6617d7163a895c776c2db7800c9d3306.js'></script> 
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
"""

# HTML Template for Articles (Full Content Page)
article_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords }}">
    <meta name="author" content="{{ author }}">
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:image" content="{{ image_url }}">
    <meta property="og:url" content="{{ url }}">
    <title>{{ title }} - Crypto News</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-blue-600 shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <a href="../index.html" class="text-white text-2xl font-bold">Crypto News</a>
                <div class="flex space-x-4">
                    <a href="../index.html" class="text-white hover:text-blue-200">Home</a>
                    <a href="#" class="text-white hover:text-blue-200">Markets</a>
                    <a href="#" class="text-white hover:text-blue-200">Analysis</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Article Content -->
    <main class="max-w-4xl mx-auto px-4 py-8">
        <article class="bg-white rounded-lg shadow-lg overflow-hidden">
            <!-- Article Header -->
            <header class="p-6 border-b">
                <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ title }}</h1>
                <div class="flex items-center text-gray-600 text-sm">
                    <span class="mr-4"><i class="fas fa-user mr-2"></i>{{ author }}</span>
                    <span><i class="fas fa-calendar mr-2"></i>{{ published_on }}</span>
                </div>
            </header>

            <!-- Article Image -->
            <div class="relative h-96">
                <img src="{{ image_url }}" alt="Article Image" class="w-full h-full object-cover">
            </div>

            <!-- Article Body -->
            <div class="p-6">
                <div class="prose max-w-none">
                    {{ body }}
                </div>

                <!-- Tags -->
                <div class="mt-6 flex flex-wrap gap-2">
                    {% for tag in tags.split(',') %}
                    <span class="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm">{{ tag.strip() }}</span>
                    {% endfor %}
                </div>
            </div>
        </article>

        <!-- Ad Script -->
        <div class="mt-8">
            {{ ad_script | safe }}
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12">
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-3 gap-8">
                <div>
                    <h3 class="text-lg font-bold mb-4">About Us</h3>
                    <p class="text-gray-400">Your trusted source for cryptocurrency news and analysis.</p>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#" class="hover:text-white">Home</a></li>
                        <li><a href="#" class="hover:text-white">Markets</a></li>
                        <li><a href="#" class="hover:text-white">Analysis</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-4">Follow Us</h3>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-facebook"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-linkedin"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# HTML Template for the Index Page (Homepage)
index_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Crypto News Site - Latest News in Crypto">
    <meta name="keywords" content="crypto, bitcoin, ethereum, news, market">
    <title>Crypto News - Latest Articles</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-blue-600 shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <a href="#" class="text-white text-2xl font-bold">Crypto News</a>
                <div class="flex space-x-4">
                    <a href="#" class="text-white hover:text-blue-200">Home</a>
                    <a href="#" class="text-white hover:text-blue-200">Markets</a>
                    <a href="#" class="text-white hover:text-blue-200">Analysis</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="bg-blue-700 text-white py-16">
        <div class="max-w-7xl mx-auto px-4">
            <h1 class="text-4xl font-bold mb-4">Latest Cryptocurrency News</h1>
            <p class="text-xl text-blue-100">Stay informed with the latest updates from the crypto world</p>
        </div>
    </div>

    <!-- Featured Articles -->
    <div class="max-w-7xl mx-auto px-4 py-12">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for article in articles %}
            <div class="bg-white shadow-lg rounded-lg overflow-hidden">
                <img src="{{ article.imageurl }}" alt="Article Image" class="w-full h-64 object-cover">
                <div class="p-6">
                    <h2 class="text-xl font-bold text-gray-900 mb-4">{{ article.title }}</h2>
                    <p class="text-gray-600 mb-4">{{ article.body | truncate(100) }}</p>
                    <a href="{{ article.url }}" class="text-blue-600 hover:text-blue-800">Read More</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Ad Script -->
    <div class="mt-8">
        {{ ad_script | safe }}
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8">
        <div class="max-w-7xl mx-auto px-4">
            <p class="text-center text-gray-400">&copy; 2024 Crypto News. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

# Fetch and parse the news
def fetch_news():
    response = requests.get(URL, params=params)
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            data = response.json()
            print(json.dumps(data, indent=4))  # For debugging
            return data['data']['feeds']
        except KeyError as e:
            print(f"Error: Missing expected data key: {str(e)}")
            return []
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON response")
            return []
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

# Save the articles as individual HTML files
def save_articles(articles):
    for article in articles:
        article_html = Template(article_html_template).render(
            title=article['title'],
            description=article['body'],
            keywords="crypto, bitcoin, ethereum, regulation, news",
            author=article['source_info']['name'],
            published_on=datetime.utcfromtimestamp(article['published_on']).strftime('%B %d, %Y'),
            image_url=article['imageurl'],
            body=article['body'],
            tags=article['categories'],
            url=article['url'],
            ad_script=ad_script
        )
        
        article_file = os.path.join(output_dir, f"{article['id']}.html")
        with open(article_file, 'w') as f:
            f.write(article_html)

# Save the index page
def save_index(articles):
    index_html = Template(index_html_template).render(
        articles=articles,
        ad_script=ad_script
    )
    with open("index.html", 'w') as f:
        f.write(index_html)

# Main function
def main():
    articles = fetch_news()
    if articles:
        save_articles(articles)
        save_index(articles)

if __name__ == "__main__":
    main()
