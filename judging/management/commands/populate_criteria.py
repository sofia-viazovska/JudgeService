from django.core.management.base import BaseCommand
from judging.models import Criteria

class Command(BaseCommand):
    help = 'Populates the database with predefined criteria'

    def handle(self, *args, **options):
        self.stdout.write('Populating criteria...')
        
        # Delete existing criteria
        Criteria.objects.all().delete()
        self.stdout.write('Deleted existing criteria')
        
        # Main criteria - Main functionality
        main_functionality = [
            {
                'name': 'Google OAuth працює надійно',
                'description': 'функціональність: Google OAuth працює надійно',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'Профіль зберігається та відновлюється',
                'description': 'функціональність: Профіль зберігається та відновлюється',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'Конструктор CV з валідацією полів',
                'description': 'функціональність: Конструктор CV з валідацією полів',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'Перегляд CV з принаймні двома шаблонами',
                'description': 'функціональність: Перегляд CV з принаймні двома шаблонами',
                'points': 4.0,
                'type': 'main',
            },
            {
                'name': 'Експорт CV у чистий PDF',
                'description': 'функціональність: Експорт CV у чистий PDF',
                'points': 3.5,
                'type': 'main',
            },
            {
                'name': 'Модуль інтерв\'ю (5-8 питань, таймер, звіт)',
                'description': 'функціональність: Модуль інтерв\'ю (5-8 питань, таймер, звіт)',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'Дашборд та функція "видалити дані"',
                'description': 'функціональність: Дашборд та функція "видалити дані"',
                'points': 2.5,
                'type': 'main',
            },
        ]
        
        # Main criteria - UI/UX and stability
        ui_ux = [
            {
                'name': 'Чистий інтерфейс, контраст, читабельність',
                'description': 'UI/UX: Чистий інтерфейс, контраст, читабельність',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'Адаптивний або нативний вигляд для цільової платформи',
                'description': 'UI/UX: Адаптивний або нативний вигляд для цільової платформи',
                'points': 5.0,
                'type': 'main',
            },
        ]
        
        # Main criteria - Engineering quality
        engineering = [
            {
                'name': 'Структура коду, модульність, лаконічність',
                'description': 'інженерних рішень: Структура коду, модульність, лаконічність',
                'points': 4.0,
                'type': 'main',
            },
            {
                'name': 'Модель даних, валідація, обробка помилок',
                'description': 'інженерних рішень: Модель даних, валідація, обробка помилок',
                'points': 3.0,
                'type': 'main',
            },
            {
                'name': 'Безпека даних',
                'description': 'інженерних рішень: Безпека даних',
                'points': 5.0,
                'type': 'main',
            },
            {
                'name': 'README та артефакти',
                'description': 'інженерних рішень: README та артефакти',
                'points': 3.0,
                'type': 'main',
            },
        ]
        
        # Main criteria - Project explanation
        explanation = [
            {
                'name': 'Розуміння та здатність пояснити ключові частини',
                'description': 'пояснення проекту: Розуміння та здатність пояснити ключові частини',
                'points': 10.0,
                'type': 'main',
            },
        ]
        
        # Bonus criteria - Vector A (Mobile App)
        vector_a = [
            {
                'name': 'Експорт CV у формати крім PDF',
                'description': 'Експорт CV у формати крім PDF',
                'points': 3.0,
                'type': 'bonus',
                'service': 'A',
            },
            {
                'name': 'Багатомовний інтерфейс',
                'description': 'Багатомовний інтерфейс',
                'points': 3.0,
                'type': 'bonus',
                'service': 'A',
            },
            {
                'name': 'Історія змін CV з часовими мітками',
                'description': 'Історія змін CV з часовими мітками',
                'points': 3.0,
                'type': 'bonus',
                'service': 'A',
            },
            {
                'name': 'CI/CD артефакт збірки',
                'description': 'CI/CD артефакт збірки',
                'points': 4.5,
                'type': 'bonus',
                'service': 'A',
            },
            {
                'name': 'Статичний аналіз та суворі правила якості',
                'description': 'Статичний аналіз та суворі правила якості',
                'points': 1.5,
                'type': 'bonus',
                'service': 'A',
            },
        ]
        
        # Bonus criteria - Vector B (Web App)
        vector_b = [
            {
                'name': 'Використання TypeScript замість JavaScript',
                'description': 'Використання TypeScript замість JavaScript',
                'points': 1.5,
                'type': 'bonus',
                'service': 'B',
            },
            {
                'name': 'Десктопна збірка з Tauri/Electron',
                'description': 'Десктопна збірка з Tauri/Electron',
                'points': 4.5,
                'type': 'bonus',
                'service': 'B',
            },
            {
                'name': 'Експорт DOCX (клієнтський або серверний)',
                'description': 'Експорт DOCX (клієнтський або серверний)',
                'points': 3.0,
                'type': 'bonus',
                'service': 'B',
            },
            {
                'name': 'Багатомовний інтерфейс',
                'description': 'Багатомовний інтерфейс',
                'points': 3.0,
                'type': 'bonus',
                'service': 'B',
            },
            {
                'name': 'Історія змін CV з можливістю відкату',
                'description': 'Історія змін CV з можливістю відкату',
                'points': 3.0,
                'type': 'bonus',
                'service': 'B',
            },
        ]
        
        # Bonus criteria - Vector C (Telegram Bot)
        vector_c = [
            {
                'name': 'Експорт CV у PDF прямо в чаті',
                'description': 'Експорт CV у PDF прямо в чаті',
                'points': 3.0,
                'type': 'bonus',
                'service': 'C',
            },
            {
                'name': 'Багатомовний /lang (uk/en)',
                'description': 'Багатомовний /lang (uk/en)',
                'points': 3.0,
                'type': 'bonus',
                'service': 'C',
            },
            {
                'name': 'Історія змін CV з логом /history',
                'description': 'Історія змін CV з логом /history',
                'points': 3.0,
                'type': 'bonus',
                'service': 'C',
            },
            {
                'name': 'Telegram WebApp для перегляду CV/дашборду',
                'description': 'Telegram WebApp для перегляду CV/дашборду',
                'points': 4.5,
                'type': 'bonus',
                'service': 'C',
            },
            {
                'name': 'Експорт DOCX та доставка в чат',
                'description': 'Експорт DOCX та доставка в чат',
                'points': 1.5,
                'type': 'bonus',
                'service': 'C',
            },
        ]
        
        # Combine all criteria
        all_criteria = (
            main_functionality + 
            ui_ux + 
            engineering + 
            explanation + 
            vector_a + 
            vector_b + 
            vector_c
        )
        
        # Create criteria objects
        for criteria_data in all_criteria:
            Criteria.objects.create(**criteria_data)
            self.stdout.write(f'Created criteria: {criteria_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(all_criteria)} criteria'))