import flask;
from flask_cors import CORS

app = flask.Flask(__name__)
app.config.from_object('voter_dex.config')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

import voter_dex.model
from voter_dex.views.index import *
app.add_url_rule('/', view_func=show_index)
