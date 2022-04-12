from home import db
class item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'{self.id} , {self.name} , {self.age}'

