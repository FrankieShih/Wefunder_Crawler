# Wefunder_Crawler

# Requirements
python2.7, scrapy, selenium, chromedriver, Chrome

# What does it do
Crawl project info from Wefunder.com:
"project_name","slogen","money_raised","number_of_investor","revenue","net_loss","short_term_debt","raised_in_2020","cash_on_hand","net_margin","graoss_margin","return_on_asset","earnings_per_share","revenue_per_employee","cash_to_assets","revenue_to_receivables","debt_ratio","link"

# What can I configue for this crawler(incoming functions)
Set funding_flag: 
    1: crawling projects that are raising money
    0: crawling projects that are funded

# How to:
> cd wefunderSpider
> scrapy crawl quotes -o result.csv
