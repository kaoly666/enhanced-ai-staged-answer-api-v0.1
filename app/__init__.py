print("starting __init__...")

from flask import Flask

app = Flask(__name__)

from app import routes
