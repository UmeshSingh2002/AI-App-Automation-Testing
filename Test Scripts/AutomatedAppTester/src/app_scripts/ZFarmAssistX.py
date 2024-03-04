import os
import time

from src.app_tester_interface import AppTesterInterface

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ZFarmAssistX(AppTesterInterface):
    def initializeDriver(self):
        base_path = os.getcwd()

        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:platformVersion": "14",
            "appium:appPackage": "com.example.farmassist",
            "appium:appActivity": "com.example.farmassist.MainActivity",
            "appium:app": f"{base_path}/apks/FarmAssistX.apk",
            "appium:deviceName": "emulator-5554",
            "appium:automationName": "UiAutomator2",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 500,
            "appium:connectHardwareKeyboard": True
        })

        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

        return driver


    def analyzeImage(self, driver, index):
        wait = WebDriverWait(driver, 5)

        try:
            username_field = wait.until(EC.element_to_be_clickable((By.ID, "your_username_field_id")))
            username_field.send_keys("tejninja7@gmail.com")
            time.sleep(5)

            password_field = wait.until(EC.element_to_be_clickable((By.ID, "your_password_field_id")))
            password_field.send_keys("Hello123!")
            time.sleep(5)
            # Detect Button Bottom Nav Bar
            el3 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "LOG IN")))
            el3.click()
            time.sleep(5)

            # Detect Button Bottom Nav Bar
            el4 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View[@content-desc=\"Manage Monitor Detect Me\"]/android.view.View[3]")))
            el4.click()
            time.sleep(1)

            # Add Image Button
            el5 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View[@content-desc=\"No image selected\"]/android.view.View[2]")))
            el5.click()
            time.sleep(1)
           
            # Browse
            el6 = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.providers.media.module:id/title")))
            el6.click()
            time.sleep(1)

            # More Options
            el7 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "More options")))
            el7.click()
            time.sleep(1)


            # More Options (Browse Button)
            el8 = wait.until(EC.element_to_be_clickable((AppiumBy.ID,"com.google.android.providers.media.module:id/title")))
            el8.click()
            time.sleep(1)


            #Google Photos Button
            el9 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id='com.google.android.documentsui:id/app_icon'])[3]")))
            el9.click()
            time.sleep(1)

            # Browse
            el10 = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "//android.widget.RelativeLayout")))
            el10.click()
            time.sleep(1)
   
            # File name (A to Z)
            el11 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,
                "//android.widget.CheckedTextView[@resource-id=\"android:id/text1\" and @text=\"File name (A to Z)\"]")))
            el11.click()
            time.sleep(1)

            # Handle case of index > 15 (needs scroll)
            # This method only supports up to 30 files
            if index > 15:
                #swipe(startX, startY, endX, endY, duration)
                driver.swipe(530,2115, 525,200, 1000)
                adjusted_index = index - 9
            else:
                adjusted_index = index
            time.sleep(1)

            el7 = wait.until(EC.element_to_be_clickable((By.XPATH,
                f"(//android.widget.ImageView[@resource-id=\"com.google.android.documentsui:id/icon_thumb\"])[{adjusted_index}]")))
            el7.click()
            time.sleep(1)

            el12 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Run Model")))
            el12.click()

            result_path = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[7]/android.view.View[1]"
            model_result_locator = (By.XPATH, result_path)
            new_view_text = wait.until(EC.presence_of_element_located(model_result_locator))
            model_result = new_view_text.get_attribute('content-desc').split('\n')[:-1]
            time.sleep(1)
            return model_result
       
        except Exception as error:
            print(f'error: {error}')
            return [None,None]
