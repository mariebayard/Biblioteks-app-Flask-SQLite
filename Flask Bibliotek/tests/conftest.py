from dotenv import load_dotenv
import os
import pytest
from app import app, db
from app.models import Book, Review

load_dotenv()

#funktion som kör först och ger en exit om TESTING i .env-filen inte är satt till True
def pytest_sessionstart(session):
    os.environ.get('TESTING')
    if os.environ.get('TESTING') !='True':
        pytest.exit('TESTING in .env-file must be set to True to run the tests', returncode=3)

#fixture för att skapa databasen tests.
#varje test körs mot databasen och därefter rensas databasen för att testerna inte
#ska påverkas av varandra
@pytest.fixture(scope='function')
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            book_test1= Book(title ='Test1', author= 'Author test1', summary= 'Summary1', genre= 'genre1')
            book_test2= Book(title ='Test2', author= 'Author test2', summary= 'Summary2', genre= 'genre2')
            book_test3= Book(title ='Test3', author= 'Author test3', summary= 'Summary3', genre= 'genre2')
            book_test4= Book(title ='Test4', author= 'Author test4', summary= 'Summary4', genre= 'genre2')
            review_test1 = Review(user= 1, rating= 4, text= 'Quite good book', book_id= 1)
            review_test2 = Review(user= 2, rating= 3, text= 'Really good book', book_id= 2)
            review_test3 = Review(user= 3, rating= 2, text= 'Quite good book', book_id= 1)
            review_test4 = Review(user= 4, rating= 3, text= 'Really good book', book_id= 3)
            db.session.add_all([book_test1, book_test2, book_test3,book_test4, review_test1, review_test2, review_test3,review_test4])
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()        