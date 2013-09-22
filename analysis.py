import article
import wikiclean
import re
import sys

if __name__ == "__main__":
	article_name = sys.argv[1]


def scan_heading( stream , pos):

	j = pos + 1
	count = 1
	while stream[j] == '=':
		count += 1
		j += 1


	if not count > 1:
		return None

	occurs = [m.start() for m in re.finditer( r'='*count , stream )]

	heading = stream[ occurs[0] : occurs[1] ].rstrip('=').lstrip('=')

	# if len(occurs) > 3:
	# 	# body = stream[ occurs[1] + count : occurs[2] ]
	# 	remainder = stream[ occurs[2] + count : ]
	# elif len(occurs) == 2:
	# 	# body = stream[ occurs[1] : ]
	# 	remainder = ''
	# else:
	# 	print "ERROR"

	remainder = stream[occurs[1] + count : ]


	return  [ [ count , heading ] , remainder ]



def read( stream ):

	start = 0
	for i in range( len( stream ) ) :


		if stream[i] == '=':
		
			heading = scan_heading( stream , i )
			if heading == None:
				continue

			return [stream[:i]] + heading

	return [ stream, None , None ]
	
#node structure: [ parent , heading , [ node , node , node ] ]
def create_tree( headings ):

	text , this_level , this_heading = headings[0]
	del headings[0]
	tree = [ [this_heading , text] ]
	while len(headings) > 0:

		text , level, heading = headings[0]
	
		if level > this_level:
			tree.append( create_tree( headings ) )
		if level == this_level:
			tree.append( [heading , text ] )
			del headings[0]
		if level < this_level:
			return tree
	return tree


code = '==heading 1== text ===sub=== subtext ===sub=== more subtext ==heading 2== text'
# print code

def get_sections( code ):
	inter , heading , code = read(code)
	headings = []
	inters = []
	while [heading, code] != [ None , None ]:
		headings.append( heading )
		inters.append( inter )
		inter,heading,code = read(code)
	inters.append(inter)




	# print "headings: ", headings
	# print "inters: ", inters[1:]
	# print "zip: ",zip( headings , inters[1:])
	headings = [ [i] + h for h,i in zip( headings , inters[1:]) ]

	# print "headings: ", headings
	return create_tree(headings)

# print get_articles( code )


pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,

	[ "html_has_been_stripped" , lambda data:  [ wikiclean.strip_html(data) , wikiclean.strip_html(data) ] ] , 

	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 

	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ] ,


]


a = article.Article( article_name , pipeline )



# a.processed =  a.processed.encode('utf-8')
# print a.processed
print get_sections(a.processed)[1]



=======
# print a.html_has_been_stripped
print a.processed.encode('utf-8')

