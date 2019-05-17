from rest_framework import serializers

from configuration.serializers.app.app import AppSerializer
from feed.models import Bit
from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class BitSerializer(serializers.ModelSerializer):
    """
    Serializer for Bit objects
    """

    person = AvatarSerializer(
        read_only=True
    )

    reported = serializers.SerializerMethodField(
        read_only=True,
    )
    new_reported = serializers.BooleanField(
        write_only=True,
        required=False,
    )

    app = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        """
        Meta class for BitSerializer
        """

        model = Bit
        fields = [
            'id',
            'datetime_created',
            'person',
            'app',
            'text',
            'url',
            'image',
            'reported',
            'new_reported',
        ]
        read_only_fields = [
            'app',
            'text',
            'url',
            'image',
            'reported',
        ]

    def get_reported(self, instance):
        """
        Return the report status of the instance for the logged-in person
        :return: True if the logged-in person has reported, False otherwise
        """

        person = self.context.get('request').person
        return instance.has_reported(person)

    def get_app(self, instance):
        """
        Expand the app referred to in the bit using the AppSerializer
        :return: the expanded dictionary of the app is allowed, None otherwise
        """

        available = self.context.get('available')
        for (app, app_configuration) in available:
            if app == instance.app_name:
                return AppSerializer(app_configuration).data
        return None

    def create(self, validated_data):
        """
        Remove new_reported from the data and defer to the base implementation
        of the function
        :param validated_data: the data sent to the serializer to create
        :return: whatever the base implementation returns
        """

        if 'new_reported' in self.validated_data:
            del validated_data['new_reported']

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Handle reporting and defer to the base implementation of the function
        :param instance: the instance being updated
        :param validated_data: the new data for the instance
        :return: the updated instance
        """

        person = self.context.get('request').person
        new_reported = validated_data.pop('new_reported', None)
        if (
                new_reported is not None
                and not new_reported == instance.has_reported(person)
        ):
            instance.toggle_report(person)

        return super().update(instance, validated_data)
