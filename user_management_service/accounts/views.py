from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, UserSubscriptionSerializer
from confluent_kafka import Producer
import json
from django.conf import settings

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            _ = serializer.save()
            data = serializer.data
            data.pop('password', None) 
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserSubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSubscriptionSerializer(request.user)
        return Response(serializer.data)

class UserSubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_subscribed = not user.is_subscribed
        user.save()
        
        message = {
            "email": user.email,
            "subscription_status": user.is_subscribed
        }
        kafka_conf = {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS
        }
        producer = Producer(kafka_conf)
        producer.produce(
            topic="subscription_updates",
            value=json.dumps(message).encode('utf-8')
        )
        producer.flush()
        return Response({"is_subscribed": user.is_subscribed})
