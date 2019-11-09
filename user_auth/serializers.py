from user_auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField, HyperlinkedModelSerializer
from user_auth.models import ProfileCompletionProgress, User, UserPhoto
    
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'mobile_number',
            'is_active',
            'email_verified',
            'is_admin',
            'is_staff',
            'bio_data',
            'gender',
            'first_name', 
            'last_name', 
            'nickname', 
            'nationality', 
            'last_login', 
            'date_joined'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            gender=validated_data['gender'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'], 
            # nationality=validated_data['nationality'], 
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
        
class UserPhotoSerializer(HyperlinkedModelSerializer):     
    user = HyperlinkedRelatedField(
        view_name='user-detail', 
        read_only=True
    )
    
    class Meta:
        model = UserPhoto
        fields = [ 
            'id',
            'user',
            'image',
            'description',
            'date_uploaded',
            'is_active',
            'is_profile_image' 
        ]
        
    def create(self, validated_data):
        return UserPhoto.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_profile_image = validated_data.get('is_profile_image', instance.is_profile_image)
        instance.save()
        return instance
        
class ProfileCompletionProgressSerializer(HyperlinkedModelSerializer):
    user = HyperlinkedRelatedField(
        view_name='user-detail', 
        read_only=True
    )
    
    class Meta:
        model = ProfileCompletionProgress
        fields = [
            'id', 
            'user', 
            'profile_completion_progress', 
            'created_at', 
            'updated_at'
        ]
        
    def create(self, validated_data):
        return ProfileCompletionProgress.objects.create(**validated_data)
    
    def update ( self, instance, validated_data ):
        instance.user = validated_data.get('user', instance.user)
        instance.profile_completion_progress = validated_data.get('profile_completion_progress', instance.profile_completion_progress)
        instance.save()  
        return instance
    
class CreateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'mobile_number', 'first_name', 'last_name', 'gender', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(
            mobile_number=validated_data['mobile_number'],
            gender=validated_data['gender'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'], 
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user