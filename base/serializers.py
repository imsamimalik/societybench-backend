from rest_framework import serializers
from .models import User, Society, Member, Post, AnnouncementPost, EventPost, PostLike, PostComment, Follower, Permission, Role, RoomBookingRequest, Report, Event, Task

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields="__all__"

		extra_kwargs = {
			'password': {'write_only':True}
		}
		def create(self, validated_data):
			user = User.objects.create(email=validated_data['email'],
										   name=validated_data['name']
											 )
			user.set_password(validated_data['password'])
			user.save()
			return user

class SocietySerializer(serializers.ModelSerializer):
	class Meta:
		model = Society
		fields="__all__"

class MemberSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	society = SocietySerializer()
	class Meta:
		model = Member
		fields="__all__"

class PostSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	society = SocietySerializer()
	class Meta:
		model = Post
		fields="__all__"

class AnnouncementPostSerializer(serializers.ModelSerializer):
	post = PostSerializer()
	class Meta:
		model = AnnouncementPost
		fields="__all__"

class EventPostSerializer(serializers.ModelSerializer):
	post = PostSerializer()
	class Meta:
		model = EventPost
		fields="__all__"

class PostLikeSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	post = PostSerializer()
	class Meta:
		model = PostLike
		fields="__all__"

class PostCommentSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	post = PostSerializer()
	class Meta:
		model = PostComment
		fields="__all__"

class FollowerSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	society = SocietySerializer()
	class Meta:
		model = Follower
		fields="__all__"


class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
	permissions = PermissionSerializer(many=True)

	class Meta:
		model = Role
		fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    

class RoomBookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBookingRequest
        fields = '__all__'
	
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
	

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
	

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'