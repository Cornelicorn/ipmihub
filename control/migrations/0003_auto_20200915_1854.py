# Generated by Django 3.0.3 on 2020-09-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_powerstatus_timeout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powerstatus',
            name='control_fault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='cooling_fault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='drive_fault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='fault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='front_panel_lockout',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='interlock',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='intrusion',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='last_event',
            field=models.CharField(max_length=17, null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='overload',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='power_on',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='powerstatus',
            name='restore_policy',
            field=models.IntegerField(null=True),
        ),
    ]
