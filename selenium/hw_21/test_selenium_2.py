import os

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver_new():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    # Передача драйвера в тест
    yield driver

    # Закрытие браузера после завершения теста
    driver.quit()


@pytest.fixture()
def driver_rus():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=ru")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    # Передача драйвера в тест
    yield driver
    # Закрытие браузера после завершения теста
    driver.quit()


def test_for_window(driver_new):
    driver_new.get("https://demoqa.com/browser-windows")
    driver_new.find_element(By.ID, "tabButton").click()
    tabs = driver_new.window_handles
    driver_new.switch_to.window(tabs[1])
    assert driver_new.find_element(By.ID, "sampleHeading").text == "This is a sample page"
    driver_new.close()
    driver_new.switch_to.window(tabs[0])


def test_for_frames(driver_new):
    driver_new.get("https://demoqa.com/frames")
    driver_new.switch_to.frame(driver_new.find_element(By.ID, "frame1"))
    assert driver_new.find_element(By.CSS_SELECTOR, "h1[id='sampleHeading']").text == "This is a sample page"
    driver_new.switch_to.default_content()
    driver_new.switch_to.frame(driver_new.find_element(By.ID, "frame2"))
    assert driver_new.find_element(By.CSS_SELECTOR, "h1[id='sampleHeading']").text == "This is a sample page"


def test_for_alert(driver_new):
    driver_new.get("https://demoqa.com/alerts")
    # Нажатие на первый алерт
    driver_new.find_element(By.ID, "alertButton").click()
    alert1 = driver_new.switch_to.alert
    alert1.accept()

    # Нажатие на второй алерт
    driver_new.find_element(By.ID, "confirmButton").click()
    alert2 = driver_new.switch_to.alert
    alert2.dismiss()
    assert driver_new.find_element(By.ID, "confirmResult").text == "You selected Cancel"

    # Нажатие на 3й алерт
    driver_new.find_element(By.ID, "promtButton").click()
    alert3 = driver_new.switch_to.alert
    alert3.send_keys("Selenium Test")
    alert3.accept()
    assert driver_new.find_element(By.ID, "promptResult").text == "You entered Selenium Test"


def test_task_4_1(driver_rus):
    driver_rus.get("https://www.google.com")
    assert driver_rus.find_element(By.CSS_SELECTOR, "textarea[class='gLFyf']").get_attribute("title") == "Поиск"


def test_for_actions(driver_new):
    driver_new.get("https://jqueryui.com/droppable/")
    driver_new.switch_to.frame(driver_new.find_element(By.CSS_SELECTOR, ".demo-frame"))
    source_element = driver_new.find_element(By.CSS_SELECTOR, "div[id='draggable']")
    target_element = driver_new.find_element(By.CSS_SELECTOR, "div[id='droppable']")

    # Перетаскивание квадратика
    action = ActionChains(driver_new)
    action.drag_and_drop(source_element, target_element).perform()
    assert target_element.text == "Dropped!"
