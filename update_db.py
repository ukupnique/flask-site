from test_flask import create_app
from test_flask import db
app = create_app()
app.app_context().push()
#db.drop_all()
db.create_all()