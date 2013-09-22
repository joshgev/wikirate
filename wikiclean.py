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
	data = data + ' '
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




#this function removes everything of the form [[File.....]]

def strip_tables( data ):
	data = data + ' '
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

	level0 = strip_File_tags( data )
	level0 = strip_tables( level0 )

	r = "\[\[[^\[]+?\|([^\|]*?)\]\]"
	level1 = re.sub(r, function2, level0)

	r = "\[\[([^\|]+?)\]\]"
	level2 = re.sub(r, function2, level1)

	return level2
	




#this function gets rid of everything between html tags <ref...>. The most common occurrance is <ref> ... </ref>, however there are also cases that begin with <ref name=...> and then have a closing ref tag. There are also some special cases which don't have a closing ref tag; they are of the form <ref ... />, and these are removed entirely.

def strip_ref_tags( data ):
	data = data + ' '
	count = 0
	counting = False
	after_first_tag = False
	last_write = 0
	final = ""
	i = 0
	while i < len(data) - 1:
		if i < len(data) - 4 and count == 0 and data[i:i+4] =='<ref':
			counting = True
			final += data[last_write : i]
			count += 1
			i += 4
		elif counting and data[i] == '<':
			count += 1
			i += 1
		elif counting and data[i] == '>':
			count -= 1			
			if after_first_tag == False and count == 0:
				if data[i-1] == '/':
					counting = False
					last_write = i + 1
				else:
					after_first_tag = True
			elif after_first_tag == True and count == 0:
				after_first_tag = False
				counting = False
				last_write = i + 1
			i += 1
		else:
			i += 1
	
	return final + data[last_write:]




#this function gets rid of wikitag references of the form [http:....], and it also replaces wikitag references of the form [http:....  sth] with "sth"

def strip_http_links( data ):
	data = data + ' '
	count = 0
	counting = False
	after_space = False
	last_write = 0
	final = ""
	i = 0
	while i < len(data) - 1:
		if i < len(data) - 5 and i > 0 and count == 0 and data[i-1] != '[' and data[i:i+5] =='[http':
			counting = True
			final += data[last_write : i]
			count += 1
			i += 5
		elif counting and after_space == False and data[i] == ' ':
			after_space = True
			last_write = i+1
			i += 1
		elif counting and data[i] == '[':
			count += 1
			i += 1
		elif counting and data[i] == ']':
			count -= 1
			if after_space == False and count == 0:
				counting = False
				last_write = i+1
			elif after_space == True and count == 0:
				after_space = False
				counting = False
				final += data[last_write: i]
				last_write = i + 1
			i += 1
		else:
			i += 1
	
	return final + data[last_write:]





#r1 gets rid of html comments and r2 gets rid of html tags

def strip_html( data ):
	#<tagname some_option=''> some stuff </tagname>
	#<tag />
	#<p>dfs</p>   good stuff <p>sdfkjdf</p>

#	function2 = lambda x:  x.group(1)
	data = re.sub(r"&nbsp;", " ", data)
	
	r1 = r"<!--.*?-->"
	level1 = re.sub(r1, "", data)

	level1 = strip_ref_tags( level1 )
	
	r2 = r"<[^>]+?>"	
	level2 = re.sub( r2 , "" , level1 )

#	r3 = r"[^\[]\[http[^\ ]*\ ([^\]])*?\][^\]]"
	level3 = strip_http_links( level2 )
	
	#r2 = r"<[\ ]*[^>\ /]+>"	
	#level2 = re.sub( r2 , "" , level1)
	
	#r3 = r"<[^>]+/>"
	#level3 = re.sub( r3 , "" , level2b )
	return level3


def clean( data ):
	data = re.sub(r"\n", '' , data)
	#return strip_html(  strip_wikilinks (strip_curlys( strip_langs(  data)  ) ) )
	return strip_wikilinks( strip_curlys( strip_html( data ) ) )
