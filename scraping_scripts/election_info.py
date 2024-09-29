from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import location_info
import time

from selenium.webdriver.support.ui import Select
from fuzzywuzzy import fuzz

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

# Example usage
target_text = "City Of East Lansing"
find_and_click_most_similar_option(driver, "Jurisdictions", target_text)


def fill_election_form():
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # Remove headless mode for visible browser interactions
    # chrome_options.add_argument("--headless")  
    service = Service('/usr/local/bin/chromedriver')  # Update the path to your chromedriver
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

        # Select a county (e.g., 'Ingham County', value 33)
        county_select = Select(driver.find_element(By.ID, 'Counties'))
        county_select.select_by_value("1")  # Replace "33" with the desired county's value

        # Wait until jurisdiction options are populated after county is selected
        wait.until(lambda driver: len(Select(driver.find_element(By.ID, 'Jurisdictions')).options) > 1)

        # Select a jurisdiction (e.g., 'Meridian Township', value 123) after it appears
        jurisdiction_select = Select(driver.find_element(By.ID, 'Jurisdictions'))
        jurisdiction_select.select_by_value("1")  # Replace "123" with the desired jurisdiction's value

        # Wait until precinct options are populated after jurisdiction is selected
        wait.until(lambda driver: len(Select(driver.find_element(By.ID, 'WardPrecincts')).options) > 1)

        # Select a precinct (e.g., 'Precinct 1', value 1) after it appears
        precinct_select = Select(driver.find_element(By.ID, 'WardPrecincts'))
        precinct_select.select_by_value("00001")  # Replace "1" with the desired precinct's value

        # Click the "View the ballot" button to submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGenerateBallot')))
        submit_button.click()

        # Optionally, you can add a wait for the page to load after submission
        time.sleep(15)  # Adjust the wait time as needed
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Adjust based on the next step

    finally:
        driver.quit()

# Call the function to execute the form-filling process
fill_election_form()
