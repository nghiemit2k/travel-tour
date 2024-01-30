from rest_framework import serializers

from  .models import Tours,Booking,News,User,Comment,Review,Customer

class ToursSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self,tours):
        if tours.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % tours.image.name)
            return '/static/%s' % tours.image.name
    class Meta:
        model = Tours
        fields =["name_tour","image","price_adult","price_child","create_date","start_date","end_date"]

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields=["name","content","create_date"]
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=["content","customer_id","news_id","tour_id","create_date"]
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['content','customer_id','newid','tour_id','create_date','rating']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','first_name','last_name','email','username','password','avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields=['user']


class BookingSerializer(serializers.ModelSerializer):
    # tour = ToursSerializer()

    class Meta:
        model = Booking
        fields = ["customer", "tour", "adults_count", "children_count", "total_price", "create_date"]