import datetime

from django.db import models
from django.contrib.auth.models import User

from fossil.fields import FossilForeignKey
from fossil.models import Fossil

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    starred = models.BooleanField(default=False, blank=True)
    points = models.IntegerField(default=0, blank=True)
    date_foundation = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def fossil_revisions(self):
        return Fossil.objects.fossils_of_object(self)

class Purchase(models.Model):
    date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    supplier = FossilForeignKey(Supplier, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)

    def fossil_revisions(self):
        return Fossil.objects.fossils_of_object(self)

from django.db.models import signals

def purchase_post_save(instance, **kwargs):
    fossil = Fossil.objects.create_for_object(instance)

    fossil.set_indexer('pk', instance.pk)
    fossil.set_indexer('date', instance.date.strftime('%d/%m/%Y'))

signals.post_save.connect(purchase_post_save, sender=Purchase)

