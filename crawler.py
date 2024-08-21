# import logging
# from urllib.parse import urljoin
# import requests
# from bs4 import BeautifulSoup

# logging.basicConfig(
#     format='%(asctime)s %(levelname)s:%(message)s',
#     level=logging.INFO)

# class Crawler:

#     def __init__(self, urls=[]):
#         self.visited_urls = []
#         self.urls_to_visit = urls

#     def download_url(self, url):
#         return requests.get(url).text

#     def get_linked_urls(self, url, html):
#         soup = BeautifulSoup(html, 'html.parser')
#         print("....")
#         print(html)
#         for link in soup.find_all('a'):
#             print("..../")
#             path = link.get('href')
#             if path and path.startswith('/'):
#                 path = urljoin(url, path)
#             yield path

#     def add_url_to_visit(self, url):
#         if url not in self.visited_urls and url not in self.urls_to_visit:
#             self.urls_to_visit.append(url)

#     def crawl(self, url):
#         html = self.download_url(url)
#         for url in self.get_linked_urls(url, html):
#             self.add_url_to_visit(url)

#     def run(self):
#         while self.urls_to_visit:
#             url = self.urls_to_visit.pop(0)
#             logging.info(f'Crawling: {url}')
#             try:
#                 self.crawl(url)
#             except Exception:
#                 logging.exception(f'Failed to crawl: {url}')
#             finally:
#                 self.visited_urls.append(url)

#         logging.info(f'Crawling has Ended!')

# if __name__ == '__main__':
#     Crawler(urls=['https://www.qavanin.ir/']).run()




#######################################################################################################

# pip install selenium webdriver-manager


# # URL of the web page to scrape 
# url = 'https://www.qavanin.ir' 


# visited_urls = []
# urls_to_visit = []

# # set up Chrome WebDriver using ChromeDriverManager 
# driver = webdriver.Chrome(service=ChromeService( 
# 	ChromeDriverManager().install())) 


# # open the specified URL in the browser 
# driver.get(url) 

# try:
# 	WebDriverWait(driver, 10).until(
# 		EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/images/MainLogo.png']"))
# 	)

# 	print(driver.page_source)
# except Exception as e:
# 	print(f"An error occured: {e}")
# 	exit


# get urls


########################################
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class QavaninCrawler:
	def __init__(self, max_pages_to_crawl):
		self.max_mages_to_crawl = max_pages_to_crawl
		self.url = 'https://qavanin.ir/' 
		self.visited_urls = []
		self.urls_to_visit = []
		self.driver = webdriver.Chrome(service=ChromeService( 
			ChromeDriverManager().install())) 

	def start(self):
		self.driver.get(self.url + "?page=1&size=1000")

		# wait for redirection to the site
		try:
			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/images/MainLogo.png']"))
			)

			# print(self.driver.page_source)
		except Exception as e:
			print(f"An error occured: {e}")
			return
		
		table = self.driver.find_element(By.CSS_SELECTOR, "table.border-list.table.table-striped.table-hover")
		rows = table.find_elements(By.TAG_NAME, "tr")
		for row in rows:
			link = row.find_element(By.TAG_NAME, "a")
			url = link.get_attribute("href")
			self.urls_to_visit.append(url)


		print(len(self.urls_to_visit))
		print(self.urls_to_visit)
		self.driver.quit()


crawler = QavaninCrawler(max_pages_to_crawl=5)
crawler.start()