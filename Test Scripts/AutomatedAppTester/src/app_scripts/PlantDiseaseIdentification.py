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

class PlantDiseaseIdentification(AppTesterInterface):
    def initializeDriver(self):
        base_path = os.getcwd()

        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:platformVersion": "14",
            "appium:appPackage": "com.faisalkabirgalib.plant_disease_detection",
            "appium:appActivity": "com.faisalkabirgalib.plant_disease_detection.MainActivity",
            "appium:app": f"{base_path}/apks/Plant Disease Detector_1.0.0_apkcombo.com.apk",
            "appium:deviceName": "emulator-5554",
            "appium:automationName": "UiAutomator2",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 10000,
            "appium:connectHardwareKeyboard": True
        })

        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

        return driver

    def analyzeImage(self, driver, index):
        wait = WebDriverWait(driver, 30)

        try:
            # Upload Image
            el1 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Pick Image")))
            el1.click()
            time.sleep(1)

            # File picker More Options
            el2 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "More options")))
            el2.click()
            time.sleep(1)
            
            # Browse
            el3 = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.providers.media.module:id/title")))
            el3.click()
            time.sleep(1)

            # Google Photos More Options
            el4 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "More options")))
            el4.click()
            time.sleep(1)

            # Sort by
            el5 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, 
                "//android.widget.TextView[@resource-id=\"com.google.android.documentsui:id/title\" and @text=\"Sort by...\"]")))
            el5.click()
            time.sleep(1)

            # File name (A to Z)
            el6 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, 
                "//android.widget.CheckedTextView[@resource-id=\"android:id/text1\" and @text=\"File name (A to Z)\"]")))
            el6.click()
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

            el8 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Run Model")))
            el8.click()

            result_path = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[7]/android.view.View[1]"
            model_result_locator = (By.XPATH, result_path)
            new_view_text = wait.until(EC.presence_of_element_located(model_result_locator))
            model_result = new_view_text.get_attribute('content-desc').split('\n')[:-1]
            time.sleep(1)
            return model_result
        
        except Exception as error:
            print(f'error: {error}')
            return [None,None]