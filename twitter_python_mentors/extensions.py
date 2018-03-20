# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

import os
import json
import subprocess

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()


class PatchedWebpack(Webpack):

    def _load_webpack_stats(self, app):
        webpack_stats = app.config['WEBPACK_MANIFEST_PATH']
        if not webpack_stats:
            raise RuntimeError(
                'Flask-Webpack requires that WEBPACK_MANIFEST_PATH be specified '
                'as a config option to the Flask app.'
            )
        full_path = os.path.join(app.root_path, webpack_stats)
        if not os.path.exists(full_path):
            # Need to manually run webpack on the parent dir of app.root_path
            pwd = os.curdir
            project_dir = os.path.dirname(os.path.abspath(app.root_path))
            os.chdir(project_dir)
            try:
                subprocess.check_call(['npm', 'run-script', 'build'])
            finally:
                os.chdir(pwd)
        if not os.path.exists(full_path):
            raise RuntimeError(
                'Flask-Webpack requires that WEBPACK_MANIFEST_PATH reference a'
                'valid JSON file.  The path given does not exist: {}'
                .format(full_path)
            )
        try:
            with open(full_path, 'r') as webpack_file:
                return json.load(webpack_file)
        except ValueError as err:
            raise RuntimeError(
                'The webpack manifest file at {} specified by the '
                'WEBPACK_MANIFEST_PATH option does not contain value JSON: {}'
                .format(full_path, err)
            )

    def _set_asset_paths(self, app):
        stats = self._load_webpack_stats(app)
        if app.config['WEBPACK_ASSETS_URL']:
            self.assets_url = app.config['WEBPACK_ASSETS_URL']
        else:
            self.assets_url = stats['publicPath']
        self.assets = stats['assets']


webpack = PatchedWebpack()
