from project import app
from flask import render_template

app.app_context().push()

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404)
def error_404(e):
   return render_template("404.html")

if __name__=='__main__':
    app.run(debug=True)