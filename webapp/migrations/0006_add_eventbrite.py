from django.db import migrations

class Migration(migrations.Migration):
    initial = False
    dependencies = [
        ('webapp', '0004_auto_20170502_1929')
    ]

    operations = [
        migrations.RunSQL(["INSERT INTO webapp_services (Name, IsEnabled) VALUES ('Eventbrite', true);"])
    ]
