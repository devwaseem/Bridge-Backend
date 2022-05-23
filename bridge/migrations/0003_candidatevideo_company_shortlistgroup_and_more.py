# Generated by Django 4.0.4 on 2022-05-18 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0002_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('thumbnail', models.ImageField(upload_to='candidate_video/thumbnail/')),
                ('video', models.FileField(upload_to='videos/')),
                ('transcript', models.TextField(max_length=4000, null=True)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'candidate_video',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='ShortlistGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'shortlist_group',
            },
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='education_type',
            field=models.CharField(choices=[('UNDERGRADUATE', 'Undergraduate'), ('POSTGRADUATE', 'Postgraduate'), ('PHD', 'PhD'), ('DROP_OUT', 'Drop out'), ('OTHER', 'Other')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='employment_type',
            field=models.CharField(choices=[('FULL_TIME', 'Full time'), ('PART_TIME', 'Part time'), ('INTERNSHIP', 'Internship'), ('FREELANCE', 'Freelance'), ('TRAINEE', 'Trainee'), ('STUDENT', 'Student')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelTable(
            name='candidateprofile',
            table='candidate_profile',
        ),
        migrations.CreateModel(
            name='ShortlistGroupVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shortlist_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.shortlistgroup')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.candidatevideo')),
            ],
            options={
                'db_table': 'shortlist_group_video_map',
            },
        ),
        migrations.AddField(
            model_name='shortlistgroup',
            name='videos',
            field=models.ManyToManyField(related_name='shortlist_groups', through='bridge.ShortlistGroupVideo', to='bridge.candidatevideo'),
        ),
        migrations.CreateModel(
            name='RecruiterProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'recruiter_profile',
            },
        ),
        migrations.AddField(
            model_name='candidatevideo',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.candidateprofile'),
        ),
        migrations.CreateModel(
            name='CandidateVideoReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('report_text', models.TextField(blank=True, max_length=2000, null=True)),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.candidatevideo')),
            ],
            options={
                'db_table': 'candidate_video_report',
                'unique_together': {('video', 'reported_by')},
            },
        ),
    ]