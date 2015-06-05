# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad_attr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad_attr_value', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'ad_attr',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('advertisement_id', models.AutoField(serialize=False, primary_key=True)),
                ('price', models.IntegerField()),
                ('original_price', models.IntegerField(null=True)),
                ('period_of_use', models.CharField(max_length=512)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'advertisement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Advertisement_notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('advertisement_id', models.ForeignKey(to='fidel_app.Advertisement')),
            ],
            options={
                'db_table': 'advertisement_notification',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Advertisement_pictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'')),
                ('advertisement_id', models.ForeignKey(to='fidel_app.Advertisement')),
            ],
            options={
                'db_table': 'ad_pictures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('attribute_id', models.AutoField(serialize=False, primary_key=True)),
                ('attribute_name', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'attribute',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Connected_notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'connected_notification',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Connected_to',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'connected_to',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Custom_user',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=512)),
                ('last_name', models.CharField(max_length=512)),
                ('email_id', models.EmailField(max_length=512)),
                ('password', models.CharField(max_length=512)),
                ('street_name', models.CharField(max_length=512, null=True)),
                ('house_number', models.CharField(max_length=512, null=True)),
                ('city', models.CharField(max_length=512, null=True)),
                ('pin_code', models.IntegerField(null=True)),
                ('profile_picture', models.ImageField(default=b'media/motivation1.jpeg', null=True, upload_to=b'/media/')),
            ],
            options={
                'db_table': 'custom_user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item_attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_value', models.CharField(max_length=512, null=True)),
                ('attribute_id', models.ForeignKey(to='fidel_app.Attribute')),
            ],
            options={
                'db_table': 'Item_attribute',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item_type',
            fields=[
                ('item_id', models.AutoField(serialize=False, primary_key=True)),
                ('item_name', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'item_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=512)),
                ('timestamp', models.DateTimeField()),
                ('user1', models.ForeignKey(related_name=b'message_user1', to='fidel_app.Custom_user')),
                ('user2', models.ForeignKey(related_name=b'message_user2', to='fidel_app.Custom_user')),
            ],
            options={
                'db_table': 'message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pending_request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver_id', models.ForeignKey(related_name=b'pending_request_receiver', to='fidel_app.Custom_user')),
                ('sender_id', models.ForeignKey(related_name=b'pending_request_sender', to='fidel_app.Custom_user')),
            ],
            options={
                'db_table': 'pending_request',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Req_attr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('req_attr_value', models.CharField(max_length=512)),
                ('attribute_id', models.ForeignKey(to='fidel_app.Attribute')),
            ],
            options={
                'db_table': 'req_attr',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('requirement_id', models.AutoField(serialize=False, primary_key=True)),
                ('max_price', models.IntegerField()),
                ('max_period_of_use', models.CharField(max_length=512)),
                ('buyer_id', models.ForeignKey(to='fidel_app.Custom_user')),
                ('item_type_id', models.ForeignKey(to='fidel_app.Item_type')),
            ],
            options={
                'db_table': 'requirement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_phone_number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=512)),
                ('user_id', models.ForeignKey(to='fidel_app.Custom_user')),
            ],
            options={
                'db_table': 'user_phone_number',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='user_phone_number',
            unique_together=set([('user_id', 'phone_number')]),
        ),
        migrations.AddField(
            model_name='req_attr',
            name='requirement_id',
            field=models.ForeignKey(to='fidel_app.Requirement'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='req_attr',
            unique_together=set([('requirement_id', 'attribute_id', 'req_attr_value')]),
        ),
        migrations.AlterUniqueTogether(
            name='pending_request',
            unique_together=set([('sender_id', 'receiver_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('user1', 'user2', 'timestamp')]),
        ),
        migrations.AddField(
            model_name='item_attribute',
            name='item_type_id',
            field=models.ForeignKey(to='fidel_app.Item_type'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='item_attribute',
            unique_together=set([('item_type_id', 'attribute_id', 'attribute_value')]),
        ),
        migrations.AddField(
            model_name='connected_to',
            name='user1',
            field=models.ForeignKey(related_name=b'connected_to_user1', to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connected_to',
            name='user2',
            field=models.ForeignKey(related_name=b'connected_to_user2', to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='connected_to',
            unique_together=set([('user1', 'user2')]),
        ),
        migrations.AddField(
            model_name='connected_notification',
            name='receiver_id',
            field=models.ForeignKey(related_name=b'connected_to_receiver', to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connected_notification',
            name='sender_id',
            field=models.ForeignKey(related_name=b'connected_to_sender', to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='connected_notification',
            unique_together=set([('sender_id', 'receiver_id', 'timestamp')]),
        ),
        migrations.AlterUniqueTogether(
            name='advertisement_pictures',
            unique_together=set([('advertisement_id', 'picture')]),
        ),
        migrations.AddField(
            model_name='advertisement_notification',
            name='user_id',
            field=models.ForeignKey(to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='advertisement_notification',
            unique_together=set([('user_id', 'advertisement_id')]),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='item_type_id',
            field=models.ForeignKey(to='fidel_app.Item_type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advertisement',
            name='seller_id',
            field=models.ForeignKey(to='fidel_app.Custom_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ad_attr',
            name='advertisement_id',
            field=models.ForeignKey(to='fidel_app.Advertisement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ad_attr',
            name='attribute_id',
            field=models.ForeignKey(to='fidel_app.Attribute'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ad_attr',
            unique_together=set([('advertisement_id', 'attribute_id')]),
        ),
        migrations.CreateModel(
            name='Circles',
            fields=[
            ],
            options={
                'db_table': 'circles',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DegreeThree',
            fields=[
            ],
            options={
                'db_table': 'degree_three',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DegreeTwo',
            fields=[
            ],
            options={
                'db_table': 'degree_two',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
