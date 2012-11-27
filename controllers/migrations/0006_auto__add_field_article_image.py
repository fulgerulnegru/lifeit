# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Article.image'
        db.add_column('controllers_article', 'image', self.gf('django.db.models.fields.files.ImageField')(default=0, max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Article.image'
        db.delete_column('controllers_article', 'image')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 4, 6, 14, 59, 445726,)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 4, 6, 14, 59, 445455, )'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'controllers.article': {
            'Meta': {'object_name': 'Article'},
            'aprobat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'describe': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['controllers.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'controllers.file': {
            'Meta': {'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'controllers.links': {
            'Meta': {'object_name': 'Links'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'controllers.menu': {
            'Meta': {'object_name': 'Menu'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['controllers.Article']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'page': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['controllers.Page']", 'unique': 'True', 'null': 'True'}),
            'undermenu': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['controllers.UnderMenu']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'controllers.newslatter': {
            'Meta': {'object_name': 'Newslatter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cod': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'controllers.page': {
            'Meta': {'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'controllers.profile': {
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cod': ('django.db.models.fields.IntegerField', [], {}),
            'describe': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'controllers.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'controllers.undermenu': {
            'Meta': {'object_name': 'UnderMenu'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['controllers.Article']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'page': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['controllers.Page']", 'unique': 'True', 'null': 'True'}),
            'undermenu': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['controllers']
