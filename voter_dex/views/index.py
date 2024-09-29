from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from fuzzywuzzy import fuzz
from googletrans import Translator
import voter_dex
import time

CHROME_DRIVER = '/usr/bin/chromedriver'

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
  try:
    county, precinct, jurisdiction = get_precinct_and_county(first_name, last_name, birth_month, birth_year, zipcode)
    proposals = get_ballot(county, jurisdiction, precinct)
    # translate to Spanish
    # translator = Translator()
    # for proposal in proposals:
    #     proposal['title'] = translator.translate(proposal['title'], dest="es")
    #     proposal['description'] = translator.translate(proposal['description'], dest="es")
    response = dict()
    response['info'] = {'county': county, 'jurisdiction': jurisdiction, 'precinct' : precinct}
    response['proposals'] = {'proposals': proposals}
    return jsonify(**response), 201
  except Exception as e:
    print(e)
    return jsonify({"county": "county", "precinct" : "precinct", "jurisdiction": "jurisdiction"}), 500





def find_and_click_most_similar_option(driver, select_element_id, target_text):
    # Get the dropdown element
    dropdown = Select(driver.find_element(By.ID, select_element_id))
    
    # Iterate over the options and compute similarity
    best_match = None
    highest_score = 0

    for option in dropdown.options:
        option_text = option.text.strip()
        similarity_score = fuzz.ratio(option_text.lower(), target_text.lower())

        # Keep track of the option with the highest similarity score
        if similarity_score > highest_score:
            highest_score = similarity_score
            best_match = option

    if best_match:
        print(f"Best match: {best_match.text} with similarity score: {highest_score}")
        best_match.click()  # Click the best match
    else:
        print("No suitable match found.")

def get_proposals(driver):
    proposals = []

    # Locate the main proposals container
    proposal_section = driver.find_element(By.ID, "proposals")
    
    # Get all proposal titles
    titles = proposal_section.find_elements(By.CLASS_NAME, "proposalTitle")

    for title in titles:
        # Get the text of the proposal title
        title_text = title.text.strip()
        
        # Initialize a list to hold the paragraphs for this proposal
        paragraphs = []
        
        # Start finding sibling elements from the title's next sibling
        siblings = title.find_elements(By.XPATH, './following-sibling::*')
        
        for sibling in siblings:
            # If it's a <p> tag, get the text
            if sibling.tag_name == 'p':
                paragraphs.append(sibling.text.strip())
            # If it's a <br> tag, break the loop
            elif sibling.tag_name == 'br':
                break
            
            # Move to the next sibling
            sibling = sibling.find_element(By.XPATH, './following-sibling::*[1]')

        # Combine the title with its paragraphs and add to proposals
        proposals.append({
            'title': title_text,
            'description': ' '.join(paragraphs)
        })

    return proposals


  
def get_precinct_and_county(first_name, last_name, birth_month, birth_year, zip_code):
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # Remove headless mode for visible browser interactions
    chrome_options.add_argument("--headless")  
    service = Service()
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
    except Exception as error:
        print(error)
        raise Exception()
    finally:
        driver.quit()


def get_ballot(county, jurisdiction, precinct):
    # Configure Selenium WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    service = Service(CHROME_DRIVER)  # Update the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        driver.get('https://mvic.sos.state.mi.us/PublicBallot')  # Replace with the actual URL

        # Wait until the election dropdown is available
        wait = WebDriverWait(driver, 10)
        election_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'Elections')))

        # Select 'State General - 11/5/2024' (value 699) from the election dropdown
        election_select = Select(election_dropdown)
        election_select.select_by_value("699")

        # Wait until county options are populated after the election is selected
        wait.until(lambda driver: len(Select(driver.find_element(By.ID, 'Counties')).options) > 1)

        # Select the most similar county using fuzzy matching
        find_and_click_most_similar_option(driver, "Counties", county)

        # Wait until jurisdiction options are populated after county is selected
        wait.until(lambda driver: len(Select(driver.find_element(By.ID, 'Jurisdictions')).options) > 1)

        # Select the most similar jurisdiction using fuzzy matching
        find_and_click_most_similar_option(driver, "Jurisdictions", jurisdiction)

        # Wait until precinct options are populated after jurisdiction is selected
        wait.until(lambda driver: len(Select(driver.find_element(By.ID, 'WardPrecincts')).options) > 1)

        # Select the most similar precinct using fuzzy matching
        find_and_click_most_similar_option(driver, "WardPrecincts", precinct)

        # Click the "View the ballot" button to submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGenerateBallot')))
        submit_button.click()

        # wait until new page loads
        proposal_section = wait.until(EC.presence_of_element_located((By.ID, 'proposals')))
        # get proprosals
        wait.until(EC.presence_of_element_located((By.ID, 'proposals')))

        # Find the proposals section
        proposals_section = driver.find_element(By.ID, "proposals")

        # Get all child elements within the proposals section
        proposal_elements = proposals_section.find_elements(By.XPATH, "./*")
        # Variables to hold proposal information
        current_title = None
        proposals = []

        current_description = ""
        for element in proposal_elements:
            # If it's a proposal title, start a new proposal
            if 'row' in element.get_attribute("class"):
                # get the class name of its child div
                child_div = element.find_element(By.XPATH, "./*")
                if 'proposalTitle' in child_div.get_attribute("class"):
                    if current_title:
                        # If there's a title and we've collected content, save the proposal
                        proposals.append({
                            "title": current_title,
                            "description": current_description.strip()
                        })
                        current_description = ""
                    # Start a new proposal
                    current_title = child_div.text.strip()
            elif current_title:
                # For other elements (description parts), collect the text
                if element.tag_name == "p" or element.tag_name == "div":
                    current_description += element.text.strip() + "\n"

        # Capture the last proposal if it exists
        if current_title:
            proposals.append({
                "title": current_title,
                "description": current_description.strip()
            })
        print(proposals)
        return proposals


    finally:
        driver.quit()


# first_name = 'Andrew'
# last_name = 'Mahler'
# birth_month = '4'  # April
# birth_year = '2002'
# zip_code = '48823'

# # Retrieve the county, precinct, and jurisdiction
# county, precinct, jurisdiction = get_precinct_and_county(first_name, last_name, birth_month, birth_year, zip_code)

# # # Fill the election form using the retrieved info
# get_ballot(county, jurisdiction, precinct)