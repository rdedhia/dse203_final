import requests
from bs4 import BeautifulSoup
import json
import re


urls = [# "https://en.wikipedia.org/wiki/Twitter", 
		"https://en.wikipedia.org/wiki/Facebook",
		"https://en.wikipedia.org/wiki/Vine_(service)",
		'https://en.wikipedia.org/wiki/Snapchat', 
    	'https://en.wikipedia.org/wiki/Instagram', 
    	'https://en.wikipedia.org/wiki/Periscope_(app)',
    	'https://en.wikipedia.org/wiki/Summify'
		]




for u in urls:
	out_d = {}
	r = requests.get(u)
	wiki_content = r.text
	soup = BeautifulSoup(wiki_content, 'lxml')
	title = soup.find_all('h1')[0].get_text()
	abstract_html, text_body = wiki_content.split('<h2>',1)
	abstract_soup = BeautifulSoup(abstract_html, 'lxml')
	abstract = abstract_soup.find_all('p')
	abstract_text = ' '.join([a.get_text() for a in abstract])
	cleaned_abstract = re.sub('\s+', ' ', abstract_text)

	rest_of_text_soup = BeautifulSoup(text_body, 'lxml')
	p_tags = rest_of_text_soup.find_all('p')
	text = ' '.join([t.get_text() for t in p_tags])
	cleaned_text = re.sub('\s+', ' ', text)


	out_d["title"] = title
	# out_d["abstract"] = cleaned_abstract
	# out_d["text"] = cleaned_text
	out_d["text"] = cleaned_abstract + cleaned_text
	with open('{}.json'.format(title), 'w') as outfile:
		outfile.write(json.dumps(out_d))



	

