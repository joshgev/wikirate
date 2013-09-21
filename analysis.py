import article
import wikiclean
import re


pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,

	[ "html_has_been_stripped" , lambda data:  [ wikiclean.strip_html(data) , wikiclean.strip_html(data) ] ] , 

	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 

	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ] ,


]


a = article.Article( 'Jesus' , pipeline )


# print a.html_has_been_stripped
print a.processed.encode('utf-8')
