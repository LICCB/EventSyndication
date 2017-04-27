from django.db import migrations

class Migration(migrations.Migration):
    initial = False
    dependencies = [
        ('webapp', '0001_initial'),
        ('webapp', '0002_google_service')
    ]

    operations = [
        migrations.RunSQL(["UPDATE webapp_services SET Name = 'Google Calendar' WHERE Name = 'Googlecal';"])
    ]
