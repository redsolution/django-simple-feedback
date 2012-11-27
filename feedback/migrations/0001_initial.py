# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResponseAttachments'
        db.create_table('feedback_responseattachments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedback.Response'])),
        ))
        db.send_create_signal('feedback', ['ResponseAttachments'])

        # Adding model 'Response'
        db.create_table('feedback_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('feedback', ['Response'])


    def backwards(self, orm):
        # Deleting model 'ResponseAttachments'
        db.delete_table('feedback_responseattachments')

        # Deleting model 'Response'
        db.delete_table('feedback_response')


    models = {
        'feedback.response': {
            'Meta': {'object_name': 'Response'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'feedback.responseattachments': {
            'Meta': {'object_name': 'ResponseAttachments'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedback.Response']"})
        }
    }

    complete_apps = ['feedback']