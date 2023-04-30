from django.contrib import admin
from .models import User, Society, Member, AnnouncementPost, EventPost, Follower, Role, Permission, RoomBookingRequest, Event, Report, Task

admin.site.register(User)
admin.site.register(Society)
admin.site.register(Member)
admin.site.register(AnnouncementPost)
admin.site.register(EventPost)
admin.site.register(Follower)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RoomBookingRequest)
admin.site.register(Event)
admin.site.register(Report)
admin.site.register(Task)