from django.db import models

from core.abstracts.models import CreatedModifiedAbstract


class Enterprise(CreatedModifiedAbstract):
    company_name = models.CharField(max_length=150, default='', unique=True)
    document = models.CharField(max_length=14, default='', unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

    class Meta:
        app_label = 'companies'


class Employee(CreatedModifiedAbstract):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Employee(user={self.user}, enterprise={self.enterprise})'

    class Meta:
        app_label = 'companies'


class TaskStatus(models.Model):
    name = models.CharField(max_length=155)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'companies'
        db_table = 'companies_task_status'


class Task(CreatedModifiedAbstract):
    title = models.TextField()
    description = models.TextField(null=True)
    due_date = models.DateTimeField(null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'companies'
