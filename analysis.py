import article
import wikiclean
import re
import sys

if __name__ == "__main__":
	article_name = sys.argv[1]


pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,

	[ "html_has_been_stripped" , lambda data:  [ wikiclean.strip_html(data) , wikiclean.strip_html(data) ] ] , 

	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 

	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ] ,


]


a = article.Article( article_name , pipeline )


# print a.html_has_been_stripped
print a.processed.encode('utf-8')

