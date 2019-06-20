# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as BS


class ProcessoScraper:
    def __init__(self, processo):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.processo = processo
        self.base_url = "https://consultas.anvisa.gov.br/#/documentos/tecnicos/{}/?processo={}".format(
            self.processo, self.processo
        )
        self.processo_content = ""
        self.peticionamentos = []

    def get_processo_page(self):
        request = self.driver.get(self.base_url)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr"))
            )
        except:
            # TODO: Implement silent fail
            print("NÃO ENCONTREI ESSA PORRA")

        self.processo_content = self.driver.page_source

    def get_processo_content(self):
        # REFACTOR: Change scraping cycle to XPATH and to Scrapy
        self.get_processo_page()
        panels = self.driver.find_elements_by_css_selector("tr")
        for panel in panels:
            panel_scraper = panel.text.split("\n")
            if len(panel_scraper) < 2:
                continue

            panel_result = {
                "expediente": panel_scraper[1],
                "n_protocolo": panel_scraper[3],
                "assunto": panel_scraper[5],
                "encontrase": panel_scraper[7],
                "data_encontrase": panel_scraper[8],
                "situacao": panel_scraper[10],
            }
            if len(panel_scraper) > 12:
                panel_result["publicacao"] = panel_scraper[12]

            self.peticionamentos.append(panel_result)

    def exit_scraper(self):
        self.driver.exit()
