1. Run the crawler in wiki_crawler
  - `scrapy crawl -s DEPTH_LIMIT=1 wiki_entities`
  - outputs `entities.json`
2. Run the notebooks in NLP folder
  - Run `scrape_wiki.py` to generate `json` files for each of the main companies
  - Run `add_triples_from_text.ipynb` and `add_more_triples.ipynb` to extract new triples from those json files
  - Output `all_entities.json`
3. copy `all_entities.json` into the BuildlingNeo4jTables folder
4. Run the notebook `generate_tables_CSVs.ipynb` in the BuildingNeo4jTables folder
5. Copy all CSV files into Neo4j database's "import" folder
6. Open `Neo4j_Create_scripts.ipynb` and execute the commands to generate graph
7. Execute queries in `neo4j_queries.txt`
