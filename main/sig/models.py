from django.db import models
from django.contrib.auth import get_user_model

class ToDo (models.Model):
  task_name = models.CharField(max_length=100)
  task_start = models.DateField()
  task_end = models.DateField()
  is_active= models.BooleanField(default=True)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

  def __str__(self):
    return self.task_name
    