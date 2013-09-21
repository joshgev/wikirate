import wikidownload
import wikiclean

class Article:

	def __init__( self , name , pipeline ):

		self.raw = wikidownload.get_article_code_from_name( name )


		self.pipeline = pipeline

		self.run_pipeline()

	def run_pipeline( self ):

		data = self.raw

		

		for member_name , process in self.pipeline:

			
			data , member_value = process( data )


			if member_name and member_value:
				setattr( self , member_name , member_value)
				







