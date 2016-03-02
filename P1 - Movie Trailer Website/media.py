#Create a Movie Structure
class Movie:
	def __init__(self, movie_data):
		self.title = movie_data['title']
		self.poster_image_url = movie_data['poster_image_url']
		self.trailer_youtube_id = movie_data['trailer_youtube_id']
		self.trailer_youtube_url = movie_data['trailer_youtube_url']