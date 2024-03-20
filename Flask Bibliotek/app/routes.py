from flask import request, jsonify
from sqlalchemy.sql import func
from app import app, db
from app.models import Book, Review
import functools
import threading
import requests

#decorator som skriver ut vilken body POST-requesten har
def print_body(func):
    @functools.wraps(func)
    def wrapper_func(*args,**kwargs):
        if request.method=='POST':
            print (request.json)
        return func(*args,**kwargs)
    return wrapper_func

#endpoint för /books med metoderna GET och POST
@app.route('/books', methods=['GET','POST'])
@print_body
def get_books_by_filter():
    try:
        if request.method== 'GET':
            #kontrollerar argumenten som skrivs in för title, author och genre. Om argumentet inte
            #förekommer blir värdet för den parametern None
            title=request.args.get('title',None)
            author=request.args.get('author',None)
            genre=request.args.get('genre',None)
            books_query=db.session.query(Book)

            #lägger till filter på queryn beroende på parametrarna
            if title != None:
                books_query= books_query.filter_by(title=title)
            if author != None:
                books_query=books_query.filter_by(author=author)
            if genre != None:
                books_query=books_query.filter_by(genre=genre)

            #lägger till average rating på böckerna som filtrerats fram
            books_info=(books_query.outerjoin(Review, Book.id ==Review.book_id)
                        .add_columns(func.avg(Review.rating).label ('average_rating'))
                        .group_by(Book.id).all())
            
            #skapar en lista med dictionaries för alla böcker som filtrerats fram
            books_dict=[{'title': book.title, 'author': book.author, 'summary':book.summary,
                          'genre': book.genre, 'average_rating': average_rating} for book,average_rating in books_info]
            return jsonify(books_dict)
        
        elif request.method=='POST':
            data= request.json
            #sätter värdet på all_books_valid_data för att kunna kontroller om något 
            #saknas i inputen när en bok ska Postas
            all_books_valid_data = True

            #kontrollerar om nödvändig info finns i samtliga böcker som ska postas.
            for book_data in data:
                if 'title' not in book_data or 'author' not in book_data or 'summary' not in book_data or 'genre' not in book_data:
                    all_books_valid_data=False
                    break
            
            #Om all data som behöver finnas finns i bodyn som skrivits in så läggs samtliga böcker till och meddelande returneras
            if all_books_valid_data:
                for book_data in data:
                    new_book= Book(title=book_data.get('title'), author= book_data.get('author'), summary= book_data.get('summary'), genre= book_data.get('genre'))
                    with app.app_context():
                        db.session.add(new_book)
                        db.session.commit()
                return jsonify({'message':'Book/Books added successfully'})
            #Om inte all nödvändig info finns i bodyn läggs inga böcker till utan användaren får kontrollera input
            else:
                return jsonify({'message' :'No books added. Some books have missing data. You need to fill in title, author, summary and genre. Please check and try again'}), 400
    except Exception as e:
        return jsonify({'error': f'Error:{str(e)}'})
    finally:
        db.session.close()

#endpoint för /books/<book_id> med metoderna GET, PUT och DELETE
@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def get_book_by_id(book_id):
    try:
        #kontroll för att se om bok id finns
        book= db.session.query(Book).filter_by(id=book_id).first()
        if book:
            if request.method == 'GET':
                #query för att ta fram bokdatan samt lägga till average rating från databasen   
                book_rating=(db.session.query(Book.id, Book.title, Book.author, Book.summary,
                                    Book.genre, func.avg(Review.rating).label('average_rating'))
                                    .outerjoin(Review,Book.id==Review.book_id)
                                    .filter(Book.id==book_id)
                                    .group_by(Book.id).first())

                #skapar ett dictionary för datan vi är intresserade av att returnera
                book_data= {'book_id':book_rating.id, 'title': book_rating.title, 'author':book_rating.author,
                             'summary':book_rating.summary, 'genre': book_rating.genre, 'average_rating':book_rating.average_rating}
                return jsonify(book_data)
            
            elif request.method == 'PUT':
                data = request.json
                #kontorllerar vilka parametrar som finns i bodyn. Om en viss parameter inte finns
                #behålls det tidigare värdet i databasen.
                book.title= data.get('title', book.title)
                book.author= data.get('author', book.author)
                book.summary = data.get('summary', book.summary)
                book.genre= data.get('genre', book.genre)
                #lägger till ändringarna i databasen och meddelandet returneras
                db.session.commit()
                return jsonify({'message': 'Book uppdated successfully'})
            
            elif request.method =='DELETE':
                #raderar boken med angivet bok-id från databasen och meddelandet returneras
                db.session.delete(book)
                db.session.commit()
                return jsonify({'message': 'Book deleted successfully'})
        else: 
            #om angivet bok id inte finns i databasen returneras detta meddelande
            return jsonify({'message': 'Book id does not exist'}), 404
    except Exception as e: 
        return jsonify({'error': f'Error:{str(e)}'})
    finally:
        db.session.close()

