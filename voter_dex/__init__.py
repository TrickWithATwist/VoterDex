import flask;
app = flask.Flask(__name__)
app.config.from_object('voter_dex.config')

import voter_dex.model
from voter_dex.views.index import *
app.add_url_rule('/', view_func=show_index)
