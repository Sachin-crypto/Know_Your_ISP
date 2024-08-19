from flask import Flask, render_template
from home import home_bp
from share import share_bp
from search import search_bp

app = Flask(__name__)

# Registering route blueprints
app.register_blueprint(home_bp)
app.register_blueprint(share_bp)
app.register_blueprint(search_bp)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
