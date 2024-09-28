import flask
import voter_dex


@voter_dex.app.route('/')
def show_index():
  connection = voter_dex.model.get_db()
  cur = connection.execute(
    "SELECT name, affiliation FROM candidate ORDER BY id DESC LIMIT 1"
  )
  ppl = cur.fetchall()
  context = {"ppl": ppl}
  return flask.jsonify(**context)

@voter_dex.app.route('/user_info', methods=['POST'])
def user_info():
  data = request.get_json()

  first_name = data.get('first_name')
  last_name = data.get('last_name')
  birth_month = data.get('birth_month')
  birth_year = data.get('birth_year')
  zipcode = data.get('zipcode')

  print(zipcode)
  