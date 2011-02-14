# -*- encoding: utf-8 -*-

# django-fossil: immutable audit trails for interrelated model instances
#
# Copyright (C) 2010 BIREME/PAHO/WHO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import hashlib, datetime

from django.db import models
from django.core.serializers import serialize, deserialize
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

try:
    set
except:
    from sets import Set as set

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
        indexers_qs = FossilIndexer.objects.all()
        indexers = []
        for k,v in kwargs.items():
            # Field is the first node before '__' if there is one in the key (k)
            if '__' in k:
                field, lookup = k.split('__',1)
                filters = {'key': field, 'value__'+lookup: v}
            else:
                filters = {'key': k, 'value': v}

            # Appends lists of found fossil indexers (only their fossil PKs)
            indexers.append(set(indexers_qs.filter(**filters).distinct().values_list('fossil', flat=True)))

        # This reduce makes an intersection of all indexers, this means that only PKs found in
        # ALL indexers will be in new list 'pks'
        pks = reduce(lambda a,b: a.intersection(b), indexers)

        return qs.filter(pk__in=pks)

class Fossil(models.Model):
    objects = _default_manager = FossilManager()

    id = models.CharField(max_length=64, primary_key=True) # Hash key
    serialized = models.TextField(blank=True, default='')
    display_text = models.TextField(blank=True, default='')
    creation = models.DateTimeField(blank=True, default=datetime.datetime.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    object = GenericForeignKey()
    is_most_recent = models.BooleanField(blank=True, default=True, db_index=True)
    previous_revision = models.ForeignKey('self', null=True, blank=True)
    revision_sequential = models.PositiveIntegerField(null=True, blank=True, db_index=True)

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
            return list(deserialize('json', data))[0].object

    def set_indexer(self, key, value):
        """
        Creates (or updates if exists) a fossil index for this fossil + given key and value
        """
        indexer, new = FossilIndexer.objects.get_or_create(
                fossil=self,
                key=key,
                defaults=dict(value=value),
                )

        if not new and unicode(value) != indexer.value:
            indexer.value = value
            indexer.save()

    def unset_indexer(self, key):
        """Removes an indexer by a given key"""
        self.indexers.filter(key=key).delete()
    
class FossilIndexerManager(models.Manager):
    def key(self, key, fail_silent=False):
        try:
            qs = self.get_query_set()
            return qs.get(key=key)
        except FossilIndexer.DoesNotExist:
            if fail_silent:
                return None
            else:
                raise

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

    objects = _default_manager = FossilIndexerManager()

    fossil = models.ForeignKey('Fossil', related_name='indexers')
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250, null=True)

    def __unicode__(self):
        return u'%s = %s'%(self.key, self.value)

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

    # Gets next "revision_sequential"
    if not instance.revision_sequential:
        if not instance.previous_revision:
            instance.revision_sequential = 1
            instance.save()
        elif instance.previous_revision.revision_sequential:
            instance.revision_sequential = instance.previous_revision.revision_sequential + 1
            instance.save()

signals.post_save.connect(fossil_post_save, sender=Fossil)

