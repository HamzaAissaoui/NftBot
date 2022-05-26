import random
from config.settings import Settings
from appium.webdriver import webdriver
from random import uniform
from time import sleep

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
driver = webdriver.WebDriver(Settings.get_server_url(),desired_cap)
driver.implicitly_wait(20)
session_uri = Settings.session_base_uri(driver.session_id)

def random_sleep(inf=0.5, sup=2.5):
    MIN_INF = 0.3
    delay = uniform(inf, sup)
    delay = max(delay, MIN_INF)
    sleep(delay)

def hand_tap(xcoord, ycoord):
        random_sleep(0.5, 2)
        move_pause = random.randint(500, 750)
        click_pause = random.randint(250, 400)
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

def swipe_by_coords(ystart=500, yend=100, xstart = 400, xend=400):
            random_sleep(0.5, 2)
            pause = random.randint(200, 350)
            pointermove1 = random.randint(250, 350)
            pointermove2 = random.randint(450, 750)
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
                                        "x":xstart,
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
                                        "x":xend,
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



