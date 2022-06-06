import configuration

from flask import Flask, render_template

app = Flask(__name__)
res = configuration.Response()

@app.route('/')
def index():
    data = res.get_top_rated_movies()
    return render_template('index.html', data = data)

@app.route('/details/<movie_id>')
def details(movie_id: int):
    return f'Movie: {movie_id}'

if __name__ == '__main__':
    app.run(debug=True)
