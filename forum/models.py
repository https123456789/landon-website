from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	userViewList = [
		1
	]
	view = {
		"count": 0
	}
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return self.text
class Entry(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add = True)
	class Meta:
		verbose_name_plural = "entries"
	def __str__(self):
		return "{}...".format(self.text)
