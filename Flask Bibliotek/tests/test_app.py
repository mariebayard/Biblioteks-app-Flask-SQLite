import pytest
from app import app,db
from app.models import Book, Review
import os
import json

#test för metoden GET för endpoint /books
def test_get_books_filtered(client):
    #test för GET för /books och att alla böcker inkluderas i svaret
    books= client.get('/books')
    assert books.status_code==200
    data= books.get_json()
    assert len(data)==4

    #test för GET för books?title= 
    title= client.get('/books?title=Test1')
    assert title.status_code == 200
    data = title.get_json()
    assert len(data)==1
    assert data[0]=={'author':'Author test1','average_rating':3.0, 'genre':'genre1', 'summary':'Summary1', 'title':'Test1'}

    #test för GET för books?author= 
    author=client.get('/books?author=Author test1')
    assert author.status_code ==200
    data = author.get_json()
    assert len(data) == 1
    assert data[0]=={'author':'Author test1','average_rating':3.0, 'genre':'genre1', 'summary':'Summary1', 'title':'Test1'}

    #test för GET för books?genre= 
    genre= client.get('/books?genre=genre2')
    assert genre.status_code == 200
    data= genre.get_json()
    assert len(data)==3
    assert {'author':'Author test2','average_rating':3.0, 'genre':'genre2', 'summary':'Summary2', 'title':'Test2'} in data

#test för metoden POST för endpoint /books
def test_post_book_to_db(client):
    #test för korrekt angiven data till POST books
    new_book = [{'title': 'Book1', 'author': 'Author1', 'summary' : 'summary1', 'genre': 'genre1'}]
    posted_book= client.post('/books',json=new_book)
    assert posted_book.status_code == 200
    assert posted_book.get_json()=={'message':'Book/Books added successfully'}

    #kontrollerar att boken är tillagd och att bokdatan som lagts till finns i databasen.
    with app.app_context():
        book_added= db.session.query(Book).filter_by(title='Book1').first()
        assert book_added.title=='Book1'
        assert book_added.author=='Author1'
        assert book_added.summary=='summary1'
        assert book_added.genre=='genre1'
    
    #test för POST till books när data i inputen saknas
    new_book_missing_data= [{'title': 'Book2'}]
    post_book_missing_data= client.post('/books', json=new_book_missing_data)
    assert post_book_missing_data.status_code == 400
    assert post_book_missing_data.get_json() =={'message' :'No books added. Some books have missing data. You need to fill in title, author, summary and genre. Please check and try again'}

#test för metoden GET för ett specifikt bok-id
def test_get_book_by_id(client):
    #test för GET för ett befintligt bok_id
    get_book= client.get('/books/2')
    assert get_book.status_code ==200
    data = get_book.get_json()
    assert data== {'author':'Author test2','average_rating':3.0, 'book_id':2, 'genre':'genre2', 'summary':'Summary2', 'title':'Test2'}

    #test för GET för ett icke befintligt bok_id och att meddelandet returneras i detta fall.
    get_book_non_existing_id = client.get('/books/200')
    assert get_book_non_existing_id.status_code==404
    assert get_book_non_existing_id.get_json() =={"message":"Book id does not exist"}

#test för metoden PUT för ett specifikt bok-id
def test_put_book_by_id(client):
    #test för PUT för ett befintligt bok-id
    put_book=client.put('/books/2', json={'title' : 'Updated Test2'})
    assert put_book.status_code== 200
    assert put_book.get_json() == {"message":"Book uppdated successfully"}

    #kontrollerar att boken har uppdaterats och att förändringen har gått igenom i databasen.
    with app.app_context():
        get_updated_book= db.session.query(Book).filter_by(id=2).first()
        assert get_updated_book.title == 'Updated Test2'

    #test för PUT för ett icke befintligt bok-id och att vi då får rätt meddelande returnerat
    put_book_non_existing_id = client.put('/books/200', json= {'title' :'Updated Test200'})
    assert put_book_non_existing_id.status_code==404
    assert put_book_non_existing_id.get_json() == {"message":"Book id does not exist"}

