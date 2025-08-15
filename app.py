# # from flask import Flask, render_template, request, jsonify
# import webbrowser
# import threading
# import urllib.parse
# import logging
# import mysql.connector

# #Configure logging
# logging.basicConfig(level=logging.INFO)

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/search/<platform>', methods=['POST'])
# def search(platform):
#     try:
#         platform = request.args.get('platform', '').strip().lower()
#         query = request.args.get('query', '').strip()

#         # Validate input
#         platform = data.get('platform', '').strip().lower()
#         query = data.get('query', '').strip()

#         if not platform or not query:
#             return jsonify({'error': 'Platform and query cannot be empty'}), 400

#         # Supported platforms
#         platform_urls = {
#             'youtube': 'https://www.youtube.com/results?search_query={}',
#             'google': 'https://www.google.com/search?q={}',
#             'instagram': 'https://www.instagram.com/explore/search/keyword/?q={}'
#         }

#         # Log the search
#         if platform not in platform_urls:
#             return jsonify({'error': f'Unsupported platform: {platform}'}), 400

#         # URL encode the query
#         encoded_query = urllib.parse.quote_plus(query)
#         url = platform_urls[platform].format(encoded_query)

#         logging.info(f"User searched {query} on {platform}")

#         # Open in a new thread to avoid blocking
#         threading.Thread(target=lambda: webbrowser.open(url)).start()

#         return jsonify({
#             'success': True,
#             'message': f'Searching {platform.capitalize()} for: {query}',
#             'url': url
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",     # if you're hosting locally
#         user="root",          # your MySQL username
#         password="", # your MySQL password
#         database="search_app" # database name we just created
#     )

    
# if __name__ == '__main__':
#     app.run( host='0.0.0.0', port=5000)

# from flask import Flask, render_template, request, jsonify
# import webbrowser
# import threading
# import urllib.parse
# import logging
# import mysql.connector

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/search', methods=['POST'])
# def search():
#     try:
#         data = request.get_json()

#         platform = data.get('platform', '').strip().lower()
#         query = data.get('query', '').strip()

#         if not platform or not query:
#             return jsonify({'error': 'Platform and query cannot be empty'}), 400

#         # Supported platforms
#         platform_urls = {
#             'youtube': 'https://www.youtube.com/results?search_query={}',
#             'google': 'https://www.google.com/search?q={}',
#             'instagram': 'https://www.instagram.com/explore/search/keyword/?q={}'
#         }

#         if platform not in platform_urls:
#             return jsonify({'error': f'Unsupported platform: {platform}'}), 400

#         encoded_query = urllib.parse.quote_plus(query)
#         url = platform_urls[platform].format(encoded_query)

#         logging.info(f"User searched '{query}' on {platform}")

#         # Open in browser without blocking
#         threading.Thread(target=lambda: webbrowser.open(url)).start()

#         return jsonify({
#             'success': True,
#             'message': f'Searching {platform.capitalize()} for: {query}',
#             'url': url
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# def get_db_connection():
#     """MySQL connection for local testing"""
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",  # change if you have a password
#         database="search_app"
#     )

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import urllib.parse
import logging
import mysql.connector

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search/<platform>', methods=['POST'])
def search(platform):
    try:
        # Get JSON body
        data = request.get_json()

        # platform comes from URL parameter, but normalize it
        platform = platform.strip().lower()
        query = data.get('query', '').strip()

        if not platform or not query:
            return jsonify({'error': 'Platform and query cannot be empty'}), 400

        # Supported platforms
        platform_urls = {
            'youtube': 'https://www.youtube.com/results?search_query={}',
            'google': 'https://www.google.com/search?q={}',
            'instagram': 'https://www.instagram.com/explore/search/keyword/?q={}'
        }

        if platform not in platform_urls:
            return jsonify({'error': f'Unsupported platform: {platform}'}), 400

        encoded_query = urllib.parse.quote_plus(query)
        url = platform_urls[platform].format(encoded_query)

        logging.info(f"User searched '{query}' on {platform}")

        # Open in browser without blocking
        threading.Thread(target=lambda: webbrowser.open(url)).start()

        return jsonify({
            'success': True,
            'message': f'Searching {platform.capitalize()} for: {query}',
            'url': url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # change if needed
        database="search_app"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
