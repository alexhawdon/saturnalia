from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=40)
    display_order = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/faq/section/#" + self.name.replace(' ', '-')
    
    def get_id(self):
        return self.name.replace(' ', '-')
    
    class Meta:
        ordering = ['-display_order']

class QAPair(models.Model):
    shortname = models.CharField(max_length=30, unique=True)
    question = models.TextField()
    answer = models.TextField()
    section = models.ForeignKey(Section)
    
    def __unicode__(self):
        return self.question
    
    def get_absolute_url(self):
        return "/faq/question/#" + self.shortname.replace(' ', '-')
    
    def get_id(self):
        return self.shortname.replace(' ', ' ')

