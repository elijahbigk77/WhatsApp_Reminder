from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# WhatsApp group name and rotating list of people
GROUP_NAME = "Young & Chosen"
PEOPLE = ["Addison", "Cam", "Eli"]

# Calculate the current week's person on trash duty
today = datetime.date.today()
weeks_since_start = (today - datetime.date(2024, 11, 14)).days // 7
person_on_duty = PEOPLE[weeks_since_start % len(PEOPLE)]
message = f"Reminder: {person_on_duty} is on trash duty this week."

# Set up Selenium and open WhatsApp Web
chrome_service = Service("C:/Users/elijah.opoku-nyarko/Desktop/chromedriver.exe")
driver = webdriver.Chrome(service=chrome_service)
driver.get("https://web.whatsapp.com")
input("Press Enter after scanning the QR code...")

# Wait until WhatsApp Web has loaded
time.sleep(10)
                                                                                                                            
# Search for the group chat
search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
search_box.click()
search_box.send_keys(GROUP_NAME)
time.sleep(3)  # Added a small delay to ensure the group has time to appear in the search
search_box.send_keys(Keys.ENTER)

# Wait for the chat to open and the message input box to be visible
time.sleep(5)  # Wait a bit longer for the chat window to load

# Wait until the message input box is loaded and interactable
message_box = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p")
    )
)

# Send the message
message_box.click()
message_box.send_keys(message)
message_box.send_keys(Keys.ENTER)

# Close the driver
time.sleep(2)
driver.quit()

