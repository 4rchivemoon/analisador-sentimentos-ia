from flask import Flask, render_template
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
