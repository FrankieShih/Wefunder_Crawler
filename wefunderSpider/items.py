# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WefunderItem(scrapy.Item):
	# basic information
	project_name = scrapy.Field()
	slogen = scrapy.Field()
	money_raised = scrapy.Field()
	number_of_investor = scrapy.Field()
	# financial information 
	revenue = scrapy.Field()
	net_loss = scrapy.Field()
	short_term_debt = scrapy.Field()
	raised_in_2020 = scrapy.Field()
	cash_on_hand = scrapy.Field()
	net_margin = scrapy.Field()
	graoss_margin = scrapy.Field()
	return_on_asset = scrapy.Field()
	earnings_per_share = scrapy.Field()
	revenue_per_employee = scrapy.Field()
	cash_to_assets = scrapy.Field()
	revenue_to_receivables = scrapy.Field()
	debt_ratio = scrapy.Field() 
	# text information  
	risks = scrapy.Field()
	# other 
	link = scrapy.Field()



