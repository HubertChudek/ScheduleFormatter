import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from credentials import user, password
from datetime import datetime


class FileDownloader:
    options = Options()

    def __init__(self):
        self.options.add_experimental_option("prefs", {
            "download.default_directory": os.path.dirname(os.path.realpath(__file__)),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        # self.options.add_argument("--window-size=100,100")
        self.options.add_argument("--headless");
        # self.options.add_argument("--no-startup-window")
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def goTo(self, url):
        self.driver.get(url)
        sleep(2)

    def download(self):
        user_in = self.driver.find_element_by_xpath(
            "/html/body/table[1]/tbody/tr/td/table[2]/tbody/tr/td/div/table[@class=\'tableInChaLog\']/tbody/tr/td[1]/table[@class=\'tableChaLog\'][2]/tbody/tr[3]/td[@class=\'tdChaLog\']/input[@class='inputChaLog']")
        user_in.send_keys(user)

        pw_in = self.driver.find_element_by_xpath(
            "/html/body/table[1]/tbody/tr/td/table[2]/tbody/tr/td/div/table[@class=\'tableInChaLog\']/tbody/tr/td[1]/table[@class=\'tableChaLog\'][2]/tbody/tr[5]/td[@class=\'tdChaLog\']/input[@class=\'inputChaLog\']")
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath(
            "/html/body/table[1]/tbody/tr/td/table[2]/tbody/tr/td/div/table[@class=\'tableInChaLog\']/tbody/tr/td[1]/table[@class=\'tableChaLog\'][2]/tbody/tr[6]/td[@class=\'tdChaLog\']/input[@class=\'inputLogL\']")
        login_btn.click()

        letni_btn = self.driver.find_element_by_xpath(
            "/html/body[@class='bodyWithSkeleton']/table/tbody/tr/td/table[3]/tbody/tr/td[2]/div/table[1]/tbody/tr/td[1]/nobr/table/tbody/tr/td/nobr/a[@class='yel']/b")
        zimowy_btn = self.driver.find_element_by_xpath(
            "/html/body[@class='bodyWithSkeleton']/table/tbody/tr/td/table[3]/tbody/tr/td[2]/div/table[1]/tbody/tr/td[1]/nobr/table/tbody/tr/td/nobr/a[@class='whit']/b")

        month = datetime.now().month
        if ((month <= 3 & month > 0) | (month >= 9 & month <= 12)):
            zimowy_btn.click()
        else:
            letni_btn.click()

        download_btn = self.driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[1]/table/tbody/tr[15]/td/a/img")
        download_btn.click()
        sleep(1)
        self.driver.quit()

    def quit(self):
        self.driver.quit()
