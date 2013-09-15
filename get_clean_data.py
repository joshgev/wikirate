import sys
from wikiclean import *
from wikidownload import *
import unicodedata

article_name = sys.argv[1]
	
query = form_query( article_name )
json_data = get_json_data( query )
code = get_article_code( json_data )
for article in code:

	print clean(article).encode('utf-8')