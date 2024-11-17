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
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Crypto News">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ title }}">
    <meta name="twitter:description" content="{{ description }}">
    <meta name="twitter:image" content="{{ image_url }}">
    <meta name="twitter:url" content="{{ url }}">
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

    <!-- Ad Banner -->
    <div class="bg-gray-800 text-white text-center py-4">
        <p class="font-semibold">Advertise with us!</p>
        <p>Contact us for ad placement on our website.</p>
    </div>

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

        <!-- Related Articles -->
        <div class="mt-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Related Articles</h2>
            <div class="grid grid-cols-2 gap-6">
                <!-- Placeholder for related articles -->
            </div>
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
    <meta name="author" content="Crypto News">
    <meta property="og:title" content="Crypto News - Latest Articles">
    <meta property="og:description" content="Stay informed with the latest updates from the crypto world">
    <meta property="og:image" content="https://www.example.com/images/logo.png">
    <meta property="og:url" content="https://www.example.com">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
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

    <!-- Ad Banner -->
    <div class="bg-gray-800 text-white text-center py-4">
        <p class="font-semibold">Advertise with us!</p>
        <p>Contact us for ad placement on our website.</p>
    </div>

    <!-- Latest Articles Section -->
    <main class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Latest Articles</h1>
        <div class="grid grid-cols-3 gap-6">
            {% for article in articles %}
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
                <img src="{{ article.image_url }}" alt="Article Image" class="w-full h-56 object-cover">
                <div class="p-4">
                    <h2 class="text-xl font-semibold text-gray-800">{{ article.title }}</h2>
                    <p class="text-gray-600 mt-2">{{ article.description }}</p>
                    <a href="{{ article.url }}" class="text-blue-600 mt-4 inline-block">Read More &raquo;</a>
                </div>
            </div>
            {% endfor %}
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

def fetch_news():
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        return response.json()['data']['feeds']
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

def generate_article_html(article):
    template = Template(article_html_template)
    return template.render(
        title=article['title'],
        description=article['description'],
        image_url=article['imageurl'],
        body=article['body'],
        url=article['url'],
        author=article['source'],
        published_on=datetime.fromtimestamp(article['published_on']).strftime('%B %d, %Y'),
        tags=article.get('tags', ''),
    )

def generate_index_html(articles):
    template = Template(index_html_template)
    return template.render(articles=articles)

# Main Execution
if __name__ == "__main__":
    news_articles = fetch_news()

    # Generate Article Pages
    for article in news_articles:
        article_html = generate_article_html(article)
        article_filename = f"{article['guid'].split('/')[-1]}.html"
        with open(os.path.join(output_dir, article_filename), 'w', encoding='utf-8') as f:
            f.write(article_html)
    
    # Generate Index Page
    index_html = generate_index_html(news_articles)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"{len(news_articles)} articles and index page generated.")
