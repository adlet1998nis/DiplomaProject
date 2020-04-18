from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from Backend.serializers import *
from rest_framework import viewsets
from django.http import JsonResponse
from Backend.Services.Services import send_push

import json

class AllPersons(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class AllCommunity(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class AllMessages(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class Authorize(APIView):

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data['name']
            phone = data['phone']
            email = data['email']
            password = data['password']
            token = data['token']
            photo = data.get('photo', '')
            user = Person.objects.filter(phone=phone).first()
            if user:
                return Response ({'code': 1, 'message': 'That phone number is taken'})
            user = Person.objects.create(name=name, phone=phone, email=email, password=password,
                                         token=token, photo=photo)
            serializer = PersonSerializer(user, many=False)
            return Response({'code': 0, 'user': serializer.data})
        except Exception as e:
            return Response({'code': 40, 'message': e.message})

class Messages(APIView):

    def post(self, request):
        try:
            data = json.loads(request.body)
            author_id = data['author_id']
            recipient_id = data['recipient_id']
            text = data['text']
            author = Person.objects.get(id=author_id)
            recipient = Person.objects.get(id=recipient_id)
            Message.objects.create(author=author, recipient=recipient, text=text)
            chat = Message.objects.filter(author=author, recipient=recipient)
            serializer = MessageSerializer(chat, many=False)
            return JsonResponse({'code': 0, 'chat': serializer.data})
        except Exception as e:
            return JsonResponse({'code': 40, 'message': e.message})

    def get(selfs, request):
        try:
            data = json.loads(request.body)
            author_id = data['author_id']
            recipient_id = data['recipient_id']
            author = Person.objects.get(id=author_id)
            recipient = Person.objects.get(id=recipient_id)
            chat = Message.objects.filter(author=author, recipient=recipient)
            serializer = MessageSerializer(chat, many=True)
            return JsonResponse({'code': 0, 'chat': serializer.data})
        except Exception as e:
            return JsonResponse({'code': 40, 'message': e.message})


def authorize(request):
    try:
        # data = json.loads(request.body)
        phone = request.GET.get('phone')
        password = request.GET.get('password')
        token = request.GET.get('token')
        user = Person.objects.filter(phone=phone, password=password).first()
        if user:
            user.token = token
            user.save()
            return JsonResponse({'code': 0, 'user': PersonSerializer(user, many=False).data})
        else:
            return JsonResponse({'code': 2, 'message': 'Wrong password or login'})
    except Exception as e:
        return JsonResponse({'code': 40, 'message': e.message})

def send_push_test(request):
    person_id = request.GET.get('id')
    person = Person.objects.get(id=person_id)
    send_push("123", "SURPRIZE SURPIZE", {"test": "test"}, person.token)
    return JsonResponse({'code': 0})
