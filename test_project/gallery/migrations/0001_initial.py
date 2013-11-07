# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'gallery_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='categories', null=True, to=orm['gallery.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'gallery', ['Category'])

        # Adding model 'Photo'
        db.create_table(u'gallery_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='photos', to=orm['gallery.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'gallery', ['Photo'])

        # Adding unique constraint on 'Photo', fields ['slug', 'parent']
        db.create_unique(u'gallery_photo', ['slug', 'parent_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Photo', fields ['slug', 'parent']
        db.delete_unique(u'gallery_photo', ['slug', 'parent_id'])

        # Deleting model 'Category'
        db.delete_table(u'gallery_category')

        # Deleting model 'Photo'
        db.delete_table(u'gallery_photo')


    models = {
        u'gallery.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'categories'", 'null': 'True', 'to': u"orm['gallery.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'gallery.photo': {
            'Meta': {'unique_together': "(('slug', 'parent'),)", 'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'photos'", 'to': u"orm['gallery.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['gallery']