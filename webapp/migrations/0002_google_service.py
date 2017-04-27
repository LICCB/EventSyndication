from django.db import migrations

class Migration(migrations.Migration):
    initial = False
    dependencies = [
        ('webapp', '0001_initial')
    ]

    operations = [
        migrations.RunSQL(["INSERT INTO webapp_services (Name, IsEnabled) VALUES ('Google Calendar', true);"])
    ]
