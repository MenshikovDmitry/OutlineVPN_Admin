from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from config import WEBSITE_API_URL, PORT
from outline_admin.outline_resource import OutlineResource

import logging
LOG = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app, prefix="/api")

    api.add_resource(OutlineResource, "/outline/<string:cmd>")

    @app.route("/")
    def index():
        # returning the UI web form
        return render_template('index.html', API_URL=WEBSITE_API_URL)

    return app

app = create_app()

if __name__ == "__main__":
    LOG.info(f"Starting the Outline Admin backend.")
    app.run(host="0.0.0.0", port=PORT)