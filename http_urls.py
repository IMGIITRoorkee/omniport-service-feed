from django.urls import path, include
from rest_framework import routers
from feed.views.bday import *
from feed.views.bit import BitViewSet
from settings.views import *

app_name = 'feed'

router = routers.SimpleRouter()
router.register('bit', BitViewSet, basename='bit')
router.register('bday-today', bdayTodayViewSet, basename='bday-today')
router.register('bday-tom', bdayTomViewSet, basename='bday-tom')
router.register('bday-dat', bdayDaTViewSet, basename='bday-dat')

urlpatterns = [
    path('', include(router.urls)),
    path('who_am_i/', whoAmI.as_view(), name='whoami'),
]
