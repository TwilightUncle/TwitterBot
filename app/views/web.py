from flask import Blueprint

app = Blueprint('web', __name__)

@app.route("/index")
def index():
    return "Hello from web.py"
