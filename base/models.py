from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import os
class UserManager(BaseUserManager):

	use_in_migration = True

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('Email is Required')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff = True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser = True')

		return self.create_user(email, password, **extra_fields)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

	# email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
	
	# create a link for frontend localhost:3000
	email_html_message = """
		<p>Hi,</p>
		<p>Someone (hopefully you) has requested a password reset for the following account:</p>
		<p>Username: {username}</p>
		<p>If this was a mistake, just ignore this email and nothing will happen.</p>
		<p>To reset your password, visit the following link:</p>
		<p><a href="{link}">{link}</a></p>
		<p>Thanks,</p>
		<p>Your friends at SocietyBench</p>
		""".format(username=reset_password_token.user.email, link="http://localhost:3000/reset-password?token={}".format(reset_password_token.key))
		


	send_mail(
		# title:
		"Password Reset for {title}".format(title="SocietyBench"),
		# message:
		email_html_message,
		# from:
		os.getenv('myemail'),
		# to:
		[reset_password_token.user.email]
	)




class User(AbstractUser):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	iis_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	username = None

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = UserManager()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	

class Society(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	logo = models.ImageField(upload_to='society/', null=True, blank=True)
	followers = models.ManyToManyField(User, through='Follower', related_name='societies_followed')
	is_active = models.BooleanField(default=True)


	def __str__(self):
		return self.name
	

class Permission(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name
	
class Role(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	permissions = models.ManyToManyField(Permission)

	def __str__(self):
		return self.name




class Member(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	is_president = models.BooleanField(default=False)

	role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user.username} in {self.society.name}"
	


class Post(models.Model):
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class AnnouncementPost(Post):
	is_announcement = models.BooleanField(default=True)

	def __str__(self):
		return self.title
	


class EventPost(Post):
	is_event = models.BooleanField(default=True)
	date = models.DateTimeField()
	
	def __str__(self):
		return self.title
	

class PostLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} likes {self.post.title}"

class PostComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} commented on {self.post.title}"
	
class Follower(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='societies_following')
	society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_followers')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} follows {self.society.name}"


class RoomBookingRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	room = models.CharField(max_length=255)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	reason = models.TextField()
	no_of_people = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_approved = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.room} on {self.date}"
	

class Event(models.Model):
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	description = models.TextField()
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	venue = models.CharField(max_length=255, blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
class Report(models.Model):
	detail = models.TextField()
	report_type = models.CharField(max_length=255)
	reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reports_made')
	reported_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reports_received')
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	is_archived = models.BooleanField(default=False)


	def __str__(self):
		return f"{self.reported_by} reported {self.reported_to}"
	

class Task(models.Model):
	STATUS_CHOICES = [
		('To Do', 'To Do'),
		('In Progress', 'In Progress'),
		('Done', 'Done')
	]

	PRIORITY_CHOICES = [
		('High', 'High'),
		('Medium', 'Medium'),
		('Low', 'Low')
	]

	title = models.CharField(max_length=255)
	description = models.TextField()
	society = models.ForeignKey(Society, on_delete=models.CASCADE)
	status = models.CharField(choices=STATUS_CHOICES, max_length=20)
	priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20)
	assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assignee')
	due_date = models.DateField()
	assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
