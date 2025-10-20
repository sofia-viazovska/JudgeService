from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum

# Service choices for teams
SERVICE_CHOICES = [
    ('A', 'A – Mobile App'),
    ('B', 'B – Web App'),
    ('C', 'C – Telegram Bot'),
]

# Criteria types
CRITERIA_TYPES = [
    ('main', 'Main Criteria'),
    ('bonus_a', 'Bonus Criteria for Vector A'),
    ('bonus_b', 'Bonus Criteria for Vector B'),
    ('bonus_c', 'Bonus Criteria for Vector C'),
]

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.TextField(blank=True, help_text="List of team members, one per line")
    members_info = models.TextField(blank=True, help_text="Additional information about team members in format: Student - leader, university, year of study")
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES, blank=True, null=True, help_text="Service vector for the team")

    def __str__(self):
        return self.name

    def get_average_scores(self):
        """Returns a dictionary of average scores for each criteria"""
        # Get all applicable criteria for this team
        main_criteria = Criteria.objects.filter(type='main')
        bonus_criteria = []
        if self.service:
            # Get bonus criteria based on service vector
            if self.service == 'A':
                bonus_criteria = Criteria.objects.filter(type='bonus_a')
            elif self.service == 'B':
                bonus_criteria = Criteria.objects.filter(type='bonus_b')
            elif self.service == 'C':
                bonus_criteria = Criteria.objects.filter(type='bonus_c')

        all_criteria = list(main_criteria) + list(bonus_criteria)

        avg_scores = {}
        for criteria in all_criteria:
            # Get all scores for this team and criteria
            scores = Score.objects.filter(team=self, criteria=criteria)
            total_judges = scores.count()

            if total_judges > 0:
                # Calculate the average score for this criteria
                avg_value = scores.aggregate(Avg('value'))['value__avg']
                avg_scores[criteria.name] = avg_value
            else:
                avg_scores[criteria.name] = 0

        return avg_scores

    def get_total_score(self):
        """Returns the sum of scores across all criteria"""
        avg_scores = self.get_average_scores()
        return sum(avg_scores.values())

class Criteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=7, choices=CRITERIA_TYPES, default='main', help_text="Type of criteria (main or bonus)")
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES, blank=True, null=True, help_text="Service vector this criteria applies to (for bonus criteria)")
    max_score = models.FloatField(default=10, help_text="Maximum possible score for this criterion")
    points = models.FloatField(default=0, help_text="Legacy field - Points awarded when this criterion is checked")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Criteria"

class Score(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.FloatField(default=0, validators=[MinValueValidator(0)], help_text="Score value (0 to max_score)")
    checked = models.BooleanField(default=False, help_text="Legacy field - Whether this criterion is checked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a judge can only score a team-criteria combination once
        unique_together = ('judge', 'team', 'criteria')

    def __str__(self):
        return f"{self.judge.username}'s score for {self.team.name} - {self.criteria.name}: {self.value}"

    @property
    def score(self):
        """Returns the score value"""
        return self.value
