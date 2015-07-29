from django.db import models

class Newsletter(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.name
