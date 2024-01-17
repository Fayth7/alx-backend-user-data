# api/v1/views.py
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

# Now you can define your routes using app_views, for example:
@app_views.route('/example', methods=['GET'])
def example_route():
    return "Hello, this is an example route!"
