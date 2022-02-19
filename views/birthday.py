import datetime
import swapper

from django import urls
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from feed.serializers.birthday import PersonSerializer, BiologicalInfoSerializer
from shell.models.roles.student import Student
from feed.constants import BIRTHDAY_CACHE_LIST, TIME_DELTA_MAP, TIME_MIDNIGHT, DATE_FORMAT

Person = swapper.load_model('kernel', 'Person')
BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')

class PersonalDetails(
    GenericAPIView
):
    """
    This view shows some personal information of the currently logged in user
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """
        person = request.person
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BirthdayViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for users information related to birthdate
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = BiologicalInfoSerializer

    def get_queryset(self):
        person_ids = Student.objects.values_list('person', flat=True)
        param = self.request.GET.get('bdayDay')
        if param not in BIRTHDAY_CACHE_LIST:
            return None
        queryset = cache.get(param , None)
        if queryset is not None:
            return queryset
        month = (datetime.date.today() +
                     datetime.timedelta(days=TIME_DELTA_MAP[param])).month
        day = (datetime.date.today() +
                   datetime.timedelta(days=TIME_DELTA_MAP[param])).day
        queryset = BiologicalInformation.objects.filter(
            date_of_birth__month=month, date_of_birth__day=day).filter(person_id__in=person_ids)
        time_now = str(datetime.datetime.now().strftime(DATE_FORMAT))
        difference = datetime.datetime.strptime(
            TIME_MIDNIGHT, DATE_FORMAT) - datetime.datetime.strptime(time_now, DATE_FORMAT)
        cache.set(param, queryset, timeout=difference.seconds)
        return queryset
