import flask
import os


basedir = os.getcwd()
PORT = 5000


app = flask.Flask(
    __name__,
    static_folder=os.path.join(basedir, 'website', 'static'),
    template_folder=os.path.join(basedir, 'website', 'templates'),
)


@app.route("/")
def index():
    html = flask.render_template("chess_game.html")
    # html = html.replace("((((", "{{").replace("))))", "}}")
    return html


def run_app():
    app.run(host='127.0.0.1', port=PORT, debug=True)

if __name__ == "__main__":
    run_app()