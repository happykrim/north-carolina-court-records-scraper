# # # ==================
# # # Imports & Setup
# # # ==================
# ----------------------------------------------------------------------------------
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
# ----------------------------------------------------------------------------------
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, ElementClickInterceptedException, ElementNotInteractableException
# ----------------------------------------------------------------------------------
from selenium.webdriver.common.keys import Keys
# ----------------------------------------------------------------------------------
import random
# ----------------------------------------------------------------------------------
import time
# ----------------------------------------------------------------------------------
import os
# ----------------------------------------------------------------------------------
import csv

# # # ==================
# # # Main Functions
# # # ==================
# ----------------------------------------------------------------------------------
# WebDriver Setup Function
def get_chrome_driver(headless=False):
    """
    Creates and returns a new undetected Chrome driver instance with stealth and incognito mode.
    
    Args:
        headless (bool): Whether to run Chrome in headless mode.

    Returns:
        uc.Chrome: A configured undetected Chrome driver instance.
    """
    options = uc.ChromeOptions()

    # Stealth features (most handled by uc internally)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")

    # User-Agent spoofing
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    # Headless settings
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    else:
        options.add_argument("--start-maximized")

    # Create and return the Chrome driver
    driver = uc.Chrome(options=options, use_subprocess=True, version_main=145)

    if not headless:
        driver.set_window_size(1280, 800)

    return driver

# ----------------------------------------------------------------------------------
# Webpage Interactions
def wait_and_click(driver, object_xpath, timeout=15):
    """
    Waits for an element to become visible and clickable, then clicks it.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        object_xpath (str): The XPath string of the element to click.
        timeout (int): Maximum time to wait for the element (in seconds). Default is 15 seconds.

    Raises:
        TimeoutException: If the element is not found within the timeout period.
        Exception: If the element is found but could not be clicked.
    """
    try:
        # Wait until the element is visible and clickable
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, object_xpath))
        )
        element.click()
        print(f"Clicked element: {object_xpath}")
    except Exception as e:
        print(f"Failed to click element '{object_xpath}': {e}")

