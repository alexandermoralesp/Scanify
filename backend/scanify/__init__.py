# Import libraries for api
from distutils.log import debug
import os
from flask import Flask

from . import api

def scanify_app(test_config = None):
    # Declare main app
    scanify = Flask(__name__, instance_relative_config=True)
    @scanify.get("/")
    def index():
        return "<h1> Hello index </h1>"
    # scanify.register_blueprint(blog.blog, url_prefix= '/blog')
    scanify.register_blueprint(api.api, url_prefix= '/api')
    return scanify

scanify = scanify_app()
