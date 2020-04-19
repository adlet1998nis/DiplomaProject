from django.conf.urls import url, include
from .BookManager.BookManager import *
from .PersonManager.PersonManager import *
from .BookManager.Recommendation import *

from rest_framework import routers

router = routers.DefaultRouter()

router.register('books', AllBooks)
router.register('persons', AllPersons)
router.register('genres', AllGenres)
router.register('messages', AllMessages)
router.register('community', AllCommunity)

# router.register('create_lesson', views.CreateLessonView)
# router.register('persons', views.PersonsView)

urlpatterns = [
    url('', include(router.urls)),
    url(r'^book/add_rating', add_rating),
    url(r'^book/add_comment/$', add_comment),
    url(r'^book/add_book/$', addBook),
    url(r'^book/change_reader/$', changeCurrentReaderRequest),
    url(r'^book/accept_change_reader/$', changeCurrentReaderAccept),
    url(r'^book/decide_change_reader/$', changeCurrentReaderDecide),
    url(r'^book/search/$', search),
    url(r'^book/free_book/$', free_books),
    url(r'^book/my/$', my_books),
    url(r'^book_finish/$', finish_book),
    url(r'^my_reading_books/$', my_reading_books),

    url(r'^message_get/$', message_get),
    url(r'^get_book_info/$', getInformationAboutBook),

    url(r'^authorize/$', Authorize.as_view()),
    url(r'^message/$', Messages.as_view()),
    url(r'^auth/$', authorize),
    url(r'^test_push/$', send_push_test),
    
    url(r'^related_books/$', related_books),
    url(r'^recommend_me/$', recommendMe),
]

# initData()