from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Setup WebDriver and Wait
# ---------------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

# ---------------------------
# Login and Navigation
# ---------------------------

# Open the initial URL
driver.get("https://vcc.pln.co.id")

# Wait for and click the "Login With SSO" button
login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Login With SSO')]"))
)
login_button.click()

# Wait for the login form to load (userId and password fields)
user_field = wait.until(EC.visibility_of_element_located((By.NAME, "userId")))
password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

# Fill in credentials (note: backslash is escaped)
username = "pusat\\wahyudi.wicaksono"
password = "==OKEje1993"
user_field.send_keys(username)
password_field.send_keys(password)

# Locate and click the submit button
submit_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)
submit_button.click()

# Wait until the URL indicates that the login is complete (contains "dashboard")
wait.until(EC.url_contains("dashboard"))

# Redirect to the Gangguan dashboard
redirect_url = "https://vcc.pln.co.id/dashboard/gangguan"
driver.get(redirect_url)
print(f"Redirected to {redirect_url}")

# ---------------------------
# Wait for Sweet Alert Modal to Hide
# ---------------------------

# Define the locator for the Sweet Alert modal
modal_locator = (By.CSS_SELECTOR, ".sweet-alert.hideSweetAlert")

# Wait until the modal's CSS "display" property is "none"
wait.until(lambda d: d.find_element(*modal_locator).value_of_css_property("display") == "none")
print("Data fetching complete. Sweet alert modal is now hidden.")

# ---------------------------
# Extract Data from Monitoring Section
# ---------------------------

# Locate the monitoring-section element
monitoring_section = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "monitoring-section"))
)

# Find all direct child div elements inside the monitoring section
child_divs = monitoring_section.find_elements(By.XPATH, "./div")

# Define the expected data-key values
expected_keys = {
    "gg_handle",
    "gg_nothandle",
    "gg_nothandle_oversla",
    "gg_open",
    "gg_oversla",
    "gg_selesai_all",
    "gg_selesai_yantek",
    "gg_selesai_plnmobile"
}

# Create a dictionary to store the final result
result = {}

# Process each parent div
for div in child_divs:
    try:
        # Find the anchor text within the "monitoring-head" element
        monitoring_head = div.find_element(By.CLASS_NAME, "monitoring-head")
        anchor = monitoring_head.find_element(By.TAG_NAME, "a")
        parent_name = anchor.text.strip()
    except Exception as e:
        print("Could not find the anchor text in a child div. Skipping this div.", e)
        continue

    # Create a dictionary for the data-key elements within this parent div
    data_dict = {}
    datakey_elements = div.find_elements(By.CSS_SELECTOR, "[data-key]")
    for element in datakey_elements:
        data_key = element.get_attribute("data-key")
        if data_key in expected_keys:
            text_value = element.text.strip()
            # Attempt to convert the value to an integer if possible
            try:
                value = int(text_value)
            except ValueError:
                value = text_value
            data_dict[data_key] = value

    # Store the result using the anchor text as the key
    result[parent_name] = data_dict

# Print the final structured data
print("\nExtracted Monitoring Data:")
for parent, data in result.items():
    print(f"{parent} : {data}")

# ---------------------------
# Cleanup
# ---------------------------
input("\nPress Enter to exit and close the browser...")
driver.quit()
