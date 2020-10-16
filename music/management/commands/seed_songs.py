import random

from django_seed import Seed
from django.core.management.base import BaseCommand

from music.models import Song
from user.models import User

class Command(BaseCommand):
    help = '신청곡 생성 명령어'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int, help="얼마나 많은 수의 신청곡 생성하시나요?"
        )

    def handle(self, *args, **options):
        user_count = User.objects.count()

        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(Song, number, {
            'is_played': False,
            'user': lambda x: User.objects.get(pk=random.randint(1, user_count - 1)),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} 개의 신청곡이 생성되었습니다!'))
