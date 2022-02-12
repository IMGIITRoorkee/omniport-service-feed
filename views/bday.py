from django import urls
import swapper
import datetime
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from feed.serializers.bday import PersonSerializer, BiologicalInfoSerializer
from shell.models.roles.student import Student
from feed.constants import Cache_dict, Delta_dict, Time_midnight, Date_format
Person = swapper.load_model('kernel', 'Person')
BiologicalInfo = swapper.load_model('kernel', 'BiologicalInformation')


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
        param = self.request.query_params.get('bdayDay')
        queryset = cache.get(Cache_dict[param])
        if not queryset:
            month = (datetime.date.today() +
                     datetime.timedelta(days=Delta_dict[param])).month
            day = (datetime.date.today() +
                   datetime.timedelta(days=Delta_dict[param])).day
            queryset = BiologicalInfo.objects.filter(
                date_of_birth__month=month, date_of_birth__day=day).filter(person_id__in=person_ids)
            time_now = str(datetime.datetime.now().strftime(Date_format))
            difference = datetime.datetime.strptime(
                Time_midnight, Date_format) - datetime.datetime.strptime(time_now, Date_format)
            cache.set(Cache_dict[param], queryset, timeout=difference.seconds)
        return queryset
