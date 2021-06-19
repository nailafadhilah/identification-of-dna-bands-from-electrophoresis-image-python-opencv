import os
from flask import Flask, render_template

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
