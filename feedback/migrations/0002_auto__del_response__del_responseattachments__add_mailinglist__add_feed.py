# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Response'
        db.delete_table('feedback_response')

        # Deleting model 'ResponseAttachments'
        db.delete_table('feedback_responseattachments')

        # Adding model 'MailingList'
        db.create_table('feedback_mailinglist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('form', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('default_from', self.gf('django.db.models.fields.EmailField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('feedback', ['MailingList'])

        # Adding M2M table for field emails on 'MailingList'
        db.create_table('feedback_mailinglist_emails', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(orm['feedback.mailinglist'], null=False)),
            ('feedbackemail', models.ForeignKey(orm['feedback.feedbackemail'], null=False))
        ))
        db.create_unique('feedback_mailinglist_emails', ['mailinglist_id', 'feedbackemail_id'])

        # Adding model 'FeedbackEmail'
        db.create_table('feedback_feedbackemail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
        ))
        db.send_create_signal('feedback', ['FeedbackEmail'])


    def backwards(self, orm):
        # Adding model 'Response'
        db.create_table('feedback_response', (
            ('send_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('feedback', ['Response'])

        # Adding model 'ResponseAttachments'
        db.create_table('feedback_responseattachments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedback.Response'])),
        ))
        db.send_create_signal('feedback', ['ResponseAttachments'])

        # Deleting model 'MailingList'
        db.delete_table('feedback_mailinglist')

        # Removing M2M table for field emails on 'MailingList'
        db.delete_table('feedback_mailinglist_emails')

        # Deleting model 'FeedbackEmail'
        db.delete_table('feedback_feedbackemail')


    models = {
        'feedback.feedbackemail': {
            'Meta': {'object_name': 'FeedbackEmail'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'feedback.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'default_from': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'emails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'forms'", 'blank': 'True', 'to': "orm['feedback.FeedbackEmail']"}),
            'form': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['feedback']