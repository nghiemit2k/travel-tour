from django.http import HttpResponse
from django.shortcuts import render
# from requests import Response
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action

from .models import Tours, Booking, News, User, Rating,Comment,Like
from .serializers import ToursSerializer,LikeSerializer,NewsDetailSerializer
from .serializers import BookingSerializer
from .serializers import NewsSerializer, UserSerializer, RatingSerializer,CommentSerializer
from rest_framework.parsers import MultiPartParser

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    ## RetrieveAPIView lấy thông tin user
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    parser_classes = [MultiPartParser, ]
    def get_permissions(self):
        if self.action =='retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class TourViewSet(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer

class TourDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer
    permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes
    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, tour=self.get_object(),content=request.data.get('content'))
        response = Response(CommentSerializer(c).data)
        response.status_code = status.HTTP_201_CREATED

        return response


class BookingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Booking.objects.filter(active=True)
    serializer_class = BookingSerializer


class NewsViewSet(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView):
    queryset = News.objects.filter(active=True)
    serializer_class = NewsDetailSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['like']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes
    @action(methods=['post'],url_path='like',detail=True)
    def like(self,request,pk):
        like,created=Like.objects.get_or_create(user=request.user,news=self.get_object())
        if not created:
            like.active = not like.active
            like.save()
        return  Response(NewsDetailSerializer(self.get_object(),context={'request': request}).data,status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = Comment


class RatingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Rating.objects.filter(active=True)
    serializer_class = RatingSerializer

class LikeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Like.objects.filter(active=True)
    serializer_class = LikeSerializer

def index(request):
    return render(request, 'index.html', context={'name': 'khai nghiem'})
