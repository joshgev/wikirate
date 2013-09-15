import json
import urllib2 as urllib
import sys
import unicodedata

def form_query( page_name ):
	return "http://en.wikipedia.org/w/api.php?format=json&action=query&titles="+page_name+"&prop=revisions&rvprop=content"

def get_json_data( url ):

	data = ""
	handle = urllib.urlopen( url ) 
	data = handle.read()
	handle.close()
	
	# return unicodedata.normalize('NFKD',u''+data).encode('ascii','ignore')
	
	return data

def get_article_code( json_data ):

	decoded = json.loads(json_data)
	pageids = decoded['query']['pages'].keys()
	article_code = []
	for pageid in pageids:

		article_code.append( decoded['query']['pages'][pageid]['revisions'][0]['*'] )

	return article_code





if __name__ == '__main__':
	
	article_name = sys.argv[1]
	
	query = form_query( article_name )
	json_data = get_json_data( query )
	code = get_article_code( json_data )
	for article in code:
		print article
