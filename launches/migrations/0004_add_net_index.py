# Generated migration for index lab demonstration
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('launches', '0003_alter_launch_failreason_alter_launch_hashtag_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='launch',
            index=models.Index(fields=['net'], name='launches_launch_net_idx'),
        ),
    ]
