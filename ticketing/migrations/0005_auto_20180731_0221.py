# Generated by Django 2.0.4 on 2018-07-31 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0004_auto_20180515_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balanceticket',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_ticket', to='ticketing.Account'),
        ),
    ]