#test för metoden DELETE för ett specifikt bok-id
def test_delete_book_by_id(client):
    #test för DELETE för befintligt bok-id
    deleted_book=client.delete('books/4')
    assert deleted_book.status_code == 200
    assert deleted_book.get_json() == {"message":"Book deleted successfully"}

    #kontrollera att boken har tagits bort
    with app.app_context():
        deleted_book= db.session.query(Book).filter_by(id=4).first()
        assert deleted_book is None

    #test för DELETE för ett icke befintligt bok-id och att vi då får rätt meddelande returnerat
    delete_book_non_existing_id= client.delete('/books/200')
    assert delete_book_non_existing_id.status_code ==404
    assert delete_book_non_existing_id.get_json() == {"message":"Book id does not exist"}

#test för metoden POST för att lägga till en review
def test_post_review_to_db(client):
    #test för POST review, med korrekt indata
    post_review = client.post('/reviews', json={'user':1, 'rating':3, 'text': 'Not the best I have read', 'book_id':1})
    assert post_review.status_code ==200
    assert post_review.get_json() == {"message":"Review added successfully"}

    #Kontrollera att reviewn har blivit tillagd och att den förväntade datan finns i databasen
    with app.app_context():
        added_review= db.session.query(Review).filter_by(id=5).first()
        assert added_review.user == 1
        assert added_review.rating ==3
        assert added_review.text == 'Not the best I have read'
        assert added_review.book_id ==1

    #test för POST utan att fylla i alla attribut, kontroll att meddelandet om att fylla i allt returneras
    post_review_missing_values = client.post('/reviews', json = {'user':1})
    assert post_review_missing_values.status_code==400
    assert post_review_missing_values.get_json()== {"message":"You need to fill in user, rating and book_id to complete your review, please try again"}

    #test för POST om bok-id inte finns
    post_review_non_existing_book_id= client.post('/reviews', json={'user':1, 'rating':3, 'text': 'Not the best I have read', 'book_id':200})
    assert post_review_non_existing_book_id.status_code == 404
    assert post_review_non_existing_book_id.get_json()=={'message': 'Book id does not exist. Please check the id and try again.'}

#test för metoden GET på alla recensioner från databasen
def test_get_reviews_from_db(client):
    get_review= client.get('/reviews')
    assert get_review.status_code ==200
    data= get_review.get_json()
    assert len(data) ==4
    assert data[0]== {'book_id': 1, 'rating': 4, 'text': 'Quite good book','user':1 }

#test för metoden GET för recensioner för specifikt bok-id
def test_get_review_by_book_id(client):
    #test för GET för befintligt bok-id
    get_review = client.get('/reviews/1')
    assert get_review.status_code == 200
    data = get_review.get_json()
    assert len(data) == 2
    assert {'book_id': 1, 'rating': 4, 'text': 'Quite good book', 'user':1 } in data
    assert {'book_id': 1, 'rating': 2, 'text': 'Quite good book', 'user':3 } in data

    #test för GET för recensioner för ett icke befintligt bok-id
    get_review_non_existing_book_id = client.get('/reviews/200')
    assert get_review_non_existing_book_id.status_code ==404
    assert get_review_non_existing_book_id.get_json()=={'message':'Book id does not exist'}

#test för metoden GET för de 5 böckerna med högst betyg
def test_top_five_books(client):
    get_top_five = client.get('/books/top')
    assert get_top_five.status_code ==200
    data= get_top_five.get_json()
    titles_expected = {'Test1', 'Test2','Test3','Test4'}
    for title in data:
        assert title['title'] in titles_expected

#test för metoden GET för externa APIer för att få info om författaren samt lista på dennes mest kända verk.
#här mockas beroende av det externa APIet med mocker.patch('requests.get')
from app.routes import get_author_info_books    
def test_get_author_info_books(mocker):
    mocker.patch('requests.get').return_value.json.return_value={
        'extract': 'Test author summary',
        'docs':[{'top_work': 'Book test1'}, {'top_work': 'Book test2'}]
    }
    with app.test_request_context():
        response= get_author_info_books('test','testsson')
        assert response.get_json() == {'Author summary': 'Test author summary',
                                        'Most famous books':['Book test1', 'Book test2']}
