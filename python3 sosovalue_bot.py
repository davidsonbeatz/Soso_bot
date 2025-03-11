from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)

# SoSoValue Referral Signup URL
signup_url = "https://sosovalue.com/join/B6I263JQ"

# FakeMailGenerator URL
temp_mail_url = "http://www.fakemailgenerator.com/"

# Function to get a temporary email
def get_temp_email():
    driver.get(temp_mail_url)
    time.sleep(3)
    email_elem = driver.find_element(By.ID, "email")
    return email_elem.get_attribute("value")

# Function to sign up on SoSoValue
def signup(email):
    driver.get(signup_url)
    time.sleep(3)
    
    # Fill email field
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)

    # Fill password fields
    password_field = driver.find_element(By.NAME, "password")
    confirm_password_field = driver.find_element(By.NAME, "confirmPassword")
    
    password_field.send_keys("Loginanddie@1")
    confirm_password_field.send_keys("Loginanddie@1")

    # Solve CAPTCHA (manual or using service)
    input("Solve the CAPTCHA and press Enter...")  # Manual step
    
    # Submit the form
    signup_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    signup_button.click()
    time.sleep(5)

# Function to get verification code from temp mail
def get_verification_code():
    driver.get(temp_mail_url)
    time.sleep(5)
    
    # Open the latest email
    try:
        email_list = driver.find_elements(By.CSS_SELECTOR, ".email_list_item")
        email_list[0].click()
        time.sleep(3)
        
        # Extract the verification code (Assuming it's a 6-digit code in email)
        email_body = driver.find_element(By.ID, "email_body").text
        verification_code = ''.join(filter(str.isdigit, email_body))  # Extract numbers
        return verification_code
    except Exception as e:
        print("Error fetching verification code:", e)
        return None

# Function to complete verification
def complete_verification(verification_code):
    driver.get(signup_url)
    time.sleep(3)
    
    code_field = driver.find_element(By.NAME, "verification_code")
    code_field.send_keys(verification_code)

    verify_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    verify_button.click()
    time.sleep(3)

# Main function to automate multiple referrals
def run_bot(referrals=50):
    for i in range(referrals):
        print(f"Processing referral {i+1}...")
        email = get_temp_email()
        signup(email)
        
        verification_code = get_verification_code()
        if verification_code:
            complete_verification(verification_code)
            print(f"Referral {i+1} completed!")
        else:
            print(f"Failed to complete referral {i+1}.")
        
        time.sleep(10)  # Delay before next signup

    driver.quit()

# Run the bot for 50 referrals
run_bot(referrals=50)