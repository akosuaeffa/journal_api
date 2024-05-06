from models import *
from user_routes import *
from entry_routes import *

db.init_app(app)

with app.app_context():
    db.create_all()
 
if __name__ == "__main__":
    app.run(debug=True)