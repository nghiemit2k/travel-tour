from django.shortcuts import render
from requests import Response

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action

from .models import Tours, Booking, News, User, Comment, Review
from .serializers import ToursSerializer
from .serializers import BookingSerializer
from .serializers import NewsSerializer, UserSerializer, CommentSerializer, ReviewSerializer
from rest_framework.parsers import MultiPartParser


class TourViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer


class TourDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer


class BookingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Booking.objects.filter(active=True)
    serializer_class = BookingSerializer


class NewsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = News.objects.filter(active=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    ## RetrieveAPIView lấy thông tin user
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    parser_classes = [MultiPartParser, ]
    def get_permissions(self):
        if self.action =='retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]



class ReviewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Review.objects.filter(active=True)
    serializer_class = ReviewSerializer


def index(request):
    return render(request, 'index.html', context={'name': 'khai nghiem'})
