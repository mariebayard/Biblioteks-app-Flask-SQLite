from app import app,db
from app.models import Book, Review

if __name__=="__main__":
    app.run(debug=True, port=8000)

"""
#för att skapa databasen library;
with app.app_context():
    db.create_all()

#Books;
book1= Book(title='Hamlet', author='William Shakespeare', summary='En av Shakespeares mest kända tragedier, där prins Hamlet kämpar med hämnd, förlåtelse och existentiella frågor efter faderns död.', genre= 'Tragedi')
book2 = Book(title='1984', author='George Orwell', summary='En dystopisk framtid där övervakning och kontroll är omfattande, och individer kämpar för sin frihet i en totalitär stat.', genre= 'Science Fiction')
book3= Book(title='Pride and Prejudice', author='Jane Austen', summary='En klassisk roman om Elizabeth Bennet och Mr. Darcy, och deras kamp genom sociala fördomar och förväntningar för att hitta kärlek.', genre= 'Romantik')
book4 = Book(title='Brave New World', author='Aldous Huxley', summary='En dystopisk framtid där samhället är uppdelat och kontrollerat genom genetisk manipulation och droger för att upprätthålla stabilitet.', genre= 'Science Fiction')
book5= Book(title='The Importance of Being Earnest', author='Oscar Wilde', summary='En satirisk komedi som undersöker förväxlingar och identiteter, där två vänner använder påhittade namn för att undkomma sina ansvar.', genre= 'Komedi')
book6 = Book(title='Moby Dick', author='Herman Melville', summary='Kapten Ahabs besatthet av att hämnas på den vita valen, Moby-Dick, leder hans besättning till katastrof.', genre= 'Äventyr')
book7= Book(title='Sense and Sensibility', author='Jane Austen', summary='En romantisk roman som utforskar systrarnas Elinor och Marianne Dashwoods kärleksliv och sociala förändringar i 1800-talets England.', genre= 'Romantik')
book8= Book(title='Othello', author='William Shakespeare', summary='En tragedi om svartsjuka och manipulation, där den misstänksamme Othello tvivlar på sin hustrus, Desdemonas, trohet.', genre= 'Tragedi')
book9 = Book(title='The Picture of Dorian Gray', author='Oscar Wilde', summary='En berättelse om moralisk förfall och konsekvenserna av en självcentrerad livsstil, med en magisk porträttmålning.', genre= 'Roman')
book10= Book(title='The Road', author='Cormac McCarthy', summary='En postapokalyptisk resa där en far och son kämpar för överlevnad i en ödelagd värld.', genre= 'Dystopi')
book11 = Book(title='The Hitchhikers Guide to the Galaxy', author='Douglas Adams', summary='En absurd och humoristisk science fiction-komedi som följer jordlingen Arthur Dent när han oavsiktligt tas med på en rymdresa runt galaxen av Ford Prefect, en utomjording och reseguideförfattare för "Handbok i galaxen, per anhalter genom galaxen."', genre= 'Science Fiction')
book12= Book(title='Anna Karenina', author='Leo Tolstoy', summary='En episk roman om kärlek och moral i det ryska aristokratiska samhället, med fokus på Anna Kareninas förbjudna kärlek och dess konsekvenser.', genre= 'Roman')
book13 = Book(title='The Girl with the Dragon Tattoo', author='Steig Larsson', summary='En spännande thriller där journalisten Mikael Blomkvist och hacker Lisbeth Salander arbetar tillsammans för att lösa ett gammalt mysterium om en försvunnen arvtagerska.', genre= 'Thriller')
book14= Book(title='The Grapes of Wrath', author='John Steinbeck', summary='En roman om en fattig arbetarfamilj under den stora depressionen som migrerar till Kalifornien i hopp om ett bättre liv.', genre= 'Roman')
book15= Book(title='The Shining', author='Stephen King', summary='En skräckroman som följer Jack Torrance och hans familj när de blir vaktmästare på det övergivna Overlook Hotel, där övernaturliga krafter hotar deras sinnestillstånd.', genre= 'Skräck')
book16 = Book(title='Northanger Abbey', author='Jane Austen', summary='n satirisk roman som följer Catherine Morland på hennes äventyr genom kärlek och föreställningar om gotiska romaner.', genre= 'Roman')
book17= Book(title='A Midsummer Nights Dream', author='William Shakespeare', summary='En komedi där förväxlingar och förvecklingar uppstår när feerna i skogen blandar sig i människors kärleksliv.', genre= 'Komedi')

#Reviews;
review1= Review(user='Marie', rating=5, text= 'Bästa boken jag läst', book_id=1)
review2= Review(user='Eva', rating=5, text= 'Superbra', book_id=2)
review3= Review(user='Sara', rating=3, text= 'Helt okej', book_id=3)
review4= Review(user='Kalle', rating=4, text= 'Bra bok', book_id=3)
review5= Review(user='Johannes', rating=2, text= 'Inte min typ av bok', book_id=4)
review6= Review(user='Molly', rating=1, text= 'Sämsta boken jag läst! Läs inte!', book_id=4)
review7= Review(user='Anders', rating=1, text= 'Sämsta boken någonsin', book_id=5)
review8= Review(user='Karl', rating=3, text= 'Helt okej', book_id=5)
review9= Review(user='Sara', rating=2, text= 'Den var okej', book_id=6)
review10= Review(user='Alex', rating=5, text= 'Sååå bra bok! Läs den!', book_id=6)
review11= Review(user='Johanna', rating=3, text= 'Varken bra eller dålig', book_id=4)
review12= Review(user='Jenny', rating=2, text= 'Helt okej', book_id=4)
review13= Review(user='Pelle', rating=5, text= 'Superbra', book_id=7)

#för att lägga in böcker och reviews i databasen library
with app.app_context():
    db.session.add_all([book1, book2, book3,book4,book5,book6,book7, book8, book9, book10, book11, book12, book13, book14, book15, book16, book17, review1,review2,review3,review4,review5,review6,review7,review8,review9,review10, review11,review12,review13])
    db.session.commit()"""
