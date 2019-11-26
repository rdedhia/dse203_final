   To run the cralwer:
   
   `cd wiki_crawler`
   `scrapy crawl -s DEPTH_LIMIT=1 wiki_entities`
   
   This outputs a file `entities.json` which contains JSON objects for each entity found within the crawl.
