from scraper import ProcessoScraper

processo_scraper = ProcessoScraper("250000112969983")
try:
    processo_scraper.get_processo_content()
except e:
    print(e)
finally:
    processo_scraper.exit_scraper()
