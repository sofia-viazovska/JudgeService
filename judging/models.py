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
    ('bonus', 'Bonus Criteria'),
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
            bonus_criteria = Criteria.objects.filter(type='bonus', service=self.service)

        all_criteria = list(main_criteria) + list(bonus_criteria)

        avg_scores = {}
        for criteria in all_criteria:
            # Get all scores for this team and criteria
            scores = Score.objects.filter(team=self, criteria=criteria)
            total_judges = scores.count()

            if total_judges > 0:
                # Calculate the percentage of judges who checked this criteria
                checked_count = scores.filter(checked=True).count()
                check_percentage = checked_count / total_judges

                # If more than 50% of judges checked it, count the points
                if check_percentage > 0.5:
                    avg_scores[criteria.name] = criteria.points
                else:
                    avg_scores[criteria.name] = 0
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
    type = models.CharField(max_length=5, choices=CRITERIA_TYPES, default='main', help_text="Type of criteria (main or bonus)")
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES, blank=True, null=True, help_text="Service vector this criteria applies to (for bonus criteria)")
    points = models.FloatField(default=0, help_text="Points awarded when this criterion is checked")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Criteria"

class Score(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False, help_text="Whether this criterion is checked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a judge can only score a team-criteria combination once
        unique_together = ('judge', 'team', 'criteria')

    def __str__(self):
        status = "checked" if self.checked else "not checked"
        return f"{self.judge.username}'s score for {self.team.name} - {self.criteria.name}: {status}"

    @property
    def score(self):
        """Returns the score value based on whether the criterion is checked"""
        return self.criteria.points if self.checked else 0
