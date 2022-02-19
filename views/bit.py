from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from discovery.available import available_apps
from feed.models import Bit
from feed.serializers.bit import BitSerializer


class BitViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for RUD of Bit objects
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = BitSerializer

    def get_serializer_context(self):
        """
        Add the available apps to the serializer
        :return: the new context with available apps
        """

        available = available_apps(
            request=self.request,
        )
        context = super().get_serializer_context()
        context['available'] = available
        return context

    def get_queryset(self):
        """
        Get a queryset of Bit objects filtered by the apps that are allowed
        :return: a queryset of filtered Bit objects
        """

        available = available_apps(
            request=self.request,
        )
        apps = [
            app
            for (app, app_configuration)
            in available
        ]
        filtered_queryset = Bit.objects.filter(app_name__in=apps)
        ordered_queryset = filtered_queryset.order_by('-datetime_created')
        return ordered_queryset