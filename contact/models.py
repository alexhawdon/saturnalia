from django.db import models

class SaturnaliaContact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    title = models.CharField(max_length=30)
    description = models.TextField()
    display_order = models.IntegerField()
    picture = models.ImageField(upload_to='images/contacts', help_text="150x114")
    
    def __unicode__(self):
        return self.name +': ' + self.title
        
    def get_absolute_url(self):
        return "/contact/" + self.name.replace(' ', '-').lower() + '/'
    
    class Meta:
        ordering = ['display_order']
