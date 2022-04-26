from home import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Item.query.get(int(user_id))


class Item(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    @property
    def password_hash(self):
        return self.password
    @password_hash.setter
    def password_hash(self, passtext):
        self.password = bcrypt.generate_password_hash(passtext).decode('utf-8')

    def check_password_correct(self, attempted):
        return bcrypt.check_password_hash(self.password, attempted)

    def __repr__(self):
        return f'{self.id} , {self.name} , {self.email}'

