from flask import session, render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')






