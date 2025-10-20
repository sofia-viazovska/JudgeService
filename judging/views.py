from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Sum
from django.contrib.auth.models import User
from .models import Team, Criteria, Score
from .forms import ScoreForm, TeamServiceForm, SERVICE_CHOICES

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
    team = get_object_or_404(Team, id=team_id)
    is_admin = request.user.is_staff or request.user.is_superuser

    # Get main criteria (common for all teams)
    main_criteria = Criteria.objects.filter(type='main')

    # Get bonus criteria based on team's service
    bonus_criteria = []
    if team.service:
        # Get bonus criteria based on service vector
        if team.service == 'A':
            bonus_criteria = Criteria.objects.filter(type='bonus_a')
        elif team.service == 'B':
            bonus_criteria = Criteria.objects.filter(type='bonus_b')
        elif team.service == 'C':
            bonus_criteria = Criteria.objects.filter(type='bonus_c')

    # Combine criteria lists
    all_criteria = list(main_criteria) + list(bonus_criteria)

    # Check if the judge has already scored this team
    existing_scores = {}
    for criteria in all_criteria:
        score = Score.objects.filter(judge=request.user, team=team, criteria=criteria).first()
        if score:
            existing_scores[criteria.id] = score.value

    # Handle service selection form for admins
    service_form = None
    if is_admin:
        if request.method == 'POST' and 'save_service' in request.POST:
            service_form = TeamServiceForm(request.POST, instance=team)
            if service_form.is_valid():
                service_form.save()
                messages.success(request, f"Сервіс для {team.name} був успішно оновлений.")
                return redirect('judge_team', team_id=team.id)
        else:
            service_form = TeamServiceForm(instance=team)

    # Handle score submission
    if request.method == 'POST' and 'save_scores' in request.POST:
        # Process the submitted scores
        for criteria in all_criteria:
            score_value = request.POST.get(f'criteria_{criteria.id}', 0)
            try:
                score_value = float(score_value)
                # Ensure score is within valid range (0 to max_score)
                score_value = max(0, min(score_value, criteria.max_score))
            except (ValueError, TypeError):
                score_value = 0

            # Update or create the score
            Score.objects.update_or_create(
                judge=request.user,
                team=team,
                criteria=criteria,
                defaults={
                    'value': score_value,
                    'checked': score_value > 0  # For backward compatibility
                }
            )

        messages.success(request, f"Оцінки для {team.name} були успішно збережені.")
        return redirect('team_list')

    context = {
        'team': team,
        'main_criteria': main_criteria,
        'bonus_criteria': bonus_criteria,
        'existing_scores': existing_scores,
        'is_admin': is_admin,
        'service_form': service_form,
    }
    return render(request, 'judging/judge_team.html', context)

def results(request):
    """View to display the results/scoreboard"""
    teams = Team.objects.all()
    main_criteria = Criteria.objects.filter(type='main')

    # Get bonus criteria by service vector
    bonus_criteria_by_service = {
        'A': list(Criteria.objects.filter(type='bonus_a')),
        'B': list(Criteria.objects.filter(type='bonus_b')),
        'C': list(Criteria.objects.filter(type='bonus_c')),
    }

    results = []
    for team in teams:
        # Get all criteria for this team
        team_criteria = list(main_criteria)
        if team.service:
            team_criteria.extend(bonus_criteria_by_service.get(team.service, []))

        # Get average scores using the Team model method
        avg_scores = team.get_average_scores()
        total_score = team.get_total_score()

        team_data = {
            'team': team,
            'avg_scores': avg_scores,
            'total_score': total_score,
            'service': team.get_service_display() if team.service else "Не вибрано",
        }
        results.append(team_data)

    # Sort results by total score (descending)
    results.sort(key=lambda x: x['total_score'], reverse=True)

    # Create a list of all criteria for the template
    criteria_list = list(main_criteria)

    context = {
        'results': results,
        'main_criteria': main_criteria,
        'bonus_criteria_by_service': bonus_criteria_by_service,
        'criteria_list': criteria_list,
    }
    return render(request, 'judging/results.html', context)

@login_required
def admin_detailed_scores(request):
    """Admin-only view to display detailed scores from all judges"""
    # Only allow admin users to access this view
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "У вас немає дозволу на перегляд детальних оцінок.")
        return redirect('results')

    teams = Team.objects.all()
    main_criteria = Criteria.objects.filter(type='main')

    # Get bonus criteria by service vector
    bonus_criteria_by_service = {
        'A': list(Criteria.objects.filter(type='bonus_a')),
        'B': list(Criteria.objects.filter(type='bonus_b')),
        'C': list(Criteria.objects.filter(type='bonus_c')),
    }

    judges = User.objects.filter(score__isnull=False).distinct()

    detailed_results = []
    for team in teams:
        # Get all criteria for this team
        team_criteria = list(main_criteria)
        if team.service:
            team_criteria.extend(bonus_criteria_by_service.get(team.service, []))

        team_data = {
            'team': team,
            'service': team.get_service_display() if team.service else "Не вибрано",
            'judge_scores': {},
            'criteria_averages': {},  # Track average score for each criteria
            'criteria_list': team_criteria  # Store the list of criteria for this team
        }

        # Initialize criteria averages tracking
        for criteria in team_criteria:
            team_data['criteria_averages'][criteria.id] = {
                'total': 0,
                'count': 0,
                'average': 0,
                'max_score': criteria.max_score
            }

        # Get scores from each judge for this team
        for judge in judges:
            judge_scores = {}
            for criteria in team_criteria:
                score = Score.objects.filter(
                    judge=judge,
                    team=team,
                    criteria=criteria
                ).first()

                if score:
                    judge_scores[criteria.id] = {
                        'value': score.value,
                        'criteria_name': criteria.name,
                        'max_score': criteria.max_score
                    }

                    # Update average tracking
                    team_data['criteria_averages'][criteria.id]['total'] += score.value
                    team_data['criteria_averages'][criteria.id]['count'] += 1
                else:
                    judge_scores[criteria.id] = {
                        'value': 0,
                        'criteria_name': criteria.name,
                        'max_score': criteria.max_score
                    }

            # Calculate total score for this judge
            total_points = sum(score['value'] for score in judge_scores.values())
            judge_scores['total'] = total_points

            team_data['judge_scores'][judge.username] = judge_scores

        # Calculate average scores for each criteria
        for criteria_id, data in team_data['criteria_averages'].items():
            if data['count'] > 0:
                data['average'] = data['total'] / data['count']

        # Get the team's average scores and total score
        team_data['avg_scores'] = team.get_average_scores()
        team_data['total_score'] = team.get_total_score()

        detailed_results.append(team_data)

    context = {
        'detailed_results': detailed_results,
        'main_criteria': main_criteria,
        'bonus_criteria_by_service': bonus_criteria_by_service,
        'judges': judges,
    }
    return render(request, 'judging/admin_detailed_scores.html', context)
