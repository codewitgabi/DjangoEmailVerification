from django.db import models
import uuid
import datetime
from django.utils import timezone


class Token(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	date_created = models.DateTimeField(auto_now_add=True)
	valid = models.BooleanField(default=False)
	
	@property
	def has_expired(self):
		delta = timezone.now() - self.date_created
		# token expires in five minutes
		return delta.seconds > 300
	
	def __str__(self):
		return str(self.id)
		
		