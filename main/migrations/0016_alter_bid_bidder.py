# Generated by Django 4.1.6 on 2023-06-25 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_alter_bid_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="bidder",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="main.enduser"
            ),
        ),
    ]
