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
url = "file:///C:/Users/Lenovo/Downloads/assignment%20for%20qa/assets/checkout.html"
driver.get(url)

# Enter valid discount code
discount_code_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "discount-code"))
)
discount_code_input.send_keys("SAVE15")

# Apply discount
apply_discount_button = driver.find_element(By.ID, "apply-discount")
apply_discount_button.click()

# Verify discount message
discount_message = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "discount-message"))
)
assert "15% Discount Applied!" in discount_message.text
assert "green" in discount_message.get_attribute("style")

# Verify total price
total_price_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "total-price"))
)
expected_total = 210.80  # 248.00 * 0.85
assert float(total_price_element.text) == round(expected_total, 2)

# Close the browser and print the result
print("✅ Test Passed!")
time.sleep(5)
driver.quit()