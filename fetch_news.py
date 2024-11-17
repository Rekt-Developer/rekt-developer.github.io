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
        <h2 class="text-3xl font-bold mb-8">Featured Stories</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for article in articles %}
            <div class="bg-white rounded-lg shadow-lg overflow-hidden transition-transform duration-300 hover:transform hover:scale-105">
                <img src="{{ article.image_url }}" alt="Article Image" class="w-full h-48 object-cover">
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2 text-gray-900">{{ article.title }}</h3>
                    <p class="text-gray-600 mb-4">{{ article.body[:150] }}...</p>
                    <div class="flex justify-between items-center">
                        <a href="news_pages/{{ article.id }}.html" class="text-blue-600 hover:text-blue-800 font-semibold">
                            Read More <i class="fas fa-arrow-right ml-2"></i>
                        </a>
                        <span class="text-gray-500 text-sm"><i class="far fa-clock mr-2"></i>{{ article.published_on }}</span>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Newsletter Section -->
    <div class="bg-gray-100 py-12">
        <div class="max-w-7xl mx-auto px-4">
            <div class="bg-white rounded-lg shadow-lg p-8 flex flex-col items-center">
                <h2 class="text-2xl font-bold mb-4">Subscribe to Our Newsletter</h2>
                <p class="text-gray-600 mb-6">Get the latest crypto news delivered straight to your inbox</p>
                <form class="w-full max-w-md flex gap-4">
                    <input type="email" placeholder="Enter your email" class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        Subscribe
                    </button>
                </form>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12">
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
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

def format_date(timestamp):
    """Format Unix timestamp to readable date"""
    return datetime.fromtimestamp(timestamp).strftime('%B %d, %Y')

# Fetch and process data
response = requests.get(URL, params=params)
news_data = response.json()
articles = news_data.get('Data', [])

# Generate pages
all_articles = []

for article in articles:
    article_id = article['id']
    title = article['title']
    url = article['url']
    body = article['body']
    published_on = format_date(article['published_on'])
    image_url = article.get('imageurl', '')
    description = body[:150]
    tags = article.get('tags', '').replace('|', ', ')
    author = article.get('author', 'Crypto News')

    # Render article page
    article_template = Template(article_html_template)
    article_html_content = article_template.render(
        title=title,
        url=url,
        body=body,
        published_on=published_on,
        image_url=image_url,
        description=description,
        tags=tags,
        keywords=tags,
        author=author
    )

    # Save article file
    article_file_path = os.path.join(output_dir, f"{article_id}.html")
    with open(article_file_path, 'w', encoding='utf-8') as file:
        file.write(article_html_content)

    all_articles.append({
        'id': article_id,
        'title': title,
        'body': body,
        'image_url': image_url,
        'published_on': published_on
    })

# Generate index page
index_template = Template(index_html_template)
index_html_content = index_template.render(articles=all_articles)

with open('index.html', 'w', encoding='utf-8') as index_file:
    index_file.write(index_html_content)

print("Enhanced HTML files generated successfully!")
