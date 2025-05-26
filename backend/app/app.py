from flask import Flask
from routes.admin_routes import admin_routes

app = Flask(__name__)
app.register_blueprint(admin_routes)

@app.route("/")
def home():
  return"StarSon POS Backend Running"

if __name__ == "__main__":
    app.run(debug=True)
