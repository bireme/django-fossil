import hashlib, datetime

from django.db import models
from django.core.serializers import serialize, deserialize
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class FossilManager(models.Manager):
    def create_for_object(self, obj):
        try:
            serialized = obj.serialize_for_fossil()
        except AttributeError:
            serialized = serialize('json', [obj])

        hash_key = hashlib.sha256(serialized).hexdigest()

        return Fossil.objects.get_or_create(
                pk=hash_key,
                defaults={
                    'serialized': serialized,
                    'display_text': unicode(obj),
                    'content_type': ContentType.objects.get_for_model(obj),
                    'object_id': unicode(obj.pk),
                    },
                )[0]

    def fossils_of_object(self, obj):
        """
        Returns a list of fossils of a given object, ordered by date
        """
        qs = self.get_query_set()
        c_type = ContentType.objects.get_for_model(obj)

        return qs.filter(content_type=c_type, object_id=obj.pk).order_by('creation')

class Fossil(models.Model):
    objects = FossilManager()

    id = models.CharField(max_length=64, primary_key=True)
    serialized = models.TextField(blank=True, default='')
    display_text = models.TextField(blank=True, default='')
    creation = models.DateTimeField(blank=True, default=datetime.datetime.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    object = GenericForeignKey()

    def __unicode__(self):
        return self.display_text

    def get_object_fossil(self):
        """
        Returns the stored version of this object.
        """

        data = self.serialized

        if isinstance(data, unicode):
            data = data.encode("utf8")

        try:
            return self.content_type.model_class.objects.deserialize_for_fossil(data)
        except AttributeError:
            return list(deserialize('json', data))[0]
    

