from flask import Flask, request, jsonify
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


# Post endpoint to receieve user info
@voter_dex.app.route('/user_info', methods=['POST'])
def user_info():
  data = request.get_json()

  first_name = data.get('first_name')
  last_name = data.get('last_name')
  birth_month = data.get('birth_month')
  birth_year = data.get('birth_year')
  zipcode = data.get('zipcode')

  # fetch {county, jurisdiction, precinct}
  
  # if we have county-jursdiction-precinct in our DB else compute and insert into DB

  # fetch info from DB -> 

  print(zipcode)
  return jsonify({"message": "Ayy!"}), 201





# DB functions
def insert_proposal(name, description, proposal_type):
  connection = voter_dex.model.get_db()
  
  cur = connection.execute('''
      INSERT INTO proposals (name, description, type) 
      VALUES (?, ?, ?);
  ''', (name, description, proposal_type))
  
  # Commit the changes and close the connection
  print(f"Proposal '{name}' inserted successfully.")

def get_proposal(name):
  connection = voter_dex.model.get_db()
  cur = connection.execute('''
        SELECT * FROM proposals 
        WHERE name = ?;
    ''', (name,))
  proposal = cur.fetchone()
  if proposal:
    return {
        'id': proposal[0],
        'name': proposal[1],
        'description': proposal[2],
        'type': proposal[3]
    }
  else:
    return None