from django.db import models
from django.contrib.admin.models import User
from applications.models import Application


# Create your models here.
class AccessToken(models.Model):
    user = models.ForeignKey(User)
    application = models.ForeignKey(Application)
    accessToken = models.CharField(max_length=32)
    accessSecret = models.CharField(max_length=32)
    created_date = models.DateTimeField(auto_now_add=True)
    validate_status = models.IntegerField()
    is_enable = models.IntegerField()

    def __unicode__(self):
        return 'access token %s %s %s ' % (self.name,self.application,self.accessToken)
