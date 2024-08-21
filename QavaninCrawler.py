import logging
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from markdownify import markdownify 
from urllib.parse import urlparse, parse_qs 


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class QavaninCrawler:
	def __init__(self, max_pages_to_crawl):
		self.max_mages_to_crawl = max_pages_to_crawl
		self.url = 'https://qavanin.ir/' 
		self.visited_urls = []
		self.urls_to_visit = []
		self.driver = webdriver.Chrome(service=ChromeService( 
			ChromeDriverManager().install())) 

	def __get_content_of_page(self, url, img_src):
		self.driver.get(url)

		# wait for redirection to the site (if needed)
		WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, f"img[src='{img_src}']"))
		)

		

	def __get_urls_to_visite(self, element_per_page=1000):
		for page in range(1, 10):  ## FIXME: get page count
			if len(self.urls_to_visit) >= self.max_mages_to_crawl:
				break
			logging.info(f"Crawler: Reading page #{page}")
			try:
				url = self.url + f"?page={page}&size={element_per_page}"
				self.__get_content_of_page(url, "/images/MainLogo.png")
			except Exception as e:
				logging.exception(f"Error occured while reading the page {url}")
				return
			
			table = self.driver.find_element(By.CSS_SELECTOR, "table.border-list.table.table-striped.table-hover")
			table_body = table.find_element(By.TAG_NAME, "tbody")
			rows = table_body.find_elements(By.TAG_NAME, "tr")
			for row in rows:
				link = row.find_element(By.TAG_NAME, "a")
				url = link.get_attribute("href")
				self.urls_to_visit.append(url)
				if len(self.urls_to_visit) >= self.max_mages_to_crawl:
					break
			logging.info(f"Crawler: Reading page {page} complete. Total URLs is {len(self.urls_to_visit)}.")
			

	def __get_approval_id_from_url(self, url) -> int:
		parsed_url = urlparse(url)
		query_string = parsed_url.query
		params = parse_qs(query_string)
		return params.get("IDS")
	
	def __get_text_of_approvals(self, url) -> str:
		logging.info(f"Reading {url}")
		self.__get_content_of_page(url, "/images/LawHeader.jpg")
		text = self.driver.find_element(By.ID, "treeText").get_attribute("innerHTML")

		return text

	def start(self):
		self.__get_urls_to_visite()
		while len(self.urls_to_visit) > 0:
			url = self.urls_to_visit.pop()
			raw_text = self.__get_text_of_approvals(url)
			markdown_text = markdownify(raw_text)
			id = self.__get_approval_id_from_url(url)
			with open(f"out/{id}.md", "w") as f:
				f.write(markdownify(markdown_text))
			# print(markdown_text, )
			self.visited_urls.append(url)
			
		self.driver.quit()