# ----------------------------------------------------------------------------------
# reCAPTCHA Handling
def wait_and_click_recaptcha(driver, object_xpath, timeout=15):
    """
    Waits for the reCAPTCHA checkbox to become visible and clickable,
    then simulates a natural, human-like click on it.
    Args:
        driver (webdriver): The Selenium WebDriver instance, already switched
                            into the reCAPTCHA iframe.
        object_xpath (str): The XPath string of the element to click.
        timeout (int): Maximum time to wait for the element (in seconds). Default is 15.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, object_xpath))
        )
        print(f"reCAPTCHA checkbox found: {object_xpath}")

        # Scroll element into view smoothly
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(0.4, 0.8))

        # Get element's position on screen to calculate a safe nearby starting point
        location = element.location
        size = element.size
        elem_x = location['x'] + size['width'] / 2
        elem_y = location['y'] + size['height'] / 2

        # Move to a safe nearby point RELATIVE to the element (not absolute viewport coords)
        actions = ActionChains(driver)
        actions.move_to_element(element)                      # First anchor to the element safely
        actions.move_by_offset(                               # Then nudge slightly from it
            random.randint(-15, 15),
            random.randint(-10, 10)
        )
        actions.pause(random.uniform(0.3, 0.6))
        actions.move_to_element(element)                      # Glide back to the element
        actions.pause(random.uniform(0.3, 0.7))               # Human hesitation before click
        actions.perform()

        # Final click with slight off-center offset to mimic natural human click
        actions2 = ActionChains(driver)
        actions2.move_to_element_with_offset(
            element,
            random.randint(-5, 5),
            random.randint(-3, 3)
        )
        actions2.pause(random.uniform(0.1, 0.3))
        actions2.click()
        actions2.perform()

        print(f"Clicked element: {object_xpath}")

    except Exception as e:
        print(f"Failed to click element '{object_xpath}': {e}")
        raise

# Dropdown Handling
def select_dropdown_option(driver, dropdown_xpath, option_text, timeout=15):
    """
    Waits for a dropdown <select> element to become available, then selects
    an option by its visible text.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        dropdown_xpath (str): XPath of the dropdown <select> element.
        option_text (str): Visible text of the option to select.
        timeout (int): Maximum time to wait for the dropdown (in seconds). Default is 15.

    Returns:
        bool: True if selection succeeded, False otherwise.
    """
    try:
        dropdown_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, dropdown_xpath))
        )

        select = Select(dropdown_element)
        select.select_by_visible_text(option_text)

        print(f"Selected option '{option_text}' from dropdown: {dropdown_xpath}")
        return True

    except Exception as e:
        print(f"Failed to select option '{option_text}' from dropdown '{dropdown_xpath}': {e}")
        return False

def get_dropdown_options(driver, dropdown_xpath, timeout=15, include_empty=False):
    """
    Waits for a dropdown <select> element, extracts all option texts,
    and returns them as a Python list.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        dropdown_xpath (str): XPath of the dropdown <select> element.
        timeout (int): Maximum time to wait for the dropdown (in seconds). Default is 15.
        include_empty (bool): Whether to include empty options. Default is False.

    Returns:
        list: A list of dropdown option texts.
    """
    try:
        dropdown_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, dropdown_xpath))
        )

        select = Select(dropdown_element)
        options = []

        for option in select.options:
            option_text = option.text.strip()

            if option_text or include_empty:
                options.append(option_text)

        print(f"Extracted {len(options)} options from dropdown: {dropdown_xpath}")
        return options

    except Exception as e:
        print(f"Failed to extract options from dropdown '{dropdown_xpath}': {e}")
        return []
# ----------------------------------------------------------------------------------
# Date Input Handling
def enter_date_in_input(driver, input_xpath, date_value, timeout=15, clear_first=True, click_first=True):
    """
    Waits for a date input field to become available, then enters the given date.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        input_xpath (str): XPath of the date input field.
        date_value (str): Date string in MM/DD/YYYY format, e.g. '03/01/2026'.
        timeout (int): Maximum time to wait for the input field (in seconds). Default is 15.
        clear_first (bool): Whether to clear the field before typing. Default is True.
        click_first (bool): Whether to click the field before typing. Default is True.

    Returns:
        bool: True if the date was entered successfully, False otherwise.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath))
        )

        if click_first:
            element.click()

        if clear_first:
            element.clear()

        element.send_keys(date_value)

        print(f"Entered date '{date_value}' into input: {input_xpath}")
        return True

    except Exception as e:
        print(f"Failed to enter date '{date_value}' into input '{input_xpath}': {e}")
        return False

# Files: Input / Output
# ----------------------------------------------------------------------------------
def save_list_to_csv(data_list, file_name, output_folder, column_name="value", encoding="utf-8-sig"):
    """
    Saves a Python list to a CSV file, with one item per row.

    Args:
        data_list (list): List of values to save.
        file_name (str): Name of the CSV file, e.g. 'hearing_types.csv'.
        output_folder (str): Folder path where the CSV file will be saved.
        column_name (str): Header name for the CSV column. Default is 'value'.
        encoding (str): File encoding. Default is 'utf-8-sig'.

    Returns:
        str | None: Full path of the saved CSV file if successful, otherwise None.
    """
    try:
        # Create output folder if it does not exist
        os.makedirs(output_folder, exist_ok=True)

        # Ensure file name ends with .csv
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        # Build full file path
        file_path = os.path.join(output_folder, file_name)

        # Write data to CSV
        with open(file_path, mode="w", newline="", encoding=encoding) as csv_file:
            writer = csv.writer(csv_file)

            # Write header
            writer.writerow([column_name])

            # Write each list item as a separate row
            for item in data_list:
                writer.writerow([item])

        print(f"CSV file saved successfully: {file_path}")
        return file_path

    except Exception as e:
        print(f"Failed to save list to CSV: {e}")
        return None

# # # ==================
# # # Global Constants
# # # ==================

# Base URL of the court records website
website_url = "https://portal-nc.tylertech.cloud/Portal/"

# Output folder for saving results (if needed)
OUTPUT_FOLDER = "output"

# XPath for the "Search Hearings" button
button_search_hearing = "//a[contains(normalize-space(.), 'Search Hearings')]"

# XPath for the location dropdown
dropdown_select_location = "//select[@name='SearchCriteria.SelectedCourt']"

# XPath for the hearing type dropdown
dropdown_select_hearing_type = "//select[@id='cboHSHearingTypeGroup']"

