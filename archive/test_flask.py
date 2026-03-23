from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>IT WORKS!</h1><p>Flask is running correctly.</p>'

@app.route('/test')
def test():
    return 'Test page works!'

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TEST SERVER")
    print("Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
