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

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user' ,url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)
class TourViewSet(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": len(queryset),
            "results": serializer.data
        }
        return Response(data)

class TourDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer

    def retrieve(self, request, pk=None):
        try:
            tour = self.queryset.get(pk=pk)
            serializer = self.serializer_class(tour,context={'request': request})
            data = serializer.data
            data['id'] = tour.pk  # Thêm trường id vào dữ liệu
            return Response(data)
        except Tours.DoesNotExist:
            return Response({"error": "Tour not found"}, status=404)

class TourCommentViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Tours.objects.filter(active=True).all()
    serializer_class = ToursSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post','get'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, tour=self.get_object(), content=request.data.get('content'))
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
