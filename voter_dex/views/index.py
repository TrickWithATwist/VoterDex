from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import voter_dex
import time

# 129.0.6668.70

CHROME_DRIVER = '/home/andrew/chromedriver-linux64/chromedriver'

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
  county, precinct, jurisdiction = get_precinct_and_county(first_name, last_name, birth_month, birth_year, zipcode)
  
  # 

  # fetch info from DB -> 

  print(zipcode)
  return jsonify({"county": county, "precinct" : precinct, "jurisdiction": jurisdiction}), 201





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
  
def get_precinct_and_county(first_name, last_name, birth_month, birth_year, zip_code):
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # Remove headless mode for visible browser interactions
    # chrome_options.add_argument("--headless")  
    service = Service(CHROME_DRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        driver.get('https://mvic.sos.state.mi.us/Voter/Index#registeredVoter')

        # Fill out the form fields
        driver.find_element(By.ID, 'FirstName').send_keys(first_name)  # Input First Name
        driver.find_element(By.ID, 'LastName').send_keys(last_name)  # Input Last Name
        
        # Select birth month from the dropdown
        birth_month_select = Select(driver.find_element(By.ID, 'NameBirthMonth'))
        birth_month_select.select_by_value(str(birth_month))  # Select birth month as value (1-12)
        
        # Enter birth year and zip code
        driver.find_element(By.ID, 'NameBirthYear').send_keys(birth_year)  # Input Birth Year
        driver.find_element(By.ID, 'ZipCode').send_keys(zip_code)  # Input Zip Code

        # Submit the form by finding the proper submit button element
        submit_button = driver.find_element(By.XPATH, "//form[@id='name-Form']//button[@type='submit']")
        submit_button.click()

        # Wait for the result page to load and for any element that contains "precinct" to appear
        wait = WebDriverWait(driver, 20)  # Increase wait time if necessary
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Precinct'))

        # Extract the county and precinct information
        county = driver.find_element(By.ID, 'lblCountyName').text  # Extract County Name
        precinct = driver.find_element(By.ID, 'lblPrecinctNumber').text  # Extract Precinct Number
        jurisdiction = driver.find_element(By.ID, 'lblJurisdName').text  # Extract Precinct Number

        return county, precinct, jurisdiction

    finally:
        driver.quit()


def get_ballot_types(county, jurisdiction, precinct: int):
    """
    Precint: int
    """
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # Remove headless mode for visible browser interactions
    # chrome_options.add_argument("--headless")  
    service = Service(CHROME_DRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        driver.get('https://mvic.sos.state.mi.us/PublicBallot/Index')
        # Do dropdowns
        election_select = Select(driver.find_element(By.ID, 'Elections'))
        # <option value="699">State General - 11/5/2024</option>
        election_select.select_by_value('699')
        
        time.sleep(1)
        county_
        county_select = Select(driver.find_element(By.ID, 'Counties'))
        # <option value="699">State General - 11/5/2024</option>
        # county_select.select_by_visible_text(county)
        county_select.select_by_value(county)

        time.sleep(1)
        jurisd = Select(driver.find_element(By.ID, 'Jurisdictions'))
        # <option value="699">State General - 11/5/2024</option>
        jurisd.select_by_visible_text(jurisdiction)

        time.sleep(1)
        # get precinct
        p = Select(driver.find_element(By.ID, 'Precincts'))
        p.select_by_visible_text(f"Precinct {precinct}")

        
        # driver.find_element(By.ID, 'LastName').send_keys(last_name)  # Input Last Name
        
        # # Select birth month from the dropdown
        # birth_month_select = Select(driver.find_element(By.ID, 'NameBirthMonth'))
        # birth_month_select.select_by_value(str(birth_month))  # Select birth month as value (1-12)
        
        # # Enter birth year and zip code
        # driver.find_element(By.ID, 'NameBirthYear').send_keys(birth_year)  # Input Birth Year
        # driver.find_element(By.ID, 'ZipCode').send_keys(zip_code)  # Input Zip Code

        # # Submit the form by finding the proper submit button element
        # submit_button = driver.find_element(By.XPATH, "//form[@id='name-Form']//button[@type='submit']")
        # submit_button.click()

        # # Wait for the result page to load and for any element that contains "precinct" to appear
        # wait = WebDriverWait(driver, 20)  # Increase wait time if necessary
        # wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Precinct'))

        # # Extract the county and precinct information
        # county = driver.find_element(By.ID, 'lblCountyName').text  # Extract County Name
        # precinct = driver.find_element(By.ID, 'lblPrecinctNumber').text  # Extract Precinct Number
        # jurisdiction = driver.find_element(By.ID, 'lblJurisdName').text  # Extract Precinct Number

        print(election_select)

    finally:
        driver.quit()


get_ballot_types("Ingham County", "City Of East Lansing", 3)