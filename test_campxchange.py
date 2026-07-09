import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()




def test_page_load(driver):

    print("\n--- Running Test 1: Page Load Verification ---")
    
    driver.get("http://localhost:5173")

    assert "SellBee" in driver.title, f"Expected title 'SellBee', but got '{driver.title}'"
    root_container = driver.find_element(By.ID, "root")
    assert root_container.is_displayed(), "Main application container is not visible."
    
    print("Test 1 Passed: App loaded successfully and root container is visible.")


def test_search_function(driver):
    print("\n--- Running Test 2: Search Functionality Verification ---")

    driver.get("http://localhost:5173")
    driver.execute_script("window.localStorage.setItem('selectedCampus', 'IIT Kanpur, Kanpur');")
    driver.get("http://localhost:5173/home")

    wait = WebDriverWait(driver, 10)

    search_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search the marketplace...']"))
    )
    assert search_input.is_displayed(), "Search input box is not visible."
    test_query = "Electronics"
    search_input.send_keys(test_query)
    current_value = search_input.get_attribute("value")

    assert current_value == test_query, f"Search input contains '{current_value}' instead of '{test_query}'"

    print("Test 2 Passed: Search input was successfully typed into.")



def test_signin_validation(driver):
    print("\n--- Running Test 3: Sign-In Validation Failure ---")

    driver.get("http://localhost:5173/signin")

    email_input = driver.find_element(By.XPATH, "//input[@placeholder='student@campus.edu']")
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    email_input.send_keys("invalidemail")
    password_input.send_keys("password123")

    form = driver.find_element(By.CLASS_NAME, "auth-form")
    form.submit()

    assert "/signin" in driver.current_url, "User was redirected away despite validation errors."
    print("Test 3 Passed: Form validation successfully blocked the invalid sign-in attempt.")



def test_signin_success_and_banner(driver):
    print("\n--- Running Test 4: Custom Sign-In & Verification Banner Check ---")

    driver.get("http://localhost:5173/signin")

    email_input = driver.find_element(By.XPATH, "//input[@placeholder='student@campus.edu']")
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    email_input.send_keys("sparshgupta@gmail.com")
    password_input.send_keys("123456789")

    form = driver.find_element(By.CLASS_NAME, "auth-form")
    form.submit()
    wait = WebDriverWait(driver, 10)

    try:
        wait.until(EC.url_contains("/home"))
        print("Logged in successfully! Redirected to /home.")
        verification_alert = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "email-verification-alert"))
        )
        assert verification_alert.is_displayed(), "Email verification banner is not displayed."
        print("Test 4 Passed: User logged in and verification banner is showing.")
    except Exception as e:
        print(f"Login outcome: Stayed on page {driver.current_url} due to: {type(e).__name__}")
        raise e




def test_admin_dashboard_restricted(driver):

    print("\n--- Running Test 5: Admin Dashboard Access Verification ---")

    driver.get("http://localhost:5173/signin")


    email_input = driver.find_element(By.XPATH, "//input[@placeholder='student@campus.edu']")
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    email_input.send_keys("sparshgupta@gmail.com")
    password_input.send_keys("123456789")

    form = driver.find_element(By.CLASS_NAME, "auth-form")
    form.submit()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/home"))

    driver.get("http://localhost:5173/profile")

    menu_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'more_vert')]"))
    )

    menu_button.click()
    admin_links = driver.find_elements(By.XPATH, "//*[contains(text(), 'Admin Dashboard')]")
    assert len(admin_links) == 0, "Security vulnerability: Admin Dashboard option is visible to a regular user."
    print("Test 5 Passed: Verified that Admin Dashboard is not accessible or visible to regular users.")
