from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_grand_challenges():
    driver_path = "C:/Users/christopher.thomasen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.grandchallenges.ca/funding-opportunities/"
    driver.get(url)

    # Wait for the page to load fully
    time.sleep(5)

    funding_list = []

    try:
        # Wait until the sections with the class 'page-builder-highlight-box' are loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-builder-highlight-box'))
        )

        # Find all sections with the class 'page-builder-highlight-box'
        sections = driver.find_elements(By.CLASS_NAME, 'page-builder-highlight-box')
        print(f"Number of sections found: {len(sections)}")

        for section in sections:
            try:
                # Extract the header (h2 or h3) or the relevant heading if available
                try:
                    header = section.find_element(By.TAG_NAME, 'header').text.strip()
                except:
                    header = "No title available"

                # Extract any description (paragraphs inside the section)
                description = section.find_elements(By.TAG_NAME, 'p')
                description_text = " ".join([p.text.strip() for p in description])

                # Print for debugging and add to the list
                print(f"Header: {header}, Description: {description_text}")
                funding_list.append({"Header": header, "Description": description_text})

            except Exception as e:
                print(f"Error processing section: {e}")
                continue

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return funding_list

def main():
    # Scrape grand challenges data
    grand_challenges_data = scrape_grand_challenges()

    # Create a DataFrame
    df = pd.DataFrame(grand_challenges_data)
    print(df)

    # Optionally save to CSV
    df.to_csv("grand_challenges_funding_opportunities.csv", index=False)


if __name__ == "__main__":
    main()
