from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_average_scores(self):
        """Returns a dictionary of average scores for each criteria"""
        avg_scores = {}
        for criteria in Criteria.objects.all():
            avg = Score.objects.filter(team=self, criteria=criteria).aggregate(Avg('score'))['score__avg'] or 0
            avg_scores[criteria.name] = avg
        return avg_scores

    def get_total_score(self):
        """Returns the sum of average scores across all criteria"""
        avg_scores = self.get_average_scores()
        return sum(avg_scores.values())

class Criteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Criteria"

class Score(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a judge can only score a team-criteria combination once
        unique_together = ('judge', 'team', 'criteria')

    def __str__(self):
        return f"{self.judge.username}'s score for {self.team.name} - {self.criteria.name}: {self.score}"
