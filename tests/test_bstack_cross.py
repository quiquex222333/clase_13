import os, time, pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

BSTACK_USER = os.getenv("BROWSERSTACK_USERNAME")
BSTACK_KEY  = os.getenv("BROWSERSTACK_ACCESS_KEY")
REMOTE_URL  = f"https://{BSTACK_USER}:{BSTACK_KEY}@hub.browserstack.com/wd/hub"

BROWSERS = [
    {"browserName": "Chrome",  "browserVersion": "latest", "os": "Windows", "osVersion": "11"},
    {"browserName": "Firefox", "browserVersion": "latest", "os": "OS X",    "osVersion": "Ventura"},
]

@pytest.mark.parametrize("caps", BROWSERS, ids=lambda c: f"{c['browserName']}_{c['os']}")
def test_search_duckduckgo_on_browserstack(caps):
    bstack_opts = {
        "os": caps["os"],
        "osVersion": caps["osVersion"],
        "buildName": "Clase13-BStack",
        "sessionName": f"DDG search ({caps['browserName']})",
        "seleniumVersion": "4.21.0",
        "consoleLogs": "errors",
        "networkLogs": "true",
    }

    # Combinar capacidades
    desired_caps = {
        "browserName": caps["browserName"],
        "browserVersion": caps["browserVersion"],
        "bstack:options": bstack_opts
    }

    # Crear opciones y agregar capacidades
    options = webdriver.ChromeOptions()
    for key, value in desired_caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)

    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("browserstack cloud testing\n")
        assert "duckduckgo" in driver.current_url.lower()
        time.sleep(1)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason":"Búsqueda cargó resultados"}}'
        )
    except Exception as e:
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason":"{str(e)[:80]}"}}}}'
        )
        raise
    finally:
        driver.quit()
