import json
import os

from flask import current_app as app, render_template, request, Blueprint
from CTFd.plugins import register_plugin_assets_directory

from .module import load_page

PLUGIN_PATH = os.path.dirname(__file__)
with open(f"{PLUGIN_PATH}/config.json", 'r') as fd:
    CONFIG = json.load(fd)


def load(app):
    app.db.create_all()
    register_plugin_assets_directory(app, base_path=f"{PLUGIN_PATH}/assets")
    pages = load_page(CONFIG["route"], PLUGIN_PATH)
    app.register_blueprint(pages)
    print("CTFd GO-CQHTTP plugin is ready!")