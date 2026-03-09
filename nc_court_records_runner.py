# # # ==================
# # # Imports & Setup
# # # ==================
# ----------------------------------------------------------------------------------
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# ----------------------------------------------------------------------------------
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, ElementClickInterceptedException, ElementNotInteractableException
# ----------------------------------------------------------------------------------
from selenium.webdriver.common.keys import Keys

# # # ==================
# # # Main Functions
# # # ==================
# ----------------------------------------------------------------------------------
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
    return driver


# # # ==================
# # # Global Constants
# # # ==================

website_url = "https://portal-nc.tylertech.cloud/Portal/"

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

        # Check for CAPTCHA presence
        input("Please complete the CAPTCHA on the website, then press Enter to continue...")
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
