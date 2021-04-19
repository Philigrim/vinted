from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import os

import time
import json
import shutil

from selenium.webdriver.firefox.webdriver import FirefoxProfile

if __name__ == "__main__":

    path = os.getcwd() + "\\"
    
    subfolders = [ f.path for f in os.scandir(path) if f.is_dir() ]
    len(subfolders)
    for folder in subfolders:
        os.chdir((folder).replace('\\','/'))
        os.system('python ikeltiItem.py')