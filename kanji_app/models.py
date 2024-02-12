from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Kanji(models.Model):
    character = models.CharField(max_length=2, unique=True)
    strokes = models.IntegerField(blank=True, null=True)
    kanken_level = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    jlpt_old = models.IntegerField(null=True, blank=True)
    jlpt_new = models.IntegerField(null=True, blank=True)
    meanings = models.JSONField()  # Stores a list of meanings
    readings_on = models.JSONField()  # Stores a list of On'yomi readings
    readings_kun = models.JSONField()  # Stores a list of Kun'yomi read
    wk_level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.character


class KanjiList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #if user is deleted so are all kanji lists
    name = models.CharField(max_length = 100)
    kanjis = models.ManyToManyField(Kanji)

class UserKanji(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    learned = models.BooleanField(default=False)
    last_studied = models.DateField(auto_now=True)
    review_score = models.IntegerField(default=0)  

    class Meta:
        unique_together = ('user', 'kanji')  #make sureone user per pair



class StudyList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanjis = models.ManyToManyField(Kanji)  

    def __str__(self):
        return self.name
    

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    level = models.IntegerField()
    kanjis = models.ManyToManyField(Kanji)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_list = models.ForeignKey(StudyList, on_delete=models.SET_NULL, null=True, blank=True)

class QuizQuestion(models.Model):

    MULTIPLE_CHOICE = 'multiple_choice'
    FILL_IN_THE_BLANK = 'fill_in_the_blank'
    MATCHING = 'matching'

    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (FILL_IN_THE_BLANK, 'Fill in the Blank'),
        (MATCHING, 'Matching'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', null=True)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, default=MULTIPLE_CHOICE) 
    #multiple choice
    choices = models.JSONField(blank=True, null=True)  #store choices as json

    #matching
    matches = models.JSONField(blank=True, null=True)  #stores pairs of matching items as json

    correct_answer = models.CharField(max_length=255)

    def check_answer(self, answer):
        return answer == self.correct_answer
    
class PremadeStudyList(models.Model):
    name = models.CharField(max_length=255)
    kanjis = models.ManyToManyField(Kanji)

    def __str__(self):
        return self.name
    