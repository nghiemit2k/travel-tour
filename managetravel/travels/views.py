from django.shortcuts import render
from rest_framework import viewsets,permissions,generics
from .models import Tours,Booking,News,User,Comment,Review
from  .serializers import ToursSerializer
from  .serializers import BookingSerializer
from .serializers import NewsSerializer,UserSerializer,CommentSerializer,ReviewSerializer
from rest_framework.parsers import MultiPartParser
class TourViewSet(viewsets.ModelViewSet):
    queryset = Tours.objects.filter(active = True)
    serializer_class = ToursSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.filter(active=True)
    serializer_class = BookingSerializer
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(active=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
class UserViewSet(viewsets.ViewSet,generics.CreateAPIView,generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    parser_classes = [MultiPartParser,]

class ReviewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(active=True)
    serializer_class = ReviewSerializer

def index(request):
    return render(request,'index.html',context= {'name':'khai nghiem'})