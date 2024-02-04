from django.urls import path, include
from django.contrib import admin
from . import views
from  .admin import admin_site
from rest_framework.routers import DefaultRouter
# khi truy van vao / thi se mo view index ra
from django.contrib import admin
from django.urls import path,include,re_path
router = DefaultRouter()
router.register('tours',views.TourViewSet)
router.register('tours',views.TourDetailViewSet)
router.register('booking',views.BookingViewSet)
router.register('news',views.NewsViewSet)
router.register('users',views.UserViewSet,basename='users')
router.register('comment',views.CommentViewSet)
router.register('Rating',views.RatingViewSet)

urlpatterns = [

    path('admin/',admin_site.urls),
    path('',include(router.urls))
]
