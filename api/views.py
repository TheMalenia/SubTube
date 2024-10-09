from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .models import User, Video, SubscriptionType, Subscription, History
from .serializers import UserSerializer, VideoSerializer, SubscriptionSerializer, SubscriptionTypeSerializer, HistorySerializer, SignUpSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny
import datetime
import json
from django.http import HttpResponse

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def accessible_videos(self, request):
        user = request.user
        subscription = Subscription.objects.filter(user=user, end_date__gt=timezone.now()).first()

        if subscription:
            videos = Video.objects.filter(subscription_type=subscription.subscription_type)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Subscription required to access videos.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def watch_video(self, request, pk=None):
        user = request.user
        video = self.get_object()

        subscription = Subscription.objects.filter(user=user, end_date__gt=timezone.now()).first()
        if not subscription:
            return Response({'error': 'You need a valid subscription to watch videos.'}, status=status.HTTP_403_FORBIDDEN)
        
        videos = Video.objects.filter(subscription_type=subscription.subscription_type)
        if video not in videos:
            return Response({'error': 'You need a valid subscription to watch videos.'}, status=status.HTTP_403_FORBIDDEN)
        
        history = History.objects.filter(user=self.request.user, video=video)
        if not history:
            History.objects.create(user=user, video=video)

        serializer = VideoSerializer(video)
        return Response(serializer.data)

class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def purchase_subscription(self, request):
        user = request.user
        subscription_type = SubscriptionType.objects.get(id=request.data.get('subscription_type'))

        active_subscription = Subscription.objects.filter(user=user, end_date__gt=timezone.now()).first()
        if active_subscription:
            return Response({'error': 'You already have an active subscription.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.wallet < subscription_type.price:
            return Response({'error': 'You dont have enough money. Charge your acoount.'}, status=status.HTTP_400_BAD_REQUEST)
        user.wallet -= subscription_type.price
        user.save()
        
        subscription = Subscription.objects.create(
            user=user,
            subscription_type=subscription_type,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
    

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created  = Token.objects.get_or_create(user=user)

            if not created:
                token.created = datetime.datetime.now()
                token.save()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def charge_wallet(self, request):
        user = request.user
        serializer = WalletViewSet(data=request.data)

        user.wallet += request.data.get('charge')
        user.renewal = request.data.get('renewal')
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)