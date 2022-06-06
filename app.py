import configuration

from flask import Flask, render_template

app = Flask(__name__)
res = configuration.Response()
print(res.top_rated_movies())

# @app.route('/')
# def index():
#     data = res.top_rated_movies()
#     return render_template('index.html', data = data)


# if __name__ == '__main__':
#     app.run(debug=True)
