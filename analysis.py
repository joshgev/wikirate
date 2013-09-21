import article
import wikiclean
import re


pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,
	[None , lambda data:  [ wikiclean.strip_html(data) , None ] ] , 
	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 
	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ]
]


a = article.article( 'Jesus' , pipeline )


print a.processed
