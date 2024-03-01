from rest_framework import serializers

from  .models import Tours,Booking,News,User,Rating,Comment,Like

class ToursSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField(source='image')

    def get_image(self,tours):
        if tours.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % tours.image.name)
            return '/static/%s' % tours.image.name

    def get_id(self, obj):
        return obj.pk
    class Meta:
        model = Tours
        fields =["id","name_tour","image","price_adult","price_child","create_date","start_date","end_date"]

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields=["name","content","create_date"]
class NewsDetailSerializer(NewsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,news):
        request=self.context.get('request')
        if request.user.is_authenticated:
            return news.like_set.filter(active=True).exists()
    class Meta:
        model = NewsSerializer.Meta.model
        fields = NewsSerializer.Meta.fields+['liked']

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields=["content","customer","news","tour","create_date"]
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields =['rating','user','tour','create_date']
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields =['user','news','create_date']
class UserSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField()
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

# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = User
#         fields=['user']


class BookingSerializer(serializers.ModelSerializer):
    # tour = ToursSerializer()

    class Meta:
        model = Booking
        fields = ["tour", "adults_count", "children_count", "total_price", "create_date"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id','content','user']