from django.db import models

# Create your models here.
class Choice(models.Model):
    answerA = models.CharField(max_length=50, blank=False)
    answerB = models.CharField(max_length=50, blank=False)
    answerC = models.CharField(max_length=50, blank=False)
    answerD = models.CharField(max_length=50, blank=False)
    problem = models.ForeignKey('ChoiceProblem')

    
class BaseProblem(models.Model):
    type = models.CharField(max_length=10, blank=False)
    description = models.CharField(max_length=100, blank=False)


class ChoiceProblem(BaseProblem):
    correct = models.CharField(max_length=50, blank=False)

    def __unicode__(self):
        return self.id

    class Meta:
        ordering = ['id']


class ToFProblem(BaseProblem):
    correct = models.BooleanField(default=False, blank=False)

    def __unicode__(self):
        return self.id

    class Meta:
        ordering = ['id']

