# Generated by Django 5.1.1 on 2025-02-16 16:31

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_frontenduser_alter_category_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="APIConfig",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "service_name",
                    models.CharField(
                        choices=[
                            ("openai", "OpenAI API"),
                            ("google", "Google API"),
                            ("baidu", "Baidu API"),
                            ("deepseek", "DeepSeek API"),
                            ("custom", "自定义 API"),
                        ],
                        max_length=50,
                    ),
                ),
                ("api_key", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_used_at", models.DateTimeField(blank=True, null=True)),
                ("usage_count", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name="frontenduser",
            name="user_id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
