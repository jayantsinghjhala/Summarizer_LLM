# from flask_cors import CORS
from app import create_app

app = create_app()
# CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, credentials=True)
# cors_options = {
#     "origins": "http://localhost:3000",
#     "supports_credentials": True,
#     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     "allow_headers": ["Content-Type", "Authorization"]
# }

# CORS(app, resources={r"/*": cors_options})
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


if __name__ == '__main__':
    app.run(debug=True)