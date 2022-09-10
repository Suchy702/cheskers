# Generated by Django 4.1.1 on 2022-09-10 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MatchmakingQueueModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.playermodel')),
            ],
        ),
        migrations.CreateModel(
            name='GameSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chess_player_joined', models.BooleanField(default=False)),
                ('checkers_player_joined', models.BooleanField(default=False)),
                ('session_url', models.TextField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('ONGOING', 'ongoing'), ('ABORTED', 'aborted'), ('CHESS_WON', 'chess_won'), ('CHECKERS_WON', 'checkers_won'), ('CHESS_TIMEOUT', 'chess_timeout'), ('CHECKERS_TIMEOUT', 'checkers_timeout')], max_length=20)),
                ('which_player_turn', models.IntegerField(default=0)),
                ('board', models.JSONField()),
                ('checkers_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.playermodel')),
                ('chess_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.playermodel')),
            ],
        ),
    ]
