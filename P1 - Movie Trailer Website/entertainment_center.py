import fresh_tomatoes
import media

#Movies to show with their details as dictionary
movies_data = [
	{
		'title': "Kung Fu Panda 3",
		'poster_image_url': "http://resizing.flixster.com/vgOShHA5wKjslJzyzPOPgmCNTsk=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/11/48/82/11488237_ori.jpg",
		'trailer_youtube_id': "10r9ozshGVE",
		'trailer_youtube_url': "https://www.youtube.com/watch?v=10r9ozshGVE"
	},
	{
		'title':"STAR WARS: EPISODE VII - THE FORCE AWAKENS",
		'poster_image_url': "http://resizing.flixster.com/lfzBVmZJ4DlML1HQUXUP9eJYAlU=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/11/20/33/11203306_ori.jpg",
		'trailer_youtube_id': "sGbxmsDFVnE",
		'trailer_youtube_url': "https://www.youtube.com/watch?v=sGbxmsDFVnE"
	},
	{
		'title': "Inside Out",
		'poster_image_url': "http://resizing.flixster.com/GIFSkqggG_NnJfQKMaHSTHgLwuQ=/180x266/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/05/11190503_ori.jpg",
		'trailer_youtube_id': "seMwpP0yeu4",
		'trailer_youtube_url': "https://www.youtube.com/watch?v=seMwpP0yeu4"
	}]

movies = []

#Create Movies
for x in movies_data:
	print(x)

	movies.append(media.Movie(x))

#create html and open browser
fresh_tomatoes.open_movies_page(movies)