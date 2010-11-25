import hashlib, datetime

from django.db import models
from django.core.serializers import serialize, deserialize
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class FossilManager(models.Manager):
    def create_for_object(self, obj):
        if hasattr(obj, 'serialize_for_fossil'):
            serialized = obj.serialize_for_fossil()
        else:
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

    def indexed(self, **kwargs):
        """
        Find fossils by fossil indexes
        """
        qs = self.get_query_set()

        # Find all indexes by given key and value
        indexeds = FossilIndexer.objects.all()
        for k,v in kwargs.items():
            indexeds = indexeds.filter(**{'key': k, 'value': v})

        pks = indexeds.distinct().values_list('fossil', flat=True)

        return qs.filter(pk__in=pks)

class Fossil(models.Model):
    objects = FossilManager()

    id = models.CharField(max_length=64, primary_key=True)
    serialized = models.TextField(blank=True, default='')
    display_text = models.TextField(blank=True, default='')
    creation = models.DateTimeField(blank=True, default=datetime.datetime.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    object = GenericForeignKey()
    is_most_recent = models.BooleanField(blank=True, default=True, db_index=True)
    previous_revision = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.display_text

    def get_object_fossil(self):
        """
        Returns the stored version of this object.
        """

        data = self.serialized

        if isinstance(data, unicode):
            data = data.encode("utf8")

        manager = self.content_type.model_class().objects
        if hasattr(manager, 'deserialize_for_fossil'):
            return manager.deserialize_for_fossil(data)
        else:
            return list(deserialize('json', data))[0]
    
class FossilIndexer(models.Model):
    """
    Class used to index fossil by field values. This is a sollution for querying
    fossils withouth use search in the field 'serialized'. Of course, this is
    because index + join is faster than like.
    """
    class Meta:
        unique_together = (
                ('fossil','key','value'),
                )

    fossil = models.ForeignKey('Fossil', related_name='indexeds')
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

# SIGNALS
from django.db.models import signals

def fossil_post_save(sender, instance, signal, **kwargs):
    # Updates old revisions setting them with "is_most_recent" as False
    if instance.is_most_recent:
        Fossil.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                creation__lt=instance.creation,
                is_most_recent=True,
                ).exclude(
                        pk=instance.pk,
                        ).update(
                                is_most_recent=False,
                                )

    # Gets "previous_revision" from last one
    if not instance.previous_revision:
        try:
            instance.previous_revision = Fossil.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                creation__lt=instance.creation,
                ).exclude(
                    pk=instance.pk,
                    ).latest('creation')
            instance.save()
        except Fossil.DoesNotExist:
            pass

signals.post_save.connect(fossil_post_save, sender=Fossil)

