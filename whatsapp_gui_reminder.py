from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
import datetime
import time

# WhatsApp group name and rotating list of people
GROUP_NAME = "Young & Chosen"
PEOPLE = ["Addison", "Cam", "Eli"]

# Calculate person on trash duty for the week
def calculate_person_on_duty():
    today = datetime.date.today()
    weeks_since_start = (today - datetime.date(2024, 11, 14)).days // 7
    return PEOPLE[weeks_since_start % len(PEOPLE)]

# Function to send the WhatsApp message
def send_message():
    # Prepare the message
    person_on_duty = calculate_person_on_duty()
    message = f"IGNORE: {person_on_duty} This is a test automated message."
    
    # Set up Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--user-data-dir=C:/Path/To/Your/Chrome/User/Data")  # Chrome data path

    # Set up Chrome driver
    chrome_service = Service("C:/Users/elijah.opoku-nyarko/Desktop/chromedriver.exe")
    
    try:
        # Initialize the driver
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.get("https://web.whatsapp.com")
        input("Press Enter after scanning the QR code...")  # Wait for manual QR code scan

        # Wait for the search box and enter the group name
        search_box = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys(GROUP_NAME)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)
        
        # Wait for the message box and send the message
        message_box = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p")
            )
        )
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        # Success notification
        messagebox.showinfo("Success", "Message sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        driver.quit()

# Function for manual sending
def manual_send():
    send_message()

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("WhatsApp Reminder by Eli")

tk.Label(root, text="Jesuskid's WhatsApp Reminder ", font=("Helvetica", 16)).pack(pady=10)
tk.Label(root, text=f"Current Group: {GROUP_NAME}").pack(pady=5)

# Message display
reminder_text = f"Reminder will be sent to: {calculate_person_on_duty()}"
label = tk.Label(root, text=reminder_text, font=("Arial", 12))
label.pack(pady=10)

# Manual send button
send_button = tk.Button(root, text="Send Reminder Now", command=manual_send, font=("Arial", 10), bg="green", fg="white")
send_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
