from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import platform  # To detect the operating system

def scrape_donations():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Determine the correct ChromeDriver file based on OS
    if platform.system() == "Windows":
        driver_path = "chromedriver.exe"
    else:  # For Linux, macOS, or others
        driver_path = "chromedriver"
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.doearenacorinthians.com.br/"
    driver.get(url)

    time.sleep(3)  # Wait for the page to load
    
    try:
        # Scrape the donation and goal values
        donation_element = driver.find_element(By.CLASS_NAME, "goal-raised__moment")
        donation_value = donation_element.text.strip()
        
        goal_element = driver.find_element(By.CSS_SELECTOR, "p.goal-raised__mark b")
        goal_value = goal_element.text.strip()
        
        return donation_value, goal_value
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    finally:
        driver.quit()

# Uncomment for testing
# print(scrape_donations())
