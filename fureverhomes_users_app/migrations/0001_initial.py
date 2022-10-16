# Generated by Django 4.1.2 on 2022-10-15 21:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import fureverhomes_users_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=30, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('user_name', models.CharField(max_length=50)),
                ('user_dob', models.DateField()),
                ('user_address', models.CharField(max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', fureverhomes_users_app.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PetProfile',
            fields=[
                ('pet_profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('pet_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('profile_pic', models.ImageField(upload_to='pet_profile_photos')),
                ('age', models.CharField(blank=True, choices=[(0, 'Young'), (1, 'Adult'), (2, 'Senior')], max_length=10)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('good_w_kids', models.BooleanField(default=False)),
                ('spayed_or_neutered', models.BooleanField(default=False)),
                ('rehoming_reason', models.CharField(max_length=200)),
                ('is_adopted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('petprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fureverhomes_users_app.petprofile')),
            ],
            bases=('fureverhomes_users_app.petprofile',),
        ),
        migrations.CreateModel(
            name='CurrentOwner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('fureverhomes_users_app.user',),
            managers=[
                ('objects', fureverhomes_users_app.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('petprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fureverhomes_users_app.petprofile')),
                ('breed', models.CharField(max_length=20)),
            ],
            bases=('fureverhomes_users_app.petprofile',),
        ),
        migrations.CreateModel(
            name='FutureOwner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('type_pref', models.TextField(choices=[('dog', 'Dog'), ('cat', 'Cat')], max_length=5)),
                ('sex_pref', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=3)),
                ('age_pref', models.IntegerField(choices=[(0, 'Young'), (1, 'Adult'), (2, 'Senior')])),
                ('other_preferences', models.IntegerField(choices=[('good_with_kids', 'Good with Kids'), ('spayed_neutered', 'Spayed or neutered?')])),
            ],
            options={
                'abstract': False,
            },
            bases=('fureverhomes_users_app.user',),
            managers=[
                ('objects', fureverhomes_users_app.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('fureverhomes_users_app.user',),
            managers=[
                ('objects', fureverhomes_users_app.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('message_content', models.CharField(max_length=1000)),
                ('receiver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_cause', models.IntegerField(choices=[(1, 'Threatening Language'), (2, 'Demand of Payment'), (3, 'Other')])),
                ('report_images', models.ImageField(blank=True, upload_to='report_photos')),
                ('user_reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported', to=settings.AUTH_USER_MODEL)),
                ('user_reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
                ('moderator_assigned', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fureverhomes_users_app.moderator')),
            ],
        ),
        migrations.AddField(
            model_name='petprofile',
            name='current_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fureverhomes_users_app.currentowner'),
        ),
        migrations.AddField(
            model_name='petprofile',
            name='interested_users',
            field=models.ManyToManyField(to='fureverhomes_users_app.futureowner'),
        ),
    ]
