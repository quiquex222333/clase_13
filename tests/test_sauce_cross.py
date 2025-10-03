import os, time, pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

SAUCE_USER = os.getenv("SAUCE_USERNAME")
SAUCE_KEY  = os.getenv("SAUCE_ACCESS_KEY")
REMOTE_URL = f"https://{SAUCE_USER}:{SAUCE_KEY}@ondemand.saucelabs.com/wd/hub"

# Matriz simple
BROWSERS = [
    {"browserName": "chrome",  "browserVersion": "latest", "platformName": "Windows 11"},
    {"browserName": "firefox", "browserVersion": "latest", "platformName": "macOS 13"},
]

@pytest.mark.parametrize("caps", BROWSERS, ids=lambda c: f"{c['browserName']}_{c['platformName']}")
def test_search_duckduckgo_on_sauce(caps):
    sauce_options = {
        "name": f"DDG search ({caps['browserName']})",
        "build": "Clase13-Sauce",
        "seleniumVersion": "4.21.0",
        "extendedDebugging": True,
        "username": SAUCE_USER,
        "accessKey": SAUCE_KEY
    }


    
    desired_caps = {
        "browserName": caps["browserName"],
        "browserVersion": caps["browserVersion"],
        "platformName": caps["platformName"],
        "sauce:options": sauce_options,
    }
    
    # Crear opciones y agregar capacidades
    options = webdriver.ChromeOptions()
    for key, value in desired_caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    try:
        driver.get("https://duckduckgo.com/")
        driver.find_element(By.NAME, "q").send_keys("sauce labs cloud testing\n")
        assert "duckduckgo" in driver.current_url.lower()
        time.sleep(1)
        # marcar passed usando Sauce REST executor (vía script)
        driver.execute_script("sauce:job-result=passed")
    except Exception:
        driver.execute_script("sauce:job-result=failed")
        raise
    finally:
        driver.quit()
