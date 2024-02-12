from rest_framework import serializers
from .models import Kanji, KanjiList, UserKanji, StudyList, QuizQuestion, PremadeStudyList

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanji
        fields = '__all__'

class KanjiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanji
        fields = '__all__'

class UserKanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKanji
        fields = '__all__'

class StudyListSerializer(serializers.ModelSerializer):
    kanjis = KanjiSerializer(many=True, read_only=True)  # Nested serialization for Kanji

    class Meta:
        model = StudyList
        fields = ('id', 'name', 'kanjis', 'user') 
        read_only_fields = ('user',)  #make user readonly so it can't be changed directly

    def create(self, validated_data):
        #a custom create method to handle the creation of a study list with the associated Kanji
        kanjis_data = validated_data.pop('kanjis', None)  #extract kanji data
        study_list = StudyList.objects.create(**validated_data)  #then create  study list
        
        if kanjis_data:
            for kanji_data in kanjis_data:
                data
                kanji, created = Kanji.objects.get_or_create(**kanji_data)
                study_list.kanjis.add(kanji)

        return study_list

    def update(self, instance, validated_data):
        #a custom update method to handle the update of a study list with the associated Kanji
        instance.name = validated_data.get('name', instance.name)  #update the name
        instance.save()

        if 'kanjis' in validated_data:
            #clear the current kanjis and add the new ones
            instance.kanjis.clear()
            for kanji_data in validated_data['kanjis']:
                kanji, created = Kanji.objects.get_or_create(**kanji_data)
                instance.kanjis.add(kanji)

        return instance

class QuizQuestionSerializer(serializers.ModelSerializer):
    kanji = KanjiSerializer(read_only=True)  # Nested serialization for related Kanji
    kanji_id = serializers.PrimaryKeyRelatedField(
        queryset=Kanji.objects.all(),  # Or any other queryset that filters Kanji as per your logic
        source='kanji',
        write_only=True
    )  # To handle input for Kanji as an ID

    class Meta:
        model = QuizQuestion
        fields = ('id', 'kanji', 'kanji_id', 'correct_answer', 'option_1', 'option_2', 'option_3')
        extra_kwargs = {
            'correct_answer': {'write_only': True}  # correct_answer should not be sent to the client
        }

    def create(self, validated_data):
        # Create method for QuizQuestion, utilizing nested Kanji data if necessary
        # Since kanji is read-only, it will be handled by the 'kanji_id' field
        return QuizQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #update for QuizQuestion, utilizing nested Kanji data if necessary
        instance.correct_answer = validated_data.get('correct_answer', instance.correct_answer)
        instance.option_1 = validated_data.get('option_1', instance.option_1)
        instance.option_2 = validated_data.get('option_2', instance.option_2)
        instance.option_3 = validated_data.get('option_3', instance.option_3)
        #update the kanji if necessary (if the kanji_id is provided)
        if 'kanji' in validated_data:
            kanji_data = validated_data.pop('kanji')
            kanji = instance.kanji
            KanjiSerializer.update(kanji, kanji_data)
        instance.save()
        return instance
    
class PremadeStudyListSerializer(serializers.ModelSerializer):
    kanjis = KanjiSerializer(many=True, read_only=True)
    class Meta:
        model = PremadeStudyList
        fields = '__all__'