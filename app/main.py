# app/main.py

from flask import Flask

# Create a new Flask application instance
app = Flask(__name__)

# Define a route for the root URL '/'
@app.route('/')
def hello_world():
    # Return the "Hello, World!" message
    return 'Hello, World!'

# Run the app if the script is executed directly
if __name__ == '__main__':
    # The app will be available on all IP addresses (host='0.0.0.0') and on port 80
    app.run(host='0.0.0.0', port=80)