#endpoint för /reviews med metoderna GET och POST
@app.route('/reviews', methods=['GET', 'POST'])
@print_body 
def get_post_review():
    try:
        if request.method =='GET':
            #hämtar alla reviews från databasen, lägger till dem i en lista med dictionaries
            #för varje review och returnerar listan
            review_query=db.session.query(Review).all()
            review_dict=[{'user': review.user, 'rating':review.rating, 'text': review.text,
                           'book_id':review.book_id} for review in review_query]
            return (review_dict)
        
        elif request.method =='POST':
            data= request.json
            #kontrollerar om något saknas i inputen från användaren
            if 'user' not in data or 'rating' not in data or 'book_id' not in data:
                return jsonify({'message': 'You need to fill in user, rating and book_id to complete your review, please try again'}), 400
            else:
                #kontrollerar om angivet bok-id i reviewn finns i Book databasen. Om inte returneras meddelandet 
                #då recensioner för obefintliga böcker inte tillåts.
                book_id=data.get('book_id')
                if not db.session.query(Book.id).filter_by(id=book_id).first():
                    return jsonify({'message': 'Book id does not exist. Please check the id and try again.'}), 404
                else:
                    #Om inputen är korrekt och bok id finns läggs recensionen till i databasen och meddeladnet returneras
                    new_review= Review(user=data.get('user'), rating= data.get('rating'), text= data.get('text'), book_id= data.get('book_id'))
                    with app.app_context():
                        db.session.add(new_review)
                        db.session.commit()
                    return jsonify({'message':'Review added successfully'})
    except Exception as e:
         return jsonify({'error': f'Error:{str(e)}'})
    finally:
        db.session.close()

#Endpoint för /reviews/<book_id> med metoden GET
@app.route('/reviews/<book_id>', methods= ['GET'])
def get_review_by_id(book_id):
    try:
        #kontrollerar att angivet bok-id finns i databasen, om inte returneras ett meddelande
        book= db.session.query(Book).filter_by(id=book_id).first()
        if not book:
            return jsonify({'message':'Book id does not exist'}), 404
        
        #hämtar alla recensioner för böckerna med angivet bok-id
        book_reviews= db.session.query(Review).filter_by(book_id=book_id).all()

        #om det finns recensioner för boken returneras en lista med dessa
        if book_reviews:
            review_dict = [{'user': review.user, 'rating':review.rating, 'text': review.text,
                             'book_id':review.book_id} for review in book_reviews] 
            return jsonify(review_dict)
        else:
            #finns det inga recesioner för angivet bok-id returneras detta meddelande 
            return jsonify({'message': 'No reviews available for this book'})
    except Exception as e:
        return jsonify({'error': f'Error:{str(e)}'})
    finally:
        db.session.close()

#endpoint för books/top med metoden GET där de 5 böckerna med högst genomsnittligt betyg hämtas.
@app.route('/books/top', methods= ['GET'])
def top_five_books():
    try:
        #tar fram Bokinfo och average rating, order_by average rating i fallende ordning och limit för att få de 5 med högst genomsnittligt betyg
        top_query= (
            db.session.query(Book, func.avg(Review.rating).label('avarage_rating'))
                    .join(Review)
                    .group_by(Book)
                    .order_by(func.avg(Review.rating).desc())
                    .limit(5)
        )
        top_books= top_query.all()
        #lägger in datan från de 5 böcker med högst betyg i en lista och returnerar denna lista
        top_books_dict= [{'book_id':book.id, 'title': book.title, 'author':book.author, 'summary':book.summary,
                           'genre': book.genre, 'avarage_rating': avarage_rating} for book, avarage_rating in top_books]
        return (top_books_dict)
    except Exception as e:
        return jsonify({'error': f'Error:{str(e)}'})
    finally:
        db.session.close()

#funktion som skickar en request-förfårgan till en url(parameter) och som sedan lägger till resultatet 
#i listan som är en parameter i funktionen.
def fetch(url,result_list):
    response=requests.get(url)
    result_list.append(response.json())

author_info_URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/'
author_books_URL = 'https://openlibrary.org/search/authors.json?q='

#endpoint för /author med metoden GET som hämtar en sammanfattning om författaren och dennes mest kända verk
@app.route('/author/<firstname>/<lastname>', methods= ['GET'])
def get_author_info_books(firstname, lastname):
    try:
        fetch_results1=[]
        fetch_results2=[]
        #tråd 1 för att hämta sammanfattning om en författare och lägga till svaret i fetch_results1
        thread1=threading.Thread(target=fetch, args=(author_info_URL+firstname+'_'+lastname, fetch_results1))
        #tråd 2 för att hämta författarens mest kända verk och lägga till svaret i fetch_results2
        thread2 = threading.Thread(target=fetch, args=(author_books_URL+firstname+'%20'+lastname, fetch_results2))

        #startar förfrågan mot externa apierna
        thread1.start()
        thread2.start()

        #väntar in att båda förfrågningarnas resultat ska hämtas
        thread1.join()
        thread2.join()
  
        if 'extract' in fetch_results1[0]:
            #tar ut sammanfattningen från fetch_results1, där sammanfattningen står efter nyckeln extract
            author_info_summary=fetch_results1[0].get('extract')
        else:
            #om ingen sammanfattning finns tillgänglig från externa apiet så sparas ett meddelande i variabeln
            author_info_summary= 'No summary available'

        if 'docs' in fetch_results2[0]:
            #tar ut infon under docs i svaret från fetch_results2
            author_top_books_data= fetch_results2[0].get('docs')
            #loopar igenom listan och tar ut svaret på de ställen där nyckeln är top_work förutsatt att det finns ett värde
            author_top_books=[top_books.get('top_work') for top_books in author_top_books_data if top_books.get('top_work') is not None]
        else:
            #om ingen lista med mest kända verk finns tillgänglig så sparas ett meddelande i variabeln
            author_top_books='No books available'

        #lägger ihop svaren och returnerar svaret med sammanfattning och en lista på mest berömda verk
        total_response= {'Author summary': author_info_summary,'Most famous books': author_top_books}
        return jsonify(total_response)
    except Exception as e:
        return jsonify({'error': f'Error:{str(e)}'})