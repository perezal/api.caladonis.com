from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('workout date', auto_now_add=True)
    notes = models.TextField(default='')

class Exercise(models.Model):

    workout = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

class Set(models.Model):

    exercise = models.ForeignKey(Exercise, related_name="sets", on_delete=models.CASCADE)
    reps = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
