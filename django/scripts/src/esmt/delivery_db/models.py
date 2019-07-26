"""
This module takes care of defining the models for Delivery DB
"""
from django.db import models

class System(models.Model):
    """
    This Class defines the System model
    """
    system_id = models.AutoField(primary_key=True)
    system_name = models.CharField(max_length=255)
    system_short_name = models.CharField(max_length=50)
    creation_date = models.DateTimeField()

    class Meta:
        db_table = 'system'

    def __str__(self):
        return self.system_name


class SystemVersion(models.Model):
    """
    This class defined the System Version model
    """
    system_version_id = models.AutoField(primary_key=True)
    system_version_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    system_id = models.ForeignKey(System)

    class Meta:
        db_table = 'system_version'

    def __str__(self):
        return self.system_version_name
