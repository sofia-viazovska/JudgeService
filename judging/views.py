from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Sum
from django.contrib.auth.models import User
from .models import Team, Criteria, Score
from .forms import ScoreForm

# Create your views here.
def home(request):
    """Home page view"""
    return render(request, 'judging/home.html')

@login_required
def dashboard(request):
    """Dashboard view for logged-in judges"""
    teams = Team.objects.all()
    return render(request, 'judging/dashboard.html', {'teams': teams})

@login_required
def team_list(request):
    """View to display all teams for selection"""
    teams = Team.objects.all()

    # For non-admin users, check which teams they have already judged
    judged_teams = set()
    if not (request.user.is_staff or request.user.is_superuser):
        # Get all teams that have at least one score from this judge
        judged_teams = set(Score.objects.filter(judge=request.user).values_list('team_id', flat=True).distinct())

    return render(request, 'judging/team_list.html', {
        'teams': teams,
        'judged_teams': judged_teams
    })

@login_required
def judge_team(request, team_id):
    """View to judge a specific team"""
    # Prevent admin users from judging teams
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin users cannot judge teams.")
        return redirect('results')

    team = get_object_or_404(Team, id=team_id)
    criteria_list = Criteria.objects.all()

    # Check if the judge has already scored this team
    existing_scores = {}
    for criteria in criteria_list:
        score = Score.objects.filter(judge=request.user, team=team, criteria=criteria).first()
        if score:
            existing_scores[criteria.id] = score.score

    if request.method == 'POST':
        # Process the submitted scores
        for criteria in criteria_list:
            score_value = request.POST.get(f'criteria_{criteria.id}')
            if score_value:
                try:
                    score_value = int(score_value)
                    if 0 <= score_value <= 10:  # Validate score range
                        # Update or create the score
                        Score.objects.update_or_create(
                            judge=request.user,
                            team=team,
                            criteria=criteria,
                            defaults={'score': score_value}
                        )
                except ValueError:
                    messages.error(request, f"Invalid score for {criteria.name}. Please enter a number between 0 and 10.")
                    return redirect('judge_team', team_id=team.id)

        messages.success(request, f"Scores for {team.name} have been saved successfully.")
        return redirect('team_list')

    context = {
        'team': team,
        'criteria_list': criteria_list,
        'existing_scores': existing_scores,
    }
    return render(request, 'judging/judge_team.html', context)

def results(request):
    """View to display the results/scoreboard"""
    teams = Team.objects.all()
    criteria_list = Criteria.objects.all()

    results = []
    for team in teams:
        team_data = {
            'team': team,
            'avg_scores': team.get_average_scores(),
            'total_score': team.get_total_score(),
        }
        results.append(team_data)

    # Sort results by total score (descending)
    results.sort(key=lambda x: x['total_score'], reverse=True)

    context = {
        'results': results,
        'criteria_list': criteria_list,
    }
    return render(request, 'judging/results.html', context)

@login_required
def admin_detailed_scores(request):
    """Admin-only view to display detailed scores from all judges"""
    # Only allow admin users to access this view
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to view detailed scores.")
        return redirect('results')

    teams = Team.objects.all()
    criteria_list = Criteria.objects.all()
    judges = User.objects.filter(score__isnull=False).distinct()

    detailed_results = []
    for team in teams:
        team_data = {
            'team': team,
            'judge_scores': {}
        }

        # Get scores from each judge for this team
        for judge in judges:
            judge_scores = {}
            for criteria in criteria_list:
                score = Score.objects.filter(
                    judge=judge,
                    team=team,
                    criteria=criteria
                ).first()

                if score:
                    judge_scores[criteria.name] = score.score
                else:
                    judge_scores[criteria.name] = 0

            team_data['judge_scores'][judge.username] = judge_scores

        detailed_results.append(team_data)

    context = {
        'detailed_results': detailed_results,
        'criteria_list': criteria_list,
        'judges': judges,
    }
    return render(request, 'judging/admin_detailed_scores.html', context)
