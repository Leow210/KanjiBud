from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KanjiViewSet, register, Logout, StudyListViewSet, get_kanjis, get_user_info, AddKanjiToStudyList, PremadeStudyListViewSet
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import get_kanjis





router = DefaultRouter()
router.register(r'kanjis', KanjiViewSet)
router.register(r'studylists', StudyListViewSet)
router.register(r'premadestudylists', PremadeStudyListViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('userinfo/', get_user_info, name='user-info'),
    #path('studylists/<int:list_id>/add_kanji/<int:kanji_id>/', add_kanji_to_list, name='add_kanji_to_list'),
    path('studylists/<int:list_id>/kanjis/', AddKanjiToStudyList.as_view()),
    path('register/', register, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('kanjis/', get_kanjis, name='kanji-list'),
    path('', include(router.urls)),
]