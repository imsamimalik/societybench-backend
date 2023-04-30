from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'societies', views.SocietyViewSet)
# router.register(r'members', views.MemberViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'announcement-posts', views.AnnouncementPostViewSet)
router.register(r'event-posts', views.EventPostViewSet)
router.register(r'post-likes', views.PostLikeViewSet)
router.register(r'post-comments', views.PostCommentViewSet)
router.register(r'followers', views.FollowerViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet, basename='Roles')
router.register(r'tasks', views.TaskViewSet)


urlpatterns = [
	path('', include(router.urls)),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register', views.RegisterView.as_view(), name="sign_up"),
    path('auth/reset-password', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('auth/change-password', views.ChangePasswordView.as_view(), name='change-password'),

    path('societies/deactivate/<int:society_id>', views.DeactivateSocietyView.as_view(), name='deactivate_society'),
    path('societies/<int:society_id>/room-bookings', views.GetRoomBookingsView.as_view(), name='get_room_bookings'),
    path('societies/room-booking/accept', views.AcceptRoomBookingView.as_view(), name='accept_room_booking'),
    path('societies/<int:society_id>/events', views.EventListView.as_view(), name='event_list'),
    path('societies/events/<int:id>', views.EventUpdateView.as_view(), name='event_update'),
    path('societies/roles', views.AddRoleView.as_view(), name='add-role'),
    path('societies/<int:societyId>/roles', views.GetRolesView.as_view(), name='get-roles'),
    path('societies/roles/<int:id>', views.UpdateRoleView.as_view(), name='get-roles'),
    path('societies/<int:societyId>/report', views.SocietyReportView.as_view(), name='society_report'),
    path('societies/report/<int:pk>', views.SocietyReportUpdateView.as_view(), name='society_report_update'),

    path('societies/members/', views.MemberCreateView.as_view(), name='create_member'),
    path('societies/<int:society_id>/members/', views.MemberView.as_view()),
    path('societies/members/<int:pk>/', views.MemberUpdateView.as_view(), name='member-update'),
    path('societies/members/<int:pk>/', views.MemberDeletelView.as_view(), name='member-delete'),


]