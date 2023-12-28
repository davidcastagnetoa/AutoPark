from selenium import webdriver

try:
    driver = webdriver.Firefox()
    driver.get("https://www.google.com")
    print(driver.title)
finally:
    driver.quit()