# XPath for the search type dropdown (e.g., "Search by Case Number", "Search by Party Name", etc.)
dropdown_select_search_type = "//select[@id='cboHSSearchBy']"

# XPath for the courtroom dropdown (if applicable)
dropdown_select_courtroom = "//select[@id='selHSCourtroom']"

# XPaths for date input fields 
input_date_from = "//input[@id='SearchCriteria_DateFrom']"
input_date_to = "//input[@id='SearchCriteria_DateTo']"

# XPath for the reCAPTCHA checkbox
recaptcha_checkbox = "//span[@id='recaptcha-anchor']"

# # # ==================
# # # Main Program
# # # ==================

if __name__ == "__main__":
    # Create the Chrome driver
    driver = get_chrome_driver(headless=False)
    try:
        # Navigate to the website
        driver.get(website_url)
        # Wait for the page to load and display the search input
        wait = WebDriverWait(driver, 10)

        # Step 1: Click the "Search Hearings" button
        wait_and_click(driver, button_search_hearing)

        # Select Location Dropdown
        # ========================
        # Step 2: Wait for the location dropdown to be available and select an option
        location_options = get_dropdown_options(driver, dropdown_select_location)
        print('Available location options:', location_options)

        # Save location options to CSV (For demonstration purposes)
        save_list_to_csv(
            data_list=location_options,
            file_name="location_options",
            output_folder=OUTPUT_FOLDER,
            column_name="location"
        )

        # input ('Please review the available location options above, then press Enter to select "Wake County District Court"...')

        # Step 3: Select the desired location from the dropdown
        select_dropdown_option(driver, dropdown_select_location, "Martin County")

        # Select Select Hearing Types
        # ========================
        hearing_options = get_dropdown_options(driver, dropdown_select_hearing_type)
        print('Available hearing type options:', hearing_options)
        
        # Save hearing type options to CSV (For demonstration purposes)
        save_list_to_csv(
            data_list=hearing_options,
            file_name="hearing_options",
            output_folder=OUTPUT_FOLDER,
            column_name="hearing_type"
        )

        # input ('Please review the available hearing type options above, then press Enter to select "Civil"...')

        # Step 4: Select the desired hearing type from the dropdown
        select_dropdown_option(driver, dropdown_select_hearing_type, "Probate or Mental Health")

        # Select Search Types
        # ========================
        # Step 5: Wait for the search type dropdown to be available and select an option
        search_type_options = get_dropdown_options(driver, dropdown_select_search_type)
        print('Available search type options:', search_type_options)
        
        # Save search type options to CSV (For demonstration purposes)
        save_list_to_csv(
            data_list=search_type_options,
            file_name="search_type_options",
            output_folder=OUTPUT_FOLDER,
            column_name="search_type"
        )


        # input ('Please review the available search type options above, then press Enter to select "Search by Case Number"...')

        # Step 6: Select the desired search type from the dropdown
        select_dropdown_option(driver, dropdown_select_search_type, "Courtroom")

        # Select Courtroom
        # ========================
        # Step 7: Wait for the courtroom dropdown to be available and select an option
        courtroom_options = get_dropdown_options(driver, dropdown_select_courtroom)
        print('Available courtroom options:', courtroom_options)

        # Save courtroom options to CSV (For demonstration purposes)
        save_list_to_csv(
            data_list=courtroom_options,
            file_name="courtroom_options_list",
            output_folder=OUTPUT_FOLDER,
            column_name="courtroom"
        )

        # input ('Please review the available courtroom options above, then press Enter to select "Courtroom 1"...')

        # Step 8: Select the desired courtroom from the dropdown
        select_dropdown_option(driver, dropdown_select_courtroom, "Ashe")

        # Select Dates
        # ========================
        enter_date_in_input(driver, input_date_from, "03/01/2026")
        enter_date_in_input(driver, input_date_to, "03/08/2026")

        # Step 9: Switch to the reCAPTCHA iframe and click the checkbox
        recaptcha_iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha') and contains(@src, 'anchor')]"))
        )
        driver.switch_to.frame(recaptcha_iframe)

        # Step 10: Click the reCAPTCHA checkbox
        wait_and_click_recaptcha(driver, recaptcha_checkbox)

        # Switch back to main content
        driver.switch_to.default_content()

        # Check for CAPTCHA presence
        input("Please complete the CAPTCHA on the website, then press Enter to continue...")
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()