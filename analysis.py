import article
import wikiclean
import re
import sys
import sections

if __name__ == "__main__":
	article_name = sys.argv[1]




pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,

	[ None , lambda data:  [ wikiclean.strip_html(data) , None ] ] , 

	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 

	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ] ,

	[ "sections" , lambda data: [ data , sections.get_sections(data) ] ] ,

]


a = article.Article( article_name , pipeline )



# a.processed =  a.processed.encode('utf-8')
# print a.processed
# for i in get_sections( a.processed ):
	# print i


sections = a.sections
for i in  sections.keys():
	print i
	if 'sub' in  sections[i].keys():
		for j in sections[i]['sub'].keys():
			print '\t',j.encode('utf-8')



# print a.html_has_been_stripped
print a.processed.encode('utf-8')

