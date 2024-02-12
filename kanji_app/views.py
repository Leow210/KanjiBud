from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Kanji, UserKanji, Quiz, QuizQuestion, StudyList, PremadeStudyList
from .serializers import KanjiSerializer, UserKanjiSerializer, StudyListSerializer, QuizQuestionSerializer, PremadeStudyListSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
import random #for quizzes
from django.http import JsonResponse
import logging
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie





@ensure_csrf_cookie
def set_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

logger = logging.getLogger(__name__)

def my_view(request):
    # Your view logic
    logger.info('Info message from my_view')
    logger.error('Error message from my_view')

    

    

# Create your views here.
class KanjiViewSet(viewsets.ModelViewSet):
    queryset = Kanji.objects.all()
    serializer_class = KanjiSerializer

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username = username, password = password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserKanjiViewSet(viewsets.ModelViewSet):
    queryset = UserKanji.objects.all()
    serializer_class = UserKanjiSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class QuizView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         questions = list(QuizQuestion.objects.all())
#         random.shuffle(questions)
#         questions = questions[:10]  
#         serializer = QuizQuestionSerializer(questions, many=True)
#         return Response(serializer.data)

def get_kanjis(request):
    search = request.GET.get('search', '')
    kanjis = Kanji.objects.filter(character__icontains=search)
    kanjis_list = list(kanjis.values())
    print(kanjis.query)  # Check the executed query
    return JsonResponse(kanjis_list, safe=False)

class StudyListViewSet(viewsets.ModelViewSet):
    queryset = StudyList.objects.all()
    serializer_class = StudyListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        #get only the lists that belong to current user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        #assigns user to current user upon creation
        serializer.save(user=self.request.user)


    

# @api_view(['POST'])
# def add_kanji_to_list(request, list_id, kanji_id):
#     try:
#         study_list = StudyList.objects.get(id=list_id, user=request.user)
#         kanji = get_object_or_404(Kanji, pk=kanji_id)
#         study_list.kanjis.add(kanji)
#         return Response({'status': 'success'}, status=status.HTTP_200_OK)
#     except StudyList.DoesNotExist:
#         return Response({'status': 'error', 'message': 'Study list not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Kanji.DoesNotExist:
#         return Response({'status': 'error', 'message': 'Kanji not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_info(request):
    # Assuming you are using Token Authentication
    token = request.auth
    user = Token.objects.get(key=token).user if token else None
    if user:
        return Response({'username': user.username})
    return Response(status=status.HTTP_404_NOT_FOUND)


class AddKanjiToStudyList(APIView):
    def post(self, request, list_id, format=None):
        study_list = StudyList.objects.get(id=list_id)
        kanji_id = request.data.get('kanji_id')
        kanji = Kanji.objects.get(id=kanji_id)
        study_list.kanjis.add(kanji)
        return Response({'status': 'kanji added'})
    

class GenerateQuiz(APIView):
    def post(self, request, *args, **kwargs):
        study_list_id = request.data.get('study_list_id')
        #add more parameters here:

        if study_list_id:
            study_list = StudyList.objects.get(id=study_list_id, user=request.user)
            kanji_ids = study_list.kanjis.values_list('id', flat=True)
            #now have list of kanji ids to generate questions from
            #add more logic here to generate questions

        # Create a new Quiz object with the generated questions
        quiz = Quiz(user=request.user, study_list=study_list)
        # Add other quiz properties based on the request
        quiz.save()

        # Return the newly created quiz
        return Response(QuizSerializer(quiz).data)
    

class PremadeStudyListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PremadeStudyList.objects.all()
    serializer_class = PremadeStudyListSerializer