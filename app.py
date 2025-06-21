from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('NEWS_API_KEY')

print("Your API Key is:", API_KEY)  # Debug: Should print actual key

app = Flask(__name__)

def fetch_news(category="technology"):
    url = ('https://newsapi.org/v2/top-headlines?'
           f'category={category}&'
           'country=us&'
           'pageSize=15&'
           f'apiKey={API_KEY}')
    print("Fetching URL:", url)  # Debug URL
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())  # Entire API response

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get('articles', [])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_news', methods=['POST'])
def get_news():
    user_input = request.json.get('interests', 'technology')
    print("User input category:", user_input)
    valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

    if user_input not in valid_categories:
        return jsonify({'error': 'Invalid category! Choose: ' + ', '.join(valid_categories)})

    articles = fetch_news(user_input)
    if not articles:
        return jsonify({'error': 'No news articles found.'})
    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
