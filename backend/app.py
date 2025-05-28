from flask import Flask
from routes.serve_pdf import serve_pdf_bp

app = Flask(__name__)
app.register_blueprint(serve_pdf_bp)

@app.route('/')
def home():
    return 'Backend Running'

if __name__ == '__main__':
    app.run(debug=True)
