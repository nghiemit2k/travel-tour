from rest_framework.serializers import ModelSerializer
from  .models import Tours,Booking,News,User,Comment,Review,Customer

class ToursSerializer(ModelSerializer):
    class Meta:
        model = Tours
        fields =["name_tour","image","price_adult","price_child","create_date","start_date","end_date"]

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields=["name","content","create_date"]
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields=["content","customer_id","news_id","tour_id","create_date"]
class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields =['content','customer_id','newid','tour_id','create_date','rating']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields=['id','first_name','last_name','email','username','password','avatar']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields=['user']


class BookingSerializer(ModelSerializer):
    # tour = ToursSerializer()

    class Meta:
        model = Booking
        fields = ["customer", "tour", "adults_count", "children_count", "total_price", "create_date"]