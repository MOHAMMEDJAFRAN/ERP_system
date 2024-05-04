from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()  # You can set the path if not in PATH
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to become available

# Navigate to your Streamlit application
driver.get('http://localhost:8501')  # Change the URL if hosted elsewhere

def test_data_ingestion():
    try:
        # Find and interact with file uploader
        file_input = driver.find_element(By.XPATH, '//*[@data-baseweb="file-uploader"]')
        file_input.send_keys('/path/to/your/test/data.csv')  # Provide the absolute path to the test file

        # Wait for file to be uploaded and processed
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'stMarkdown'),  # Assuming the confirmation message is in a Markdown element
                'Data ingestion successful.'
            )
        )

        print("Data ingestion test passed.")
    except Exception as e:
        print(f"Data ingestion test failed: {e}")

def test_module_processing():
    try:
        # Select a module from the sidebar dropdown
        module_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@data-baseweb="select-input"]'))
        )
        module_select.click()

        # Choose 'Finance' module for example
        finance_module = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Finance')]"))
        )
        finance_module.click()

        # Click the 'Analyze' button
        analyze_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze')]")
        analyze_button.click()

        # Verify that the data is processed and displayed
        result_data = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'stDataFrame'))
        )

        print("Module processing test passed.")
    except Exception as e:
        print(f"Module processing test failed: {e}")

# Close the browser after testing
driver.quit()

