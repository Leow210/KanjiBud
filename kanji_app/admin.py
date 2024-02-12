from django.contrib import admin
from .models import Kanji, KanjiList, StudyList, PremadeStudyList
from django import forms

# Register your models here.

class StudyListForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = '__all__'
        widgets = {
            'kanjis': admin.widgets.FilteredSelectMultiple('Kanjis', is_stacked=False),
        }

class PremadeStudyListForm(forms.ModelForm):
    class Meta:
        model = PremadeStudyList
        fields = '__all__'
        widgets = {
            'kanjis': admin.widgets.FilteredSelectMultiple('Kanjis', is_stacked=False),
        }

class StudyListAdmin(admin.ModelAdmin):
    form = StudyListForm

class PremadeStudyListAdmin(admin.ModelAdmin):
    form = PremadeStudyListForm

admin.site.register(StudyList, StudyListAdmin)

admin.site.register(Kanji)
admin.site.register(KanjiList)
admin.site.register(PremadeStudyList, PremadeStudyListAdmin)
#admin.site.register(StudyList)

