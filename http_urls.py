from django.urls import path, include
from rest_framework import routers
from feed.views.bday import BirthdayViewSet, PersonalDetails
from feed.views.bit import BitViewSet

app_name = 'feed'

router = routers.SimpleRouter()
router.register('bit', BitViewSet, basename='bit')
router.register('birthday', BirthdayViewSet, basename='birthday')

urlpatterns = [
    path('', include(router.urls)),
    path('personal_details/', PersonalDetails.as_view(), name='personaldetails'),
]
