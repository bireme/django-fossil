# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'FossilIndexer.value'
        db.alter_column('fossil_fossilindexer', 'value', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))


    def backwards(self, orm):
        
        # Changing field 'FossilIndexer.value'
        db.alter_column('fossil_fossilindexer', 'value', self.gf('django.db.models.fields.CharField')(max_length=250))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fossil.fossil': {
            'Meta': {'object_name': 'Fossil'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'is_most_recent': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fossil.Fossil']", 'null': 'True', 'blank': 'True'}),
            'revision_sequential': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'serialized': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'fossil.fossilindexer': {
            'Meta': {'unique_together': "(('fossil', 'key', 'value'),)", 'object_name': 'FossilIndexer'},
            'fossil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indexeds'", 'to': "orm['fossil.Fossil']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        }
    }

    complete_apps = ['fossil']
