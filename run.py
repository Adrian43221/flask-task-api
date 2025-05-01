from app import create_app
from app.extensions import db
from app.models.user import User
app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # создаёт таблицу User в базе
    app.run(debug=True)
