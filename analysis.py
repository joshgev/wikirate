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

	remainder = stream[occurs[1] + count : ]


	return  [ [ count , heading.rstrip().lstrip() ] , remainder ]



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
	# tree = [ [this_heading , text] ]
	tree = { this_heading : { 'text' : text } }
	current_heading = this_heading
	while len(headings) > 0:

		text , level, heading = headings[0]
	
		if level > this_level:
			# tree.append( create_tree( headings ) )
			tree[ current_heading ][ 'sub' ] = create_tree( headings )

		if level == this_level:
			# tree.append( [heading , text ] )
			tree[ heading  ] = { 'text' : text }
			current_heading = heading
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

	headings = [ [i] + h for h,i in zip( headings , inters[1:]) ]


	return create_tree(headings)




pipeline = [ 
	
	[ None , lambda data: [ re.sub(r"\n", '' , data) ,  None  ] ] ,

	[ "html_has_been_stripped" , lambda data:  [ wikiclean.strip_html(data) , wikiclean.strip_html(data) ] ] , 

	[ None , lambda data: [ wikiclean.strip_curlys(data) , None] ] , 

	[ "processed" , lambda data:  [ wikiclean.strip_wikilinks(data) , wikiclean.strip_wikilinks(data)   ] ] ,


]


a = article.Article( article_name , pipeline )



# a.processed =  a.processed.encode('utf-8')
# print a.processed
# for i in get_sections( a.processed ):
	# print i


sections = get_sections(a.processed )
for i in  sections.keys():
	print i
	if 'sub' in  sections[i].keys():
		for j in sections[i]['sub'].keys():
			print '\t',j



# print a.html_has_been_stripped
# print a.processed.encode('utf-8')

