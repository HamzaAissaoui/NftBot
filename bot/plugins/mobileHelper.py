import random
from config.settings import Settings
from appium.webdriver import webdriver
from random import uniform
from time import sleep
from core.log import logger
import requests

desired_cap = {
    "platformName": Settings.get_platform_name(),
    "deviceName": Settings.get_device_name(),
    "appPackage": Settings.get_app_package(),
    "noReset": True,
    "automationName": "UiAutomator2",
    "systemPort": 8226,
    "autoLaunch": False,
    "dontStopAppOnReset": True,
    "skipDeviceInitialization": True
}
driver = webdriver.WebDriver(Settings.get_server_url(), desired_cap)
driver.implicitly_wait(30)
session_uri = Settings.session_base_uri(driver.session_id)
Settingsdata = {
    'settings': {
        'waitForIdleTimeout': 100,
        'ignoreUnimportantViews': True,
        'waitForSelectorTimeout': 3500
    }
}
requests.post(session_uri+'/appium/settings', json=Settingsdata,
              headers={'Content-Type': "application/json"})


def random_sleep(inf=1.5, sup=3, message=''):
    MIN_INF = 0.3
    delay = uniform(inf, sup)
    delay = max(delay, MIN_INF)
    logger.info(f'sleeping for {int(delay)} seconds {message}')
    sleep(delay)


def hand_tap(xcoord, ycoord):
    random_sleep(0.5, 2, message='before tapping')
    move_pause = random.randint(500, 750)
    click_pause = random.randint(250, 400)
    return {
        "actions":
            [
                {
                    "type": "pointer",
                    "id": "finger1",
                    "parameters": {"pointerType": "touch"},
                    "actions":
                    [
                        {
                            "type": "pointerMove",
                            "duration": 0, "x": xcoord, "y": ycoord
                        },
                        {
                            "type": "pause",
                            "duration": move_pause
                        },
                        {
                            "type": "pointerDown",
                            "button": 0},
                        {
                            "type": "pause",
                            "duration": click_pause
                        },
                        {
                            "type": "pointerUp",
                            "button": 0}
                    ]
                }
            ]
    }


def swipe_by_coords(ystart=500, yend=100, xstart=400, xend=400):
    random_sleep(0.5, 2, message='before swiping')
    pause = random.randint(400, 800)
    pointermove1 = random.randint(250, 350)
    pointermove2 = random.randint(600, 1200)
    return {
        "actions":
            [
                {
                    "type": "pointer",
                    "id": "finger1",
                    "parameters":
                        {"pointerType": "touch"},
                    "actions":
                        [
                            {
                                "type": "pointerMove",
                                "duration": pointermove1,
                                "x": xstart,
                                "y": ystart
                            },
                            {
                                "type": "pointerDown",
                                "button": 0
                            },
                            {
                                "type": "pause",
                                "duration": pause
                            },
                            {
                                "type": "pointerMove",
                                "duration": pointermove2,
                                "origin": "viewport",
                                "x": xend,
                                "y": yend
                            },
                            {
                                "type": "pause",
                                "duration": pause
                            },
                            {
                                "type": "pointerUp",
                                "button": 0
                            }
                        ]
                }
            ]
    }
