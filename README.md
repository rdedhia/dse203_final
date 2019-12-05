1. Run the crawler in wiki_crawler
  - `scrapy crawl -s DEPTH_LIMIT=1 wiki_entities`
  - outputs `entities.json`
2. copy `entities.json` into the nlp folder
  - run the notebooks in NLP folder
  - output `all_entities.json`
3. copy `all_entities.json` into the BuildlingNeo4jTables folder
4. Run the notebook `generate_tables_CSVs.ipynb` in the BuildingNeo4jTables folder
5. Copy all CSV files into Neo4j database's "import" folder
6. Open `Neo4j_Create_scripts.ipynb` and execute the commands to generate graph
7. Execute queries in `neo4j_queries.txt`
