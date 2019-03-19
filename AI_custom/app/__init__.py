from flask import Flask
app = Flask(__name__)
from app import sockets
from app import views