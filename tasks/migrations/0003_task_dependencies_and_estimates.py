import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('tasks', '0002_task_status')]
    operations = [
        migrations.AddField(
            model_name='task', name='estimated_hours',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predecessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_dependencies', to='tasks.task')),
                ('successor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_dependencies', to='tasks.task')),
            ],
        ),
        migrations.AddField(
            model_name='task', name='predecessors',
            field=models.ManyToManyField(blank=True, related_name='successors', symmetrical=False, through='tasks.TaskDependency', through_fields=('successor', 'predecessor'), to='tasks.task'),
        ),
        migrations.AddConstraint(
            model_name='taskdependency',
            constraint=models.UniqueConstraint(fields=('predecessor', 'successor'), name='unique_task_dependency'),
        ),
    ]
