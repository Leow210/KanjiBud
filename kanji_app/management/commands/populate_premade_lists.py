from django.core.management.base import BaseCommand
from kanji_app.models import Kanji, PremadeStudyList  # Adjust the import path according to your app structure

class Command(BaseCommand):
    help = 'Populates the database with premade study lists based on JLPT and Kanken levels.'

    def handle(self, *args, **options):
        # For each JLPT level
        for level in range(1, 6):  # JLPT levels N1 to N5
            kanjis = Kanji.objects.filter(jlpt_new=level)
            list, created = PremadeStudyList.objects.get_or_create(name=f'JLPT N{level}')
            list.kanjis.set(kanjis)
            self.stdout.write(self.style.SUCCESS(f'Successfully populated JLPT N{level} list with {kanjis.count()} kanjis'))

        # Repeat for Kanken levels, adjusting the range as necessary
        for level in range(1, 11):  # Example: Kanken levels 1 to 10
            kanjis = Kanji.objects.filter(kanken_level=level)
            list, created = PremadeStudyList.objects.get_or_create(name=f'Kanken Level {level}')
            list.kanjis.set(kanjis)
            self.stdout.write(self.style.SUCCESS(f'Successfully populated Kanken Level {level} list with {kanjis.count()} kanjis'))
