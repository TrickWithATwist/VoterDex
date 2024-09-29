from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_proposals():
    # Configure Selenium WebDriver options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable if you want to run in headless mode
    service = Service('/usr/local/bin/chromedriver')  # Update the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        driver.get('https://mvic.sos.state.mi.us/PublicBallot')  # Replace with the actual URL

        # Wait for the proposals section to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'proposals')))

        # Find all proposal rows
        proposal_sections = driver.find_elements(By.CSS_SELECTOR, "#proposals .row")

        proposals = []
        skip_keywords = ['County', 'City', 'Authority']

        for i, section in enumerate(proposal_sections):
            # Get the text of the current section
            section_text = section.text.strip()

            # Skip sections that contain keywords like "County", "City", or "Authority"
            if any(keyword in section_text for keyword in skip_keywords):
                continue

            # Check if the current section contains a proposal title
            if 'proposalTitle' in section.get_attribute("class"):
                proposal_title = section_text

                # Get the next sibling paragraph for the description (p tag)
                next_section = proposal_sections[i + 1]
                description = next_section.find_element(By.TAG_NAME, 'p').text

                # Store the proposal and its description
                proposals.append({
                    'title': proposal_title,
                    'description': description
                })

        # Print the proposals
        for proposal in proposals:
            print(f"Title: {proposal['title']}")
            print(f"Description: {proposal['description']}\n")

    finally:
        driver.quit()

# Call the function to execute the proposal extraction
extract_proposals()
