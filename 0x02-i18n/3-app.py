#!/usr/bin/env python3
"""asic Flask app"""
from flask import Flask, render_template, request
from flask_babel import Babel, _
app = Flask(__name__)
babel = Babel(app)


class Config:
    """Has a LANGUAGES class attribute"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """determine the best match with our supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """html jinja template"""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(debug=True)
