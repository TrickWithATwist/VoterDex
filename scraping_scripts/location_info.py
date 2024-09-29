from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_precinct_and_county(first_name, last_name, birth_month, birth_year, zip_code):
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # Remove headless mode for visible browser interactions
    # chrome_options.add_argument("--headless")  
    service = Service('/usr/local/bin/chromedriver')
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




# Example usage
# first_name = 'Abbas'
# last_name = 'Fattah'
# birth_month = '4'  # May
# birth_year = '2002'
# zip_code = '48823'

# county, precinct, jurisdiction = get_precinct_and_county(first_name, last_name, birth_month, birth_year, zip_code)
# print(f"County: {county}, Precinct: {precinct}", f"Jurisdiction: {jurisdiction}")
