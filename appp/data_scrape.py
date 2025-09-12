from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Scrape():
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.BASE_URL= "https://www.avax.network/about/blog"
        self.games_data=[]
        self.builder_data=[]
        self.nfts_data = []

    def scrape_category(self, category_name,storage_list):
        self.driver.get(self.BASE_URL)
        time.sleep(3)
        print(f"Scraping category: {category_name}")
        lower=category_name.lower()
        if category_name=="Builders":
            category_button=self.driver.find_element(By.ID, value=f"checkbox-{lower}")
        elif category_name=="Gaming":
            category_button=self.driver.find_element(By.CSS_SELECTOR, "#checkbox-gaming")
        elif category_name == "NFTs, Arts, and Culture":
            category_button=self.driver.find_element(By.CSS_SELECTOR, "#checkbox-nft")
        category_button.click()
        time.sleep(3)

    #Continuous clicking of view more button till it's gone
        while True:
            try:
                view_more=self.driver.find_element(By.ID, value="load-more-button")
                view_more.click()
            except:
                break

        time.sleep(3)
        posts = self.driver.find_elements(By.CSS_SELECTOR, "#articles-wrapper a")

        for post in posts:
            article= post.get_attribute("href")
            storage_list.append(article)    
        print(f"Scraping {category_name} complete")


    def get_content(self, categ_list):
        print("Getting the content of the various articles")
        all_articles = []
        
        for link in categ_list:
            self.driver.get(link)
            textz = self.driver.find_elements(By.CSS_SELECTOR, ".flex.flex-col.items-stretch.justify-start.gap-md p")
            paragraphs = [tex.text for tex in textz][:-1]
            page_text = " ".join(paragraphs) 
            all_articles.append(page_text) 
        
        return all_articles 


