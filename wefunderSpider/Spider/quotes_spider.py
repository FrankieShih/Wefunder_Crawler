import scrapy
import time
# import sys
from wefunderSpider.items import WefunderItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url_root = "https://wefunder.com/explore"
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['wefunder.com']

    def start_requests(self):
        self.driver = webdriver.Chrome()
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}  
        yield scrapy.Request(url=url_root, callback=self.parse, headers = headers)


    def parse(self, response):
        self.driver.get(url_root)
        # --------------------config area--------------------#

        #

        # --------------------below is the selector--------------------#
        # get the start window handle
        mainwin = self.driver.current_window_handle
        projectCount = 0
        
        # # starting search
        # searchButton.click()
        
        # def killwin(mainWinHandle):           
        #     # wait for loading and get all window handles
        #     time.sleep(2)
        #     allwin = self.driver.window_handles

        #     # kill popup windows that is not what we want
        #     for win in allwin:
        #         if win != mainWinHandle:
        #             self.driver.switch_to_window(win)
        #             self.driver.close()
        #             print win," is closed."                     
        #     # get back to main window and prepare to work        
        #     self.driver.switch_to_window(mainWinHandle)
        #     print "backed to the main window"
        #     #time.sleep(4)

        # killwin(mainwin)

        # sel = scrapy.Selector(text = self.driver.page_source);
        
        #click the more button and load more pages
        more_flag = 1
        clickCount = 1
        while(more_flag):
            js="var q=document.documentElement.scrollTop=10000"  
            self.driver.execute_script(js)  
            time.sleep(1) 
            try:
                moreButtons = self.driver.find_elements_by_class_name("wf-secondary.explore_load_more")
                moreButton = moreButtons[1]
                moreButton.click()
                clickCount += 1
                print('Loading the page ' + str(clickCount))
                time.sleep(1)
            except:
                more_flag = 0


        # # # get the projects' links on the result pages

        projectmetrics = WefunderItem()
        
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        funded_projects_page = self.driver.find_element_by_class_name("funded")
        funded_projects = funded_projects_page.find_elements_by_class_name("company-url-bn")
        crawlCount = 0
        for funded_project in funded_projects:
            projectmetrics['link'] = funded_project.get_attribute("href")
            crawlCount += 1
            print('Requesting project ' + str(crawlCount))
            url_detail = projectmetrics['link'] + "/details"
            yield scrapy.Request(url = url_detail, headers = headers, callback=self.detail_parse)

        self.driver.quit()




    def detail_parse(self, response):

        projectmetrics = WefunderItem()

        projectmetrics['link'] = response.url
        # basic information
        projectmetrics['project_name'] = response.xpath('//*[@id="company-profile-2021"]/div[1]/div[1]/div/div/div[1]/h1/b/text()').extract_first()
        projectmetrics['slogen'] = response.xpath('//*[@id="company-profile-2021"]/div[1]/div[1]/div/div/div[1]/h2/text()').extract_first()
        projectmetrics['money_raised'] = response.xpath('//*[@id="js-sidebar-height"]/div[2]/h4/text()').extract_first()
        projectmetrics['number_of_investor'] = response.xpath('//*[@id="js-sidebar-height"]/div[2]/div[1]/text()').extract_first()
                                                                                                    #Important Notice Open to accredited investors only. if this tag shows, use div[2]
        # financial information 
        projectmetrics['revenue'] = response.xpath('//*[@id="profile-content-container"]/div[3]/div[1]/div/text()').extract_first()
        projectmetrics['net_loss']= response.xpath('//*[@id="profile-content-container"]/div[3]/div[2]/div/text()').extract_first()
        projectmetrics['short_term_debt'] = response.xpath('//*[@id="profile-content-container"]/div[3]/div[3]/div/text()').extract_first()
        projectmetrics['raised_in_2020'] = response.xpath('//*[@id="profile-content-container"]/div[3]/div[4]/div/text()').extract_first()
        projectmetrics['cash_on_hand'] = response.xpath('//*[@id="profile-content-container"]/div[3]/div[5]/div/text()').extract_first()
        
        projectmetrics['net_margin'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[1]/div/text()').extract_first()
        projectmetrics['graoss_margin'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[2]/div/text()').extract_first()
        projectmetrics['return_on_asset'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[3]/div/text()').extract_first()
        projectmetrics['earnings_per_share'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[4]/div/text()').extract_first()
        projectmetrics['revenue_per_employee'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[5]/div/text()').extract_first()
        projectmetrics['cash_to_assets'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[6]/div/text()').extract_first()
        projectmetrics['revenue_to_receivables'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[7]/div/text()').extract_first()
        projectmetrics['debt_ratio'] = response.xpath('//*[@id="profile-content-container"]/*[@class="flex flex-wrap coolgray mt-6 mb-12"]/div[8]/div/text()').extract_first()
        
        return projectmetrics
