from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User, Society, Member,Post, AnnouncementPost, EventPost, PostLike, PostComment, Follower, Role, Permission, Event, RoomBookingRequest, Report, Task
from .serializers import UserSerializer, SocietySerializer, MemberSerializer, PostSerializer, AnnouncementPostSerializer, EventPostSerializer,PostLikeSerializer, PostCommentSerializer, FollowerSerializer, RoleSerializer, PermissionSerializer, ChangePasswordSerializer, RoomBookingRequestSerializer, EventSerializer, ReportSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	# permission_classes = [IsAuthenticated]

class SocietyViewSet(viewsets.ModelViewSet):
	queryset = Society.objects.all()
	serializer_class = SocietySerializer
	# permission_classes = [IsAuthenticated]

class MemberViewSet(viewsets.ModelViewSet):
	queryset = Member.objects.all()
	serializer_class = MemberSerializer
	# permission_classes = [IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	# permission_classes = [IsAuthenticated]

class AnnouncementPostViewSet(viewsets.ModelViewSet):
	queryset = AnnouncementPost.objects.all()
	serializer_class = AnnouncementPostSerializer
	# permission_classes = [IsAuthenticated]

class EventPostViewSet(viewsets.ModelViewSet):
	queryset = EventPost.objects.all()
	serializer_class = EventPostSerializer
	# permission_classes = [IsAuthenticated]

class FollowerViewSet(viewsets.ModelViewSet):
	queryset = Follower.objects.all()
	serializer_class = FollowerSerializer
	# permission_classes = [IsAuthenticated]

class PostLikeViewSet(viewsets.ModelViewSet):
	queryset = PostLike.objects.all()
	serializer_class = PostLikeSerializer
	# permission_classes = [IsAuthenticated]

class PostCommentViewSet(viewsets.ModelViewSet):
	queryset = PostComment.objects.all()
	serializer_class = PostCommentSerializer
	# permission_classes = [IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
	queryset = Permission.objects.all()
	serializer_class = PermissionSerializer
	# permission_classes = [IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):
	queryset = Role.objects.all()
	serializer_class = RoleSerializer
	# permission_classes = [IsAuthenticated]


class RegisterView(APIView):
	def post(self, request):
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	model = User
	permission_classes = (IsAuthenticated,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			response = {
				'status': 'success',
				'code': status.HTTP_200_OK,
				'message': 'Password updated successfully',
				'data': []
			}

			return Response(response)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeactivateSocietyView(APIView):
	def post(self, request, society_id):
		society = get_object_or_404(Society, pk=society_id)

		society.is_active = False
		society.save()

		return Response({'message': f"{society.name} has been deactivated."}, status=status.HTTP_200_OK)


class RoomBookingRequestViewSet(viewsets.ModelViewSet):
	queryset = RoomBookingRequest.objects.all()
	serializer_class = RoomBookingRequestSerializer
	# permission_classes = [IsAuthenticated]


class GetRoomBookingsView(APIView):
	def get(self, request, society_id):
		society = get_object_or_404(Society, pk=society_id)
		bookings = RoomBookingRequest.objects.filter(society=society)

		serializer = RoomBookingRequestSerializer(bookings, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	

class AcceptRoomBookingView(APIView):
	def post(self, request):
		booking_id = request.data.get('booking_id')
		booking = get_object_or_404(RoomBookingRequest, pk=booking_id)

		booking.is_approved = True
		booking.save()

		serializer = RoomBookingRequestSerializer(booking)
		return Response(serializer.data, status=status.HTTP_200_OK)


class EventListView(APIView):
	def get(self, request, society_id):
		events = Event.objects.filter(society__id=society_id)
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

	def post(self, request, society_id):
		serializer = EventSerializer(data=request.data)
		if serializer.is_valid():
			serializer.validated_data['society_id'] = society_id
			serializer.validated_data['created_by'] = request.user
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdateView(generics.UpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	# permission_classes = [IsAuthenticated]
	lookup_url_kwarg = 'id'


class AddRoleView(APIView):
	def post(self, request, format=None):
		serializer = RoleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(created_by=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRolesView(APIView):
	def get(self, request, societyId, format=None):
		roles = Role.objects.filter(society_id=societyId)
		serializer = RoleSerializer(roles, many=True)
		return Response(serializer.data)


class UpdateRoleView(APIView):
	queryset = Role.objects.all()
	serializer_class = RoleSerializer
	# permission_classes = [IsAuthenticated]
	
	def patch(self, request, *args, **kwargs):
		role_id = kwargs.get('id')
		try:
			role = Role.objects.get(id=role_id)
		except Role.DoesNotExist:
			return Response({'message': 'Role not found'}, status=404)
		serializer = RoleSerializer(role, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=400)



class SocietyReportView(APIView):
	def post(self, request, societyId):
		try:
			society = Society.objects.get(id=societyId)
		except Society.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = ReportSerializer(data=request.data)
		if serializer.is_valid():
			report = serializer.save(society=society)
			return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, societyId):
		try:
			society = Society.objects.get(id=societyId)
		except Society.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		reports = Report.objects.filter(society=society)
		serializer = ReportSerializer(reports, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
   
class SocietyReportUpdateView(APIView):
	def put(self, request, pk):
		try:
			report = Report.objects.get(pk=pk)
		except Report.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = ReportSerializer(report, data=request.data,partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk):
		try:
			report = Report.objects.get(pk=pk)
		except Report.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = ReportSerializer(report, data=request.data,partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	# permission_classes = [IsAuthenticated]



class MemberCreateView(APIView):
    def post(self, request):
        # extract data from request
        user_data = request.data.pop('user')
        society_id = request.data.pop('society_id')
        role_id = request.data.pop('role_id')

        # create user instance
        user_data['password'] = make_password(user_data['password'])
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.save()

        # create member instance
        member_data = {
            'user': user.id,
            'society': society_id,
            'role': role_id
        }
        member_serializer = MemberSerializer(data=member_data)
        if not member_serializer.is_valid():
            user.delete()  # rollback user creation
            return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        member = member_serializer.save()

        return Response(member_serializer.data, status=status.HTTP_201_CREATED)


class MemberView(APIView):
    def get(self, request, society_id):
        members = Member.objects.filter(society_id=society_id)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class MemberUpdateView(generics.UpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberDeletelView(APIView):
    def delete(self, request, pk):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
