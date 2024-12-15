from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_donations():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service("chromedriver.exe") 
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.doearenacorinthians.com.br/"
    driver.get(url)

    time.sleep(3)
    
    try:
        donation_element = driver.find_element(By.CLASS_NAME, "goal-raised__moment")
        donation_value = donation_element.text.strip()
        
        goal_element = driver.find_element(By.CSS_SELECTOR, "p.goal-raised__mark b")
        goal_value = goal_element.text.strip()
        
        return donation_value, goal_value
    except Exception as e:
        return None, None
    finally:
        driver.quit()

# print(scrape_donations())