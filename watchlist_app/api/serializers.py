from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatForm,Review


# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short")
#     else:
#         return value

# class MovieSerializers(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[name_length])
#     description=serializers.CharField()
#     active=serializers.BooleanField()
    
#     # create 
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     # update
#     def update(self,instance,validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance 
        
#     # validation 
#     def validate(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError('Title and should be different')
#         else:
#             return data
#     # def validate_name(self,value):
#     #     if len(value)<2:
#     #         raise  serializers.ValidationError("Name is too Short!")
#     #     else:
#     #         return value
    
    # model serializers 
class ReviewSerializers(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields="__all__"
class WatchListSerializers(serializers.ModelSerializer):
    reviews = ReviewSerializers(many=True,read_only=True)
    # len_name=serializers.SerializerMethodField()
    class Meta:
        model=WatchList 
        fields="__all__"
        # fields=['id','name','description']
    #     # exclude=['active']
    # def get_len_name(self,object):
    #     return len(object.name)
    
# class StreamPlatFormSerializers(serializers.ModelSerializer):
class StreamPlatFormSerializers(serializers.HyperlinkedModelSerializer):
    watchlist=WatchListSerializers(many=True,read_only=True)
    # watchlist=serializers.StringRelatedField(many=True)
    # watchlist=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='streamplatform-detail') # urls

    
    class Meta:
        model=StreamPlatForm
        fields="__all__"   
    # validation 
    # def validate(self, data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError('Title and should be different')
    #     else:
    #         return data
        
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise  serializers.ValidationError("Name is too Short!")
    #     else:
    #         return value