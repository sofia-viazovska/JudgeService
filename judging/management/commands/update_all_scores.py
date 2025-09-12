from django.core.management.base import BaseCommand
from judging.models import Score

class Command(BaseCommand):
    help = 'Updates all scores in the database to a specified value'

    def add_arguments(self, parser):
        parser.add_argument('score_value', type=int, help='The value to set for all scores')

    def handle(self, *args, **kwargs):
        score_value = kwargs['score_value']
        
        # Validate the score value
        if not (0 <= score_value <= 10):
            self.stdout.write(self.style.ERROR(f'Score value must be between 0 and 10, got {score_value}'))
            return
        
        # Get the count of scores before updating
        total_scores = Score.objects.count()
        self.stdout.write(f'Found {total_scores} scores in the database')
        
        # Update all scores
        updated_count = Score.objects.update(score=score_value)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} scores to {score_value}'))