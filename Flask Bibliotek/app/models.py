from app import db

#modellerna för att skapa databasen
class Book(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    summary= db.Column(db.String, nullable= False)
    genre = db.Column(db.String, nullable=False)
    reviews= db.relationship('Review', backref='books', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user= db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column (db.Text, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


