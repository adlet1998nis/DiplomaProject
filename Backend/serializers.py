from rest_framework import serializers
from .models import *

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', )


class CommentSerializer(serializers.ModelSerializer):
    author = PersonSerializer(read_only=True, many=False)
    class Meta:
        model = Comment
        fields = '__all__'


class AllBookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ('name', 'isbn', 'author', 'description', 'photo', 'genre', 'rating', 'reader')
        # fields = ('__all__')
# class DetailBookSerializer(serializers.Serializer):


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    belong = PersonSerializer(read_only=True, many=False)
    reader = PersonSerializer(read_only=True, many=False)
    history = PersonSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = '__all__'


class CommunitySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True, many=False)
    author = PersonSerializer(read_only=True, many=False)

    class Meta:
        model = Community
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True, many=False)
    author = PersonSerializer(read_only=True, many=False)
    recipient = PersonSerializer(read_only=True, many=False)
    class Meta:
        model = Message
        fields = '__all__'

