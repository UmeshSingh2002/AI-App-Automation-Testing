import os
import time

from ..app_tester_interface import AppTesterInterface

from appium import webdriver

from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class DoctorP(AppTesterInterface):
    def initializeDriver(self):
        base_path = os.getcwd()

        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:platformVersion": "14",
            "appium:appPackage": "com.pdd.pdd",
            "appium:appActivity": "com.pdd.pdd.MainActivity",
            "appium:app": f"{base_path}/apks/DoctorPAPK.apk",
            "appium:deviceName": "emulator-5554",
            "appium:automationName": "UiAutomator2",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True
        })

        try:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        except:
            print('Error Instantiating AppTesterInterface. Skipping tests ...')
            return None
            
        return driver

    def analyzeImage(self, driver, index):
        wait = WebDriverWait(driver, 30)

        try:
            if index == 9:
                index = index+1
            # Upload Image
            if index == 1:
                el1 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Explore")))
                el1.click()
                time.sleep(1)
            else:
                driver.press_keycode(4)

            # Picture Icon
            el2 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[1]")))
            el2.click()
            time.sleep(1)

            # File picker More Options
            if index == 1:
                el3 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Understood, I’m ready")))
                el3.click()
                time.sleep(1)
            
            # Permission
            if index == 1:
                el4 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@resource-id=\"com.android.permissioncontroller:id/permission_allow_foreground_only_button\"]")))
                el4.click()
                time.sleep(1)

            # Permission
            if index == 1:
                el5 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@resource-id=\"com.android.permissioncontroller:id/permission_allow_foreground_only_button\"]")))
                el5.click()
                time.sleep(1)

            # Image Icon
            el6 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Photos")))
            el6.click()
            time.sleep(1)

            # Permission
            if index == 1:
                el7 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@resource-id=\"com.android.permissioncontroller:id/permission_allow_button\"]")))
                el7.click()
                time.sleep(1)

           # Google Photos More Options
            el8 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "More options")))
            el8.click()
            time.sleep(1)

            # Sort by
            el9 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, 
                "//android.widget.TextView[@resource-id=\"com.google.android.documentsui:id/title\" and @text=\"Sort by...\"]")))
            el9.click()
            time.sleep(1)

            # File name (A to Z)
            el10 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, 
                "//android.widget.CheckedTextView[@resource-id=\"android:id/text1\" and @text=\"File name (A to Z)\"]")))
            el10.click()
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

            el11 = wait.until(EC.element_to_be_clickable((By.XPATH, 
                f"(//android.widget.ImageView[@resource-id=\"com.google.android.documentsui:id/icon_thumb\"])[{adjusted_index}]")))
            el11.click()
            time.sleep(1)

            # Press Send button
            el12 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]")))
            el12.click()
            time.sleep(7)

            result_path = "//android.widget.ScrollView/android.view.View[3]/android.view.View/android.view.View"
            model_result_locator = (By.XPATH, result_path)
            new_view_text = wait.until(EC.presence_of_element_located(model_result_locator))
            model_result = new_view_text.get_attribute('content-desc')

            result_path2 = "//android.widget.ScrollView/android.view.View[2]/android.view.View/android.view.View[1]/android.widget.ImageView"
            model_result_locator2 = (By.XPATH, result_path2)
            new_view_text2 = wait.until(EC.presence_of_element_located(model_result_locator2))
            model_result2 = new_view_text2.get_attribute('content-desc')

            time.sleep(1)
            result = [model_result, model_result2]
            return result
        

        except Exception as error:
            print(f'error: {error}')
            return [None, None]