from Backend.models import *
from Backend.BookManager.Recommendation import *
from Backend.Services.Services import send_push
from Backend.serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
import json, urllib


class AllBooks(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AllGenres(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


def getBookFromGoogle(isbn):
    try:
        book = Book.objects.filter(isbn=isbn).first()
        if book != None:
            return (0, book)
        url = ("https://www.googleapis.com/books/v1/volumes?q=" + isbn + "&key=AIzaSyCy5MFc-rA39C8jBHS1q0cNHZHS4nPw8jQ")
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        items = data['items'][0]
        item = items['volumeInfo']
        author = ""
        for aut in item['authors']:
            author += aut + ", "
        item['author'] = author
        item['photo'] = item['imageLinks']['smallThumbnail']
        item['isbn'] = isbn
        book = bookParser(item)
        return (0, book)
    except Exception as e:
        return (1, None)


def bookParser(data):
    name = data.get("name", "")
    if len(name) == 0:
        name = data.get('title')
    author = data["author"]
    description = data["description"]
    photo = data.get("photo", "")
    isbn = data["isbn"]
    genres = data.get("genres", [])
    book = Book.objects.create(name=name, author=author, description=description, isbn=isbn, photo=photo)
    if len(genres) == 0:
        book.genre.add(Genre.objects.get(name='Science'))
    for genre in genres:
        genre_book = Genre.objects.filter(name__contains=genre).first()
        if genre_book == None:
            genre_book = Genre.objects.filter(name__contains='Science')
        book.genre.add(genre_book)
    belong_id = data.get('belong', "")
    if len(belong_id):
        person = Person.objects.get(id=belong_id)
        book.belong = person
        person.read.add(book)
        person.save()
    book.save()

    return book


def finish_book(request):
    try:
        isbn = request.GET.get('isbn')
        book = Book.objects.get(isbn=isbn)
        book.reader = None
        book.save()
        return JsonResponse({'code': 0})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})

#+
def addBook(request):
    try:
        isbn = request.GET.get('isbn')
        code, book = getBookFromGoogle(isbn)
        if code != 0:
            return JsonResponse({'code': 1})

        belong_id = request.GET.get('belong_id')
        belong = Person.objects.get(id=belong_id)
        book.belong = belong
        book.save()
        if code != 0:
            return JsonResponse({'code': 1})
        serializer = BookSerializer(book, many=False)
        return JsonResponse({'code': 0, 'book': serializer.data})

    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})

