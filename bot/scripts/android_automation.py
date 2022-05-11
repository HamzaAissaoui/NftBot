from time import sleep
from appium import webdriver
from selenium.webdriver.common.by import By
from config.settings import Settings
from helper import logger
from models import Sneaker, Attributes, BoughtSneaker, db

desired_cap ={
    "platformName": Settings.get_platform_name(),
    "deviceName": Settings.get_device_name(),
    "appPackage": Settings.get_app_package(),
    "noReset": True,
    "automationName": "UiAutomator2",
    "systemPort" : 8226,
    "autoLaunch": False,
    "dontStopAppOnReset":True,
    "skipDeviceInitialization": True,
    "fullReset":False
}
android_driver = webdriver.Remote(Settings.get_server_url(), desired_cap)
SESSION_BASE_URI = Settings.session_base_uri(android_driver.session_id)

class Android:

    driver = android_driver

    def scrap_sneakers(self):
        self.restart_app()
        #Put scrapping here

    def restart_app(self):
        try:
            self.driver.close_app()
            sleep(1)
            self.driver.launch_app()
        except:
            logger.error('Cannot Restart App!')
    
    def hand_tap(self, xcoord, ycoord, move_pause=1500, click_pause = 300):
        return {
                "actions":
                [
                    {
                        "type":"pointer",
                        "id":"finger1",
                        "parameters":{"pointerType":"touch"},
                        "actions":
                        [
                            {
                                "type":"pointerMove",
                                "duration":0,"x":xcoord,"y": ycoord
                            },
                            {
                                "type":"pause",
                                "duration":move_pause
                            },
                            {
                                "type":"pointerDown",
                                "button":0},
                            {
                                "type":"pause",
                                "duration":click_pause
                            },
                            {
                                "type":"pointerUp",
                                "button":0}
                        ]
                    }
                ]
            }

    def scroll_by_coords(self, ystart=500, yend=100, xcoord = 400, pause=250, pointermove1=300, pointermove2=750):
            return {
                "actions":
                    [
                        {
                            "type":"pointer",
                            "id":"finger1",
                            "parameters":
                                {"pointerType":"touch"},
                            "actions":
                                [
                                    {
                                        "type":"pointerMove",
                                        "duration":pointermove1,
                                        "x":xcoord,
                                        "y":ystart
                                    },
                                    {
                                        "type":"pointerDown",
                                        "button":0
                                    },
                                    {
                                        "type":"pause",
                                        "duration":pause
                                    },
                                    {
                                        "type":"pointerMove",
                                        "duration":pointermove2,
                                        "origin":"viewport",
                                        "x":xcoord,
                                        "y":yend
                                    },
                                    {
                                        "type":"pause",
                                        "duration":pause
                                    }
                                ]
                        }
                    ]
            }