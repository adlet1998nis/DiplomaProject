import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from nltk.corpus import wordnet
from Backend.models import *
from Backend.serializers import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json
import urllib


class DB :
    books = pd.DataFrame()
    users = pd.DataFrame()
    ratings = pd.DataFrame()
    average_rating = pd.DataFrame()
    ratings_pivot = pd.DataFrame()


def initData():
    #void function, one time call when run server
    DB.books = pd.read_csv('Final_books.csv', sep='\t', error_bad_lines=False, encoding='utf-8')
    DB.books = DB.books[['ISBN', 'bookTitle', 'bookAuthor',
               'yearOfPublication', 'publisher', 'Genre', 'Content', 'IMG_URL']]
    DB.users = pd.read_csv('Final_users.csv', sep='\t', error_bad_lines=False, encoding='utf-8')
    DB.users = DB.users[['userID', 'Location', 'Age']]
    DB.ratings = pd.read_csv('Final_ratings.csv', sep='\t', error_bad_lines=False, encoding='utf-8')
    DB.ratings = DB.ratings[['userID', 'ISBN', 'bookRating']]
    #correct it
    DB.books = DB.books.dropna()
    DB.books = DB.books.reset_index()
    DB.books = DB.books[['ISBN', 'bookTitle', 'bookAuthor',
            'yearOfPublication', 'publisher', 'Genre', 'Content', 'IMG_URL']]
    #reshaped dataset by bookrating
    DB.ratings_pivot = DB.ratings.pivot(
        index='userID', columns='ISBN').bookRating
    #average
    DB.average_rating = pd.DataFrame(
        DB.ratings.groupby('ISBN')['bookRating'].mean())
    DB.average_rating['ratingCount'] = pd.DataFrame(
        DB.ratings.groupby('ISBN')['bookRating'].count())
    DB.average_rating.sort_values('ratingCount', ascending=False)


def pearson(isbn):
    bones_ratings = DB.ratings_pivot[isbn].T
    similar_to_bones = DB.ratings_pivot.corrwith(bones_ratings)
    corr_bones = pd.DataFrame(similar_to_bones, columns=['pearsonR'])
    corr_bones.dropna(inplace=True)
    corr_summary = corr_bones.join(DB.average_rating['ratingCount'])
    c = corr_summary[corr_summary['ratingCount'] >= 100].sort_values('pearsonR', ascending=False).head(10)
    return c.index.values
    # return 0


def final_c(isbn, array):
    storage = []
    q = DB.books.loc[DB.books['ISBN'] == isbn]
    q = q.reset_index()
    txt = q['Content'][0]
    arr = []
    max = 0
    for i in array:
        b = DB.books.loc[DB.books['ISBN'] == i]
        b = b.reset_index()
        if len(b) != 0 and isbn != b['ISBN'][0]:
            try:
                num = compare(b['Content'][0], txt)
            except:
                num = -1
            cur = [num, i]
            arr.append(cur)
    arr.sort(key=lambda x: x[0])
    arr.reverse()
    print (arr[len(arr) - 1][1])
    for i in range(0, min(10, len(arr))):
        b = DB.books.loc[DB.books['ISBN'] == arr[i][1]]
        b = b.reset_index()
        isbn = arr[i][1]
        book = Book.objects.filter(isbn=isbn).first()
        if book != None:
            storage.append(book)
        else: 
            name = b['bookTitle'][0]
            author = b['bookAuthor'][0]
            description = b['Content'][0]
            photo = b['IMG_URL'][0]
            genreS = b['Genre'][0]
            genreList = genreS.split()
            ind = 0
            for i in range(0,len(genreList)):
                if (genreList[i].lower() != 'fiction'):
                    ind = i
                    break
            genre = Genre.objects.filter(name=genreList[ind]).first()
            if genre == None:
                genre = Genre.objects.create(name=genreList[i])
            #genre.book.add(book)
            print (genre)
            book = Book.objects.create(name=name, author=author, description=description,
                                       isbn=isbn, photo=photo)
            book.genre.add(genre)
            book.save()
            storage.append(book)
    return (storage)
    

def extract_main_topics(doc_a):
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    doc_set = [doc_a]
    texts = []
    for i in doc_set:
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [i for i in tokens if not i in en_stop]
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        texts.append(stopped_tokens)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus, num_topics=1, id2word=dictionary, passes=3)
    top_topics = ldamodel.top_topics(corpus)
    return top_topics


def compare(sstring1, sstring2):
    avg = 0
    #count of similarities
    cnt1 = 0
    top_topics1 = extract_main_topics(sstring1)
    top_topics2 = extract_main_topics(sstring2)
    for i in range(0, 20):
        sim = 0
        max_avg = 0
        for j in range(0, 20):
            try:
                first = top_topics1[0][0][i][1]+'.n.01'
                second = top_topics2[0][0][j][1]+'.n.01'

                cb = wordnet.synset(first)
                ib = wordnet.synset(second)
                sim = cb.wup_similarity(ib)

                if(sim > max_avg):
                    max_avg = sim

            except:
                pass
            try:
                first = top_topics1[0][0][i][1]+'.a.01'
                second = top_topics2[0][0][j][1]+'.a.01'

                cb = wordnet.synset(first)
                ib = wordnet.synset(second)
                sim = cb.wup_similarity(ib)

                if(sim > max_avg):
                    max_avg = sim

            except:
                pass
            try:
                first = top_topics1[0][0][i][1]+'.v.01'
                second = top_topics2[0][0][j][1]+'.v.01'

                cb = wordnet.synset(first)
                ib = wordnet.synset(second)
                sim = cb.wup_similarity(ib)

                if(sim > max_avg):
                    max_avg = sim

            except:
                pass
        if(max_avg != 0):
            cnt1 += 1
            avg += max_avg
    if(cnt1 != 0):
        #print(avg/cnt1)
        return (avg/cnt1)
    else:
        #print('no sim')
        return -1.0
