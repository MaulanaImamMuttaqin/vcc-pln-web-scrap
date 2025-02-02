from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (Chrome)
driver = webdriver.Chrome()

# Create a WebDriverWait instance with a 30-second timeout (adjust as needed)
wait = WebDriverWait(driver, 30)

# Open the initial URL
driver.get("https://vcc.pln.co.id")

# Wait until the "Login With SSO" button is clickable and click it
login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Login With SSO')]"))
)
login_button.click()

# Wait for the login form to load by waiting for the 'userId' input field to be visible
user_field = wait.until(EC.visibility_of_element_located((By.NAME, "userId")))
password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

# Fill in the login form credentials
username = "pusat\\wahyudi.wicaksono"  # Note: backslash is escaped
password = "==OKEje1993"
user_field.send_keys(username)
password_field.send_keys(password)

# Locate and click the submit button (assuming it is a <button> with type="submit")
submit_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)
submit_button.click()

# Wait until the login process is complete (e.g., URL contains "dashboard")
wait.until(EC.url_contains("dashboard"))

# Redirect to the Gangguan dashboard URL
redirect_url = "https://vcc.pln.co.id/dashboard/gangguan"
driver.get(redirect_url)
print(f"Redirected to {redirect_url}")

# Define a locator for the sweet alert modal
modal_locator = (By.CSS_SELECTOR, ".sweet-alert.hideSweetAlert")

# Wait until the modal's CSS "display" property becomes "none"
# This lambda function retrieves the element and checks its display property.
wait.until(lambda d: d.find_element(*modal_locator).value_of_css_property("display") == "none")
print("Data fetching complete. Sweet alert modal is now hidden.")

# Keep the browser open until you press Enter
input("Press Enter to exit and close the browser...")

# Clean up and close the browser
driver.quit()
