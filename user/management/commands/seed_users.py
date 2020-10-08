from django_seed import Seed
from django.core.management.base import BaseCommand

from user.models import User

class Command(BaseCommand):
    help = '유저 생성 명령어'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int, help="얼마나 많은 수의 유저를 생성하시나요?"
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
            'is_staff': False,
            'is_admin': False,
            'is_active': True
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} 개의 유저가 생성되었습니다!'))