#+
def getInformationAboutBook(request):
    try:
        isbn = request.GET.get('isbn')
        code, book = getBookFromGoogle(isbn)

        return JsonResponse({'code': 1, 'book': BookSerializer(book, many=False).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


#-?
def search(request):
    try:
        name = request.GET.get("name", "")
        genre = request.GET.get("genre", "")
        books = Book.objects.filter(name__contains=str(name), genre__name__contains=str(genre)).distinct()
        serializer = BookSerializer(books, many=True)
        return JsonResponse({'code': 0, 'size': len(books), 'books': serializer.data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


#+
def add_rating(request):
    try:
        book_id = request.GET.get('book_id')
        rating = request.GET.get('rating')
        book = Book.objects.get(id=book_id)
        x = book.raiting + rating
        y = book.raiting_count
        x = x * y
        y += 1
        x = x / (1.0 * y)
        book.rating = x
        book.rating = x
        book.rating_count = y
        book.save()
        serializer = BookSerializer(book, many=False)
        return JsonResponse({'code': 0, 'book': serializer.data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


def free_books(request):
    try:
        free_books = Book.objects.filter(reader__isnull=True)
        return JsonResponse({'code': 0, 'books': BookSerializer(list(free_books), many=True).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


#+
def add_comment(request):
    try:
        book_id = request.GET.get('book_id')
        text = request.GET.get('text')
        author_id = request.GET.get('author_id')

        author = Person.objects.get(id=author_id)
        book = Book.objects.get(id=book_id)

        comment = Comment.objects.create(text=text, author=author)
        book.comments.add(comment)
        book.save()
        return JsonResponse({'code': 0, 'comment': CommentSerializer(comment, many=False).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


def my_books(request):
    try:
        belong_id = request.GET.get('belong_id')
        belong = Person.objects.get(id=belong_id)
        books = Book.objects.filter(belong=belong)
        return JsonResponse({'book': BookSerializer(books, many=True).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


def my_reading_books(request):
    try:
        belong_id = request.GET.get('reader_id')
        belong = Person.objects.get(id=belong_id)
        books = Book.objects.filter(reader=belong)
        return JsonResponse({'book': AllBookSerializer(books, many=True).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})

# -----> Recommendation <-----


def recommendMe(request):
    try:
        consumer_id = request.GET.get('consumer_id')
        consumer = Person.objects.get(id=consumer_id)
        read_books = consumer.read.all()
        if len(read_books):
            for i in read_books:
                array = pearson(i.isbn)
                array = final_c(i.isbn, array)
            return JsonResponse({'code': 0, 'books': BookSerializer(list(array), many=True).data})
        else:
            a = pearson("0440234743")
            a = final_c("0440234743", a)
            return JsonResponse({'code': 0, 'books': BookSerializer(list(a), many=True).data})

    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


#  ----> related books <----

def related_books(request):
    try:
        isbn = request.GET.get('isbn')
        array = pearson(isbn)
        array = final_c(isbn, array)
        return JsonResponse({'code': 0, 'books': BookSerializer(list(array), many=True).data})
    except Exception as e:
        isbn = request.GET.get('isbn')
        book = Book.objects.get(isbn=isbn)
        genre = book.genre.filter().first()
        books = Book.objects.filter(genre=genre).exclude(id=book.id)[:5]
        return JsonResponse({'code': 0, 'books': BookSerializer(list(books), many=True).data})
        # return JsonResponse({'code': 40, 'message': e.message})
    

#  ----> messaging <----


def changeCurrentReaderRequest(request):
    try:
        isbn = request.GET.get('isbn')
        book = Book.objects.get(isbn=isbn)

        consumer_id = request.GET.get('consumer_id')
        consumer = Person.objects.get(id=consumer_id)
        book.history.add(consumer)
        book.requesters.add(consumer)
        owner = book.belong
        reader = book.reader
        title = consumer.name + "requested the book"
        text = "Please tap to here to answer."
        body = {}
        to = ""
        if owner is None:
            if reader is None:
                book.reader = consumer
                book.requesters.clear()
                book.save()
                communty = Community.objects.create(author=consumer, book=book)
                return JsonResponse({'code': 0, 'book': BookSerializer(book, many=False).data})
            else:
                to = reader.token
        else:
            if reader is None:
                to = owner.token
            else:
                to = reader.token
        send_push(title, text, body, to)
        book.save()
        Message.objects.create(author=consumer, recipient=owner, text=title, status=0, book=book)
        return JsonResponse({'code': 1, 'message': 'OK'})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


def changeCurrentReaderAccept(request):
    isbn = request.GET.get('isbn')
    consumer_id = request.GET.get('consumer_id')

    book = Book.objects.get(isbn=isbn)
    consumer = Person.objects.get(id=consumer_id)
    owner = book.belong
    reader = book.reader

    text = "Tap to here to continue."
    body = {}

    if reader is None:
        reader = owner

    if reader != owner:
        title = "Dear, " + owner.name + " your book changed reader to" + consumer.name
        send_push(title, text, body, consumer.token)
        Message.objects.create(author=reader, recipient=owner, text=title, status=3, book=book)

    title = "Dear, " + consumer.name + " your request was accepted"

    Message.objects.create(author=reader, recipient=consumer, text=title, status=1, book=book)
    message = Message.objects.filter(author=consumer, status=0, book=book).first()
    if message:
        message.status = 1
        message.save()

    messages = Message.objects.filter(book=book)
    for message in messages:
        if message.status == 0:
            message.status = 2
            message.save()

    book.reader = consumer
    book.history.add(consumer)
    book.requesters.clear()
    consumer.read.add(book)

    consumer.save()
    book.save()

    Community.objects.create(author=consumer, book=book)
    send_push(title, text, body, consumer.token)

    return JsonResponse({'code': 0, 'message': 'ok'})


def changeCurrentReaderDecide(request):
    isbn = request.GET.get('isbn')
    book = Book.objects.get(isbn=isbn)

    consumer_id = request.GET.get('consumer_id')
    consumer = Person.objects.get(id=consumer_id)

    send_push("Sorry, " + consumer.name + " but your request was decided", "Tap to here to continue.", {},
              consumer.token)
    message = Message.objects.get(book=book, consumer=consumer)
    message.status = 2
    message.save()

    book.requesters.remove(consumer)
    book.save()
    return JsonResponse({'code': 0, 'message': 'ok'})


def message_get(request):
    try:
        user_id = request.GET.get('user_id')
        user = Person.objects.get(id=user_id)
        send = Message.objects.filter(author=user)
        received = Message.objects.filter(recipient=user)
        all = (send | received).distinct()
        return JsonResponse({'code': 0, 'chat': MessageSerializer(all, many=True).data})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})


