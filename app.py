import configuration

from flask import Flask, render_template

app = Flask(__name__)
res = configuration.Response()

@app.route('/')
def index():
    top_rated = res.get_top_rated_movies()
    popular_movies = res.get_popular_movies()
    return render_template('index.html',
                           top_rated = top_rated, popular_movies = popular_movies)

@app.route('/details/<movie_id>')
def details(movie_id: int):
    movie_details = res.get_movie_details_by_id(int(movie_id))
    return render_template('details.html', movie_details = movie_details)



if __name__ == '__main__':
    app.run(debug=True)
