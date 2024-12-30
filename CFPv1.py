from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

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
                    # Check if the deadline contains a recognizable date format
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

def main():
    convergence_finance_data = scrape_convergence_finance()

    # Create a DataFrame
    df = pd.DataFrame(convergence_finance_data)
    print(df)

    # Optionally save to CSV
    df.to_csv("convergence_funding_opportunities.csv", index=False)

if __name__ == "__main__":
    main()
