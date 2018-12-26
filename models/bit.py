from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models
from django.db import models

from kernel.models.root import Model


class Bit(Model):
    """
    This model holds information about a bit of update in the news feed
    """

    app_name = models.CharField(
        max_length=63,
    )

    # Relationship with the contactable entity
    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
    )
    entity_object_id = models.PositiveIntegerField()
    entity = contenttypes_fields.GenericForeignKey(
        ct_field='entity_content_type',
        fk_field='entity_object_id',
    )

    @property
    def person(self):
        """
        Return the person to be displayed on the feed bit
        :return: the person to be displayed on the feed bit
        """

        entity = self.entity
        if entity is not None:
            return entity.feed_person  # Property on the feedable models

    @property
    def text(self):
        """
        Return the text to be displayed on the feed bit
        :return: the text to be displayed on the feed bit
        """

        entity = self.entity
        if entity is not None:
            return entity.feed_text  # Property on the feedable models

    @property
    def image(self):
        """
        Return the image to be displayed on the feed bit
        :return: the image to be displayed on the feed bit
        """

        entity = self.entity
        if entity is not None:
            return entity.feed_image  # Property on the feedable models

    @property
    def url(self):
        """
        Return the URL to which a feed bit should point
        :return: the URL to which a feed bit should point
        """

        entity = self.entity
        if entity is not None:
            return entity.feed_url  # Property on the feedable models

    def has_reported(self, person):
        """
        Return whether the person has reported the object or not
        :param person: the person whose report status is being checked
        :return: True if the person has reported the object, False otherwise
        """

        entity = self.entity
        if entity is not None:
            return entity.has_reported(person)

    def toggle_report(self, person):
        """
        Toggle the report status of the given object for the given person
        :param person: the person toggling his report against the object
        """

        entity = self.entity
        if entity is not None:
            entity.toggle_report(person)

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        app_name = self.app_name
        entity = self.entity
        return f'{app_name}: {entity}'
