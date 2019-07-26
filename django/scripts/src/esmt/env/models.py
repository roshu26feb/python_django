"""
Author: Yogaraja Gopal
This module contains the model for env app
"""
from django.db import models


class ServiceGroup(models.Model):
    """
    This Class contains the Service Group Model
    """
    client_name = models.CharField(max_length=50)
    region = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.region + "|" + self.client_name


class Server(models.Model):
    """
    This Class contains the Server Model
    """
    server_ip = models.GenericIPAddressField(unique=True)
    env_type = models.CharField(max_length=50)
    app = models.CharField(max_length=50)
    sub_app = models.CharField(max_length=50)
    service_group = models.ForeignKey(ServiceGroup)
    store_server = models.ForeignKey("self", null=True, default=None, blank=True)

    def __str__(self):
        return self.server_ip


class Services(models.Model):
    """
    This Class contains the Services Model
    """
    service_group = models.ForeignKey(ServiceGroup)
    service_name = models.CharField(max_length=50)
    alias_name = models.CharField(max_length=50)

    def __str__(self):
        return self.service_group.region + "|" + self.service_group.client_name + "|" +\
               self.service_name


class ServiceInstance(models.Model):
    """
    This Class contains the Service Instance Model
    """
    server_id = models.ForeignKey(Server)
    service_name = models.ForeignKey(Services)
    service_status = models.CharField(max_length=20)

    def __str__(self):
        return self.server_id.server_ip + "|" + self.service_name.service_name + "|" +\
               self.service_status


class RundeckJobEntry(models.Model):
    """
    This Class contains the  Rundeck Job Entry Model
    """
    server_id = models.ForeignKey(Server)
    job_name = models.CharField(max_length=50)
    job_execution_id = models.BigIntegerField()
    executed_datetime = models.DateTimeField()

    def __str__(self):
        return self.server_id.server_ip + " | " + self.job_name


class MountTimeStamp(models.Model):
    """
    This Class contains Mount Time Stamp Model
    """
    server_id = models.ForeignKey(Server)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.server_id.server_ip + " | " + self.timestamp.strftime('%Y/%m/%d %H:%M:%S')


class Mount(models.Model):
    """
    This Class contains the Mount Model
    """
    mount_ts = models.ForeignKey(MountTimeStamp)
    filesystem = models.CharField(max_length=255)
    size = models.CharField(max_length=30)
    used = models.CharField(max_length=30)
    avail = models.CharField(max_length=30)
    used_percent = models.CharField(max_length=30)
    mounted_on = models.CharField(max_length=255)

    def __str__(self):
        return self.mount_ts.server_id.server_ip + " : " + "Mount"


class FactsTimeStamp(models.Model):
    """
    This Class contains the Fact Time stamp Model
    """
    server_id = models.ForeignKey(Server)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.server_id.server_ip + " | " + self.timestamp.strftime('%Y/%m/%d %H:%M:%S')


class Facts(models.Model):
    """
    This Class contains the Facts Model
    """
    server_id = models.ForeignKey(Server)
    fact_name = models.CharField(max_length=100)
    fact_value = models.CharField(max_length=100)

    def __str__(self):
        return self.server_id.server_ip + " : " + self.fact_name
