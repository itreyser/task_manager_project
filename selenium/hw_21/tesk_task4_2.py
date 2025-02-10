import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture()
def driver():
    """Pytest fixture to set up and tear down the WebDriver instance."""
    download_dir = os.path.join(os.getcwd(), "Downloads")

    # Chrome options with download preferences
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    config_driver = webdriver.Chrome(service=service, options=chrome_options)
    config_driver.implicitly_wait(3)
    yield config_driver
    config_driver.quit()


def test_task4_2(driver):
    """Test to download a file and verify the download."""
    download_dir = os.path.join(os.getcwd(), "Downloads")
    file_name = "file-sample_100kB.doc"

    # Set up explicit wait
    wait = WebDriverWait(driver, 15)

    # Open the website
    driver.get("https://file-examples.com/index.php/sample-documents-download/")

    # Scroll to and click the first file link
    files = driver.find_elements(By.CSS_SELECTOR, ".text-right.file-link > a")
    actions = ActionChains(driver)
    actions.move_to_element(files[0]).perform()
    files[0].click()
    close_ads(driver)

    # Verify navigation to the file page
    assert "index.php/sample-documents-download/sample-doc-download/" in driver.current_url, "Failed to navigate to file page"

    # Click the download button
    file_sizes = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-orange.btn-outline.btn-xl.page-scroll.download-button")
    actions.move_to_element(file_sizes[0]).perform()
    file_sizes[0].click()

    # Check if the file is downloaded
    check_download(wait, download_dir, file_name)


def close_cookie_window(driver):
    """Close the cookie banner if present."""
    try:
        cookie_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
        )
        cookie_close_button.click()
    except Exception:
        print("No cookie banner to close.")


def check_download(wait, download_dir, file_name):
    """Wait for the file to appear in the download directory."""
    wait.until(lambda driver: os.path.exists(os.path.join(download_dir, file_name)), "File not downloaded")
    print("Download completed!")


def close_ads(driver):
    """Перебирает все рекламные iframes, ищет кнопку 'Close' и закрывает рекламу."""
    try:
        # Находим все iframes на странице
        all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(all_iframes)} iframes on the page.")

        for iframe in all_iframes:
            try:
                iframe_id = iframe.get_attribute("id")
                if not iframe_id or not iframe_id.startswith("aswift"):
                    continue  # Пропускаем не относящиеся к рекламе iframes

                print(f"Trying to switch to iframe: {iframe_id}")
                driver.switch_to.frame(iframe)

                # Проверяем кнопку закрытия сразу в этом iframe
                try:
                    ad_close_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "dismiss-button"))
                    )
                    ad_close_button.click()
                    print("Ad banner closed in main iframe.")
                    driver.switch_to.default_content()
                    return  # Выходим из функции сразу

                except Exception:
                    print("No close button found in main iframe, checking nested iframe.")

                # Ищем вложенный iframe с рекламой
                try:
                    nested_iframe = driver.find_element(By.TAG_NAME, "iframe")
                    driver.switch_to.frame(nested_iframe)
                    print("Switched to nested ad_iframe.")

                    # Проверяем кнопку закрытия внутри вложенного iframe
                    ad_close_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "dismiss-button"))
                    )
                    ad_close_button.click()
                    print("Ad banner closed in nested iframe.")
                    driver.switch_to.default_content()
                    return  # Выходим из функции сразу

                except Exception:
                    print(f"No ad found in nested iframe of {iframe_id}, switching back.")

            except Exception as e:
                print(f"Error switching to iframe {iframe_id}: {e}")

            finally:
                driver.switch_to.default_content()  # Возвращаемся в основной контент

        print("No ads found in any iframe.")

    except Exception as e:
        print(f"General error while handling ads: {e}")

    finally:
        driver.switch_to.default_content()
        print("Returned to main content.")




