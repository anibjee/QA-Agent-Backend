import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the HTML file
# Update the URL to the path of your local HTML file
driver.get("file:///C:/Users/Lenovo/Downloads/assignment%20for%20qa/assets/checkout.html")

# Wait for the discount code input field to be visible
discount_code_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "discount-code"))
)

# Enter an invalid discount code
discount_code_input.send_keys("INVALIDCODE")

# Click the apply discount button
apply_discount_button = driver.find_element(By.ID, "apply-discount")
apply_discount_button.click()

# Wait for the discount message to be visible
discount_message = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "discount-message"))
)

# Verify the discount message
assert "Invalid Code" in discount_message.text
assert "red" in discount_message.get_attribute("style")

# Verify the total price
total_price = driver.find_element(By.ID, "total-price")
assert float(total_price.text) == round(248.00, 2)

print("✅ Test Passed!")
time.sleep(5)
driver.quit()