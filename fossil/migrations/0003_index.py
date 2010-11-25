# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FossilIndexer'
        db.create_table('fossil_fossilindexer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fossil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fossil.Fossil'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('fossil', ['FossilIndexer'])

        # Adding unique constraint on 'FossilIndexer', fields ['fossil', 'key', 'value']
        db.create_unique('fossil_fossilindexer', ['fossil_id', 'key', 'value'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FossilIndexer', fields ['fossil', 'key', 'value']
        db.delete_unique('fossil_fossilindexer', ['fossil_id', 'key', 'value'])

        # Deleting model 'FossilIndexer'
        db.delete_table('fossil_fossilindexer')


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
            'serialized': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'fossil.fossilindexer': {
            'Meta': {'unique_together': "(('fossil', 'key', 'value'),)", 'object_name': 'FossilIndexer'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'fossil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fossil.Fossil']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['fossil']
