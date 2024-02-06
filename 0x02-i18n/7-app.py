#!/usr/bin/env python3
"""asic Flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from pytz.exceptions import UnknownTimeZoneError
app = Flask(__name__)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Has a LANGUAGES class attribute"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user(user_id):
    """Returns a user dictionary or None if the ID cannot
    be found or if login_as was not passed"""
    if user_id:
        return users.get(user_id)
    else:
        return None


@app.before_request
def before_request():
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None

@babel.localeselector
def get_locale():
    """determine the best match with our supported languages"""
    locale_param = request.args.get('locale')
    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """get_timezone function"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

        if g.user and 'timezone' in g.user:
            try:
                pytz.timezone(g.user['timezone'])
                return g.user['timezone']
            except UnknownTimeZoneError:
                pass

        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """html template"""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(debug=True)
