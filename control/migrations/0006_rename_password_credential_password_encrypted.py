# Generated by Django 4.2.4 on 2024-04-27 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("control", "0005_credential_password_unencrypted"),
    ]

    operations = [
        migrations.RenameField(
            model_name="credential",
            old_name="password",
            new_name="password_encrypted",
        ),
    ]
