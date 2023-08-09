from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import undetected_chromedriver as uc

from time import sleep

username = ''
password = ''

my_lat = 4
my_long = 1


class MyUDC(uc.Chrome):
    def __del__(self):
        try:
            self.service.process.kill()
        except:  # noqa
            pass
        # self.quit()


driver = MyUDC()

driver.delete_all_cookies()
driver.maximize_window()
driver.execute_cdp_cmd("Browser.grantPermissions",
                       {
                           "origin": "https://tinder.com/",
                           "permissions": ["geolocation"]
                       },
                       )
driver.execute_cdp_cmd(
    "Emulation.setGeolocationOverride",
    {
        "latitude": my_lat,
        "longitude": my_long,
        "accuracy": 100,
    },
)

# ---- testing geo overrider ------------- #
# driver.get("https://www.openstreetmap.org/")
# driver.find_element(By.XPATH, "//span[@class='icon geolocate']").click()
#

# ------------ loging in with google account --------------- #
driver.get('https://accounts.google.com/ServiceLogin')
sleep(2)

driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(username)
sleep(1)
driver.find_element(By.XPATH, '//*[@id="identifierNext"]').click()
sleep(2)

driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)
sleep(1)
driver.find_element(By.XPATH, '//*[@id="passwordNext"]').click()
sleep(4)

# ---------------- old log in attempt ----------------- #
# GOOGLE_USER_PROFILE_PATH = "C:/Users/tobif/AppData/Local/Google/Chrome/User Data/Profile 1"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# options.add_argument("--user-data-dir=C:/Users/tobif/AppData/Local/Google/Chrome/User Data/Profile 1")
#
# driver = webdriver.Chrome(options=options)


# --------------- tinder ----------------- #
driver.get("https://tinder.com/")
driver.maximize_window()
sleep(4)

# ------ decline cookies ------ #
try:
    driver.find_element(By.XPATH,
                        '//*[@id="q-620494849"]/div/div[2]/div/div/div[1]/div[2]/button/div[2]/div[2]').click()
    sleep(1)
except NoSuchElementException:
    print("cookies already rejected")
    sleep(2)
# first log in button
driver.find_element(By.XPATH, '//*[@id="q-620494849"]/div/div[1]/div/'
                              'main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]').click()
sleep(5)

driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@title="Sign in with Google Dialog"]'))
# title should be : "Sign in with Google Dialog" //*[@title="Sign in with Google Dialog"]
sleep(2)
google_sign_in_button = driver.find_element(By.XPATH, '//*[@id="continue-as"]')
print(google_sign_in_button.text)
print("element found")
google_sign_in_button.click()
sleep(5)
# It works !!!!!!!


print(driver.title)
sleep(10) # enough time for tinder to load
# allow location
try:
    driver.find_element(By.XPATH, '//*[@id="q1946091371"]/main/div/div/div/div[3]/button[1]/div[2]/div[2]').click()
    sleep(5)
except NoSuchElementException:
    print("location already allowed")
# deny notifications
try:
    driver.find_element(By.XPATH, '//*[@id="q1946091371"]/main/div/div/div/div[3]/button[2]/div[2]/div[2]').click()
    sleep(4)
except NoSuchElementException:
    print("Notification already allowed/declined")


# hit like
for n in range(5):
    try:
        like = driver.find_element(By.XPATH, '//span[text()="Like"]')
        like.click()
        sleep(4)
        #
    except ElementClickInterceptedException:
        print("like button not found looking for match")
        try:
            match_popup = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button/span/span/svg')
            match_popup.click()
            # <svg focusable="false" aria-hidden="true" role="presentation" viewBox="0 0 24 24" width="24px" height="24px" class="Sq(28px) P(4px)"><path fill-rule="evenodd" clip-rule="evenodd" d="M0.585786 0.585786C1.36683 -0.195262 2.63317 -0.195262 3.41422 0.585786L12 9.17157L20.5858 0.585787C21.3668 -0.195262 22.6332 -0.195262 23.4142 0.585787C24.1953 1.36684 24.1953 2.63317 23.4142 3.41421L14.8284 12L23.4142 20.5858C24.1953 21.3668 24.1953 22.6332 23.4142 23.4142C22.6332 24.1953 21.3668 24.1953 20.5858 23.4142L12 14.8284L3.41422 23.4142C2.63317 24.1953 1.36683 24.1953 0.585786 23.4142C-0.195262 22.6332 -0.195262 21.3668 0.585786 20.5858L9.17157 12L0.585786 3.41421C-0.195262 2.63317 -0.195262 1.36683 0.585786 0.585786Z"></path></svg>
            # //*[@id="q-290123648"]/main/div/div[1]/div/div[4]/button/svg
            # <span class="Hidden">Close</span>
        except NoSuchElementException:
            sleep(3)

print("that enough likes for today")