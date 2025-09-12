from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from judging.models import Team, Criteria, Score
import random

class Command(BaseCommand):
    help = 'Sets up demo data for the judging service'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up demo data...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create judge users
        judges = []
        for i in range(1, 4):
            username = f'judge{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'judge{i}@example.com',
                    password=f'judge{i}password'
                )
                judges.append(user)
                self.stdout.write(self.style.SUCCESS(f'Judge user {username} created'))
        
        # Create criteria (10 of them)
        criteria_names = [
            'Innovation', 'Technical Difficulty', 'Design', 'Functionality',
            'Presentation', 'User Experience', 'Impact', 'Scalability',
            'Originality', 'Overall Quality'
        ]
        
        criteria_objects = []
        for name in criteria_names:
            criteria, created = Criteria.objects.get_or_create(
                name=name,
                defaults={'description': f'Evaluation of the team\'s {name.lower()}'}
            )
            criteria_objects.append(criteria)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Criteria "{name}" created'))
        
        # Create teams
        team_names = ['Alpha Team', 'Beta Squad', 'Gamma Group', 'Delta Force', 'Epsilon Innovators']
        team_objects = []
        
        for name in team_names:
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={'description': f'{name} is a group of talented individuals working on innovative solutions.'}
            )
            team_objects.append(team)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Team "{name}" created'))
        
        # Create some sample scores
        if judges and team_objects and criteria_objects:
            for judge in judges:
                for team in team_objects:
                    for criteria in criteria_objects:
                        # Only create scores if they don't exist
                        if not Score.objects.filter(judge=judge, team=team, criteria=criteria).exists():
                            score = random.randint(5, 10)  # Random score between 5 and 10
                            Score.objects.create(
                                judge=judge,
                                team=team,
                                criteria=criteria,
                                score=score
                            )
            self.stdout.write(self.style.SUCCESS('Sample scores created'))
        
        self.stdout.write(self.style.SUCCESS('Demo data setup complete!'))