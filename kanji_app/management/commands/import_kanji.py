import json
from django.core.management.base import BaseCommand
from kanji_app.models import Kanji  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Import Kanji from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        with open(options['json_file'], 'r', encoding='utf-8') as file:
            data = json.load(file)
            for character, details in data.items():
                kanji, created = Kanji.objects.get_or_create(
               
                    character=character,
                    defaults= {
                        'strokes': details['strokes'],
                        'kanken_level': details['kanken_level'],
                        'frequency': details['freq'],
                        'jlpt_old': details.get('jlpt_old'),  # Use .get() for optional fields
                        'jlpt_new': details.get('jlpt_new'),
                        'meanings': details['meanings'],
                        'readings_on': details['readings_on'],
                        'readings_kun': details['readings_kun'],
                        'wk_level': details['wk_level'],
                        # Map other fields as necessary
                    }
                )

                if not created:
                    # Record already exists, you can choose to update it or simply pass
                    pass
        self.stdout.write(self.style.SUCCESS(f"Successfully imported Kanji from {options['json_file']}"))