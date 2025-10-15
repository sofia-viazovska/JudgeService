from django.core.management.base import BaseCommand
from judging.models import Team

class Command(BaseCommand):
    help = 'Deletes all previous teams and adds new ones'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting all previous teams...')
        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All previous teams deleted'))
        
        # Create new teams with their members
        teams_data = [
            {
                'name': 'DeadlineTerminators',
                'members': 'Єгор Папкович\nЖак Марія\nЯна Василенко\nСиняєв Ігор',
                'description': 'Team DeadlineTerminators'
            },
            {
                'name': 'Branch Master',
                'members': 'Куцевіл Іван\nМикола Білявський\nКонрад Владислав',
                'description': 'Team Branch Master'
            },
            {
                'name': 'okaki',
                'members': 'Євгенія Каспрук\nАнастасія Покормяк\nДавиденко Георгій\nВязовська Соломія',
                'description': 'Team okaki'
            },
            {
                'name': 'Vibe Coders',
                'members': 'Артур Кудирко\nВасиленко Ілля\nГабріелла Тер-Нікогосян\nМороз Андрій',
                'description': 'Team Vibe Coders'
            },
            {
                'name': 'Pineapple',
                'members': 'Артем Анкудінов\nБогдан Рак\nЄвгеній Пронь\nІлля Смірнов',
                'description': 'Team Pineapple'
            },
            {
                'name': 'PL KPI',
                'members': 'Галина Пастушкова\nМакарій Слупський\nОлександр Ковальов\nІван Лобур',
                'description': 'Team PL KPI'
            },
            {
                'name': '3pilci',
                'members': 'Дмитро Джос\nВолодимир Степанов\nМаргарита Лепушинська\nІван Соснюк',
                'description': 'Team 3pilci'
            },
            {
                'name': 'Непереможні2000 3.0',
                'members': 'Лідія Соха\nЮстина Гаєвська\nБритан Михайло\nСиротюк Віктор',
                'description': 'Team Непереможні2000 3.0'
            },
            {
                'name': 'KPIck-me',
                'members': 'Дмитро Кулагін\nПавло Малуєв\nАртем Власенко\nДмитро Волощук',
                'description': 'Team KPIck-me'
            },
            {
                'name': 'ну хз',
                'members': 'Куц Анна\nМалащук Іванна\nХорунжа Марія\nМихайлов Владислав',
                'description': 'Team ну хз'
            },
            {
                'name': 'UCUна Матата',
                'members': 'Михайлищук Назар\nМороз Тетяна\nНичипорук Дарина\nМандрик Софія',
                'description': 'Team UCUна Матата'
            },
            {
                'name': 'Git Push and Pray',
                'members': 'Швачка Денис\nТугай Анастасія\nХаришин Ігор\nГібський Владислав',
                'description': 'Team Git Push and Pray'
            },
            {
                'name': 'Emerald',
                'members': 'Горецька Дарина\nПечененко Ярина\nОгінська Марина\nЗарицький Іван',
                'description': 'Team Emerald'
            },
        ]
        
        for team_data in teams_data:
            team = Team.objects.create(
                name=team_data['name'],
                description=team_data['description'],
                members=team_data['members']
            )
            self.stdout.write(self.style.SUCCESS(f'Team "{team.name}" created'))
        
        self.stdout.write(self.style.SUCCESS('All new teams created successfully!'))