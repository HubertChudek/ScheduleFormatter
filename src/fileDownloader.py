from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep
from credentials import user, password
from datetime import datetime


class FileDownloader:
    options = Options()

    def __init__(self, download_directory):
        self.options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def go_to(self, url):
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

        #Rozkład zajęć
        element_to_hover_over = self.driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/table/tbody/tr/td[2]/span[2]")
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        #Mój rozkład zajęć
        element_to_hover_over = self.driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/div[2]/table/tbody/tr[1]/td[2]")
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        letni_btn = self.driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/div[3]/table/tbody/tr[2]/td[2]")
        zimowy_btn = self.driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/div[3]/table/tbody/tr[3]/td[2]")

        month = datetime.now().month
        if ((month) <= 1 & (month > 0)) | ((month >= 9) & (month <= 12)):
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
