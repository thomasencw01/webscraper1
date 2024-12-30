from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

# Scraping from Convergence Finance
def scrape_convergence_finance():
    driver_path = "C:/Users/christopher.thomasen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.convergence.finance/design-funding#funding-windows"
    driver.get(url)

    funding_list = []

    try:
        # Wait until all window boxes are loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'window-box'))
        )

        # Collect all window boxes at once
        window_boxes = driver.find_elements(By.CLASS_NAME, 'window-box')
        print(f"Number of window boxes found: {len(window_boxes)}")

        for window_box in window_boxes:
            try:
                # Extract title from the h6 element
                h6_tag = window_box.find_element(By.TAG_NAME, 'h6')
                title = h6_tag.text.strip()

                # Extract the description containing the deadline information
                try:
                    description_div = window_box.find_element(By.CLASS_NAME, 'window-description')
                    description_text = description_div.text.strip()

                    # Check if there is an actual deadline in the description
                    if "Application Deadline" in description_text:
                        deadline_text = description_text.split("Application Deadline")[-1].strip()
                    else:
                        deadline_text = "More info to come"
                except:
                    deadline_text = "More info to come"

                # Attempt to parse the deadline as a date
                try:
                    deadline = datetime.strptime(deadline_text, "%d %b %Y")  # Example format: "23 Nov 2024"
                    print(f"Title: {title}, Deadline: {deadline_text}")
                    funding_list.append({"Title": title, "Deadline": deadline_text})
                except ValueError:
                    # If it cannot be parsed as a date, skip this window
                    print(f"Skipping non-date deadline: {deadline_text}")
                    continue

            except Exception as e:
                print(f"Error processing window box: {e}")
                continue  # Continue to the next window box even if there's an error

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return funding_list

# Scraping from Grand Challenges
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

# Main function to combine both scrapes and output to an Excel file
def main():
    # Scrape convergence finance data
    convergence_finance_data = scrape_convergence_finance()
    convergence_df = pd.DataFrame(convergence_finance_data)
    
    # Scrape grand challenges data
    grand_challenges_data = scrape_grand_challenges()
    grand_challenges_df = pd.DataFrame(grand_challenges_data)

    # Save both DataFrames to different sheets in one Excel file
    with pd.ExcelWriter("funding_opportunities_combined.xlsx") as writer:
        convergence_df.to_excel(writer, sheet_name="Convergence Finance", index=False)
        grand_challenges_df.to_excel(writer, sheet_name="Grand Challenges", index=False)

    print("Data saved to funding_opportunities_combined.xlsx")

if __name__ == "__main__":
    main()
