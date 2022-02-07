from django.urls import path, include
from rest_framework import routers
from feed.views.bday import bdayViewSet, whoAmI
from feed.views.bit import BitViewSet

app_name = 'feed'

router = routers.SimpleRouter()
router.register('bit', BitViewSet, basename='bit')
router.register('birthday', bdayViewSet, basename='birthday')

urlpatterns = [
    path('', include(router.urls)),
    path('who_am_i/', whoAmI.as_view(), name='whoami'),
]
