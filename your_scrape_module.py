import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Scraping function for Convergence Finance
def scrape_convergence_finance():
    driver_path = "C:/Users/christopher.thomasen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.convergence.finance/design-funding#funding-windows"
    driver.get(url)

    funding_list = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'window-box')))
        window_boxes = driver.find_elements(By.CLASS_NAME, 'window-box')
        print(f"Number of window boxes found: {len(window_boxes)}")

        for window_box in window_boxes:
            try:
                h6_tag = window_box.find_element(By.TAG_NAME, 'h6')
                title = h6_tag.text.strip()

                try:
                    description_div = window_box.find_element(By.CLASS_NAME, 'window-description')
                    description_text = description_div.text.strip()
                    if "Application Deadline" in description_text:
                        deadline_text = description_text.split("Application Deadline")[-1].strip()
                    else:
                        deadline_text = "More info to come"
                except:
                    deadline_text = "More info to come"

                try:
                    deadline = datetime.strptime(deadline_text, "%d %b %Y")
                    funding_list.append({
                        "Title": title,
                        "Deadline": deadline_text,
                        "Source": url  # Add the source URL
                    })
                except ValueError:
                    print(f"Skipping non-date deadline: {deadline_text}")
                    continue
            except Exception as e:
                print(f"Error processing window box: {e}")
                continue
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return funding_list

# Scraping function for Grand Challenges
def scrape_grand_challenges():
    driver_path = "C:/Users/christopher.thomasen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.grandchallenges.ca/funding-opportunities/"
    driver.get(url)

    time.sleep(5)
    funding_list = []

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-builder-highlight-box')))
        sections = driver.find_elements(By.CLASS_NAME, 'page-builder-highlight-box')
        print(f"Number of sections found: {len(sections)}")

        for section in sections:
            try:
                try:
                    header = section.find_element(By.TAG_NAME, 'header').text.strip()
                except:
                    header = "No title available"

                description = section.find_elements(By.TAG_NAME, 'p')
                description_text = " ".join([p.text.strip() for p in description])

                funding_list.append({
                    "Title": header,
                    "Description": description_text,
                    "Source": url  # Add the source URL
                })

            except Exception as e:
                print(f"Error processing section: {e}")
                continue
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return funding_list

# Combine and save both datasets
def save_combined_data():
    # Scrape both datasets
    convergence_finance_data = scrape_convergence_finance()
    grand_challenges_data = scrape_grand_challenges()

    # Convert lists of dicts to DataFrames
    df_convergence = pd.DataFrame(convergence_finance_data)
    df_grand_challenges = pd.DataFrame(grand_challenges_data)

    # Combine both DataFrames
    combined_df = pd.concat([df_convergence, df_grand_challenges], ignore_index=True)

    # Save combined data to an Excel file
    combined_df.to_excel("funding_opportunities_combined.xlsx", index=False)
