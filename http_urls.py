from django.urls import path, include
from rest_framework import routers

from feed.views.bit import BitViewSet

app_name = 'feed'

router = routers.SimpleRouter()
router.register('bit', BitViewSet, base_name='bit')

urlpatterns = [
    path('', include(router.urls)),
]
