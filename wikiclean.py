import re


def strip_langs( data ):
		function2 = lambda x:  x.group(1)
		r = r"{{lang.*?\|([^\|]*)}}"
		level1=re.sub( r , function2 , data )
		r = r"{{IPA(.*?)}}"
		level2=re.sub( r , "" , level1 )
		return level2




def strip_curlys( data ):

	count = 0
	last_write = 0
	final = ""
	i = 0
	while i < len(data) - 1:
		if count == 0 and data[i] =='{' and data[i+1]=='{':
			final += data[last_write : i]
			count += 1
			i += 1
		elif data[i] == '{' and data[i+1] == '{' :
			count += 1
			i += 1

		if data[i] == '}' and data[i+1] == '}' :
			count -= 1
			if count == 0:
				last_write = i + 2

			i += 1
		i += 1

	return final + data[last_write:]


def strip_File_tags( data ):
	count = 0
	counting = False
	last_write = 0
	final = ""
	i = 0
	while i < len(data) - 2:
		if i < len(data) - 6 and count == 0 and data[i:i+6] =='[[File':
			counting = True
			final += data[last_write : i]
			count += 1
			i += 6
		elif counting and data[i:i+2] == '[[':
			count += 1
			i += 2
		elif counting and data[i:i+2] == ']]':
			count -= 1
			if count == 0:
				counting = False
				last_write = i + 2
			i += 2
		else:
			i += 1
	
	return final + data[last_write:]



def strip_tables( data ):
	count = 0
	counting = False
	last_write = 0
	final = ""
	i = 0
	while i < len(data) - 2:
		if i < len(data) - 19 and count == 0 and data[i:i+19] =='{| class="wikitable':
			counting = True
			final += data[last_write : i]
			count += 1
			i += 19
		elif i < len(data) - 18 and count == 0 and data[i:i+18] =='{|class="wikitable':
			counting = True
			final += data[last_write : i]
			count += 1
			i += 18
		elif counting and data[i:i+2] == '{|':
			count += 1
			i += 2
		elif counting and data[i:i+2] == '|}':
			count -= 1
			if count == 0:
				counting = False
				last_write = i + 2
				i += 2
		else:
			i += 1
	
	return final + data[last_write:]



def strip_wikilinks( data ):
	function1 = lambda x : x.group(1) if not x.group(2) else x.group(2)
	function2 = lambda x:  x.group(1)

	level0 = strip_File_tags( data + ' ')
	level0 = strip_tables( level0 )

	r = "\[\[[^\[]+?\|([^\|]*?)\]\]"
	level1 = re.sub(r, function2, level0)

	r = "\[\[([^\|]+?)\]\]"
	level2 = re.sub(r, function2, level1)

	return level2
	

def strip_html( data ):

	#<tagname some_option=''> some stuff </tagname>

	#<tag />
	#<p>dfs</p>   good stuff <p>sdfkjdf</p>
	data = re.sub(r"&nbsp;", " ", data)
	
	r1 = r"<!--.*?-->"
	level1 = re.sub(r1, "", data)
	
	r2 = r"<[^>]+?>"	
	level2 = re.sub( r2 , "" , level1)
	
	#r2 = r"<[\ ]*[^>\ /]+>"	
	#level2 = re.sub( r2 , "" , level1)
	
	#r3 = r"<[^>]+/>"
	#level3 = re.sub( r3 , "" , level2b )
	return level2


def clean( data ):
	data = re.sub(r"\n", '' , data)
	#return strip_html(  strip_wikilinks (strip_curlys( strip_langs(  data)  ) ) )
	return strip_wikilinks( strip_curlys( strip_html( data ) ) )
