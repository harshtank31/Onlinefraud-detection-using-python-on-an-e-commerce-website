# Generated by Django 4.1.7 on 2023-03-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fraud_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='userDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(default=None, max_length=100, null=True)),
                ('Password', models.CharField(default=None, max_length=100, null=True)),
                ('Name', models.CharField(default=None, max_length=100, null=True)),
                ('Age', models.CharField(default=None, max_length=200, null=True)),
                ('Phone', models.CharField(default=None, max_length=100, null=True)),
                ('Email', models.CharField(default=None, max_length=100, null=True)),
                ('Address', models.CharField(default=None, max_length=100, null=True)),
                ('Card_Number', models.CharField(default=None, max_length=100, null=True)),
                ('cvv', models.CharField(default=None, max_length=100, null=True)),
                ('month', models.CharField(default=None, max_length=100, null=True)),
                ('year', models.CharField(default=None, max_length=100, null=True)),
                ('spending', models.CharField(default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'userDetails',
            },
        ),
    ]
