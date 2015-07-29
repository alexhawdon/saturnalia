from django.db import models

class NewsCategory(models.Model):
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/news/tag/" + self.name.lower().replace(' ', '-') + "/"
    
    class Meta:
        ordering = ['name']

class NewsItem(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=60)
    text = models.TextField()
    image = models.ImageField(blank=True, upload_to="news_images/", help_text="310x236")
    category = models.ManyToManyField(NewsCategory)
    
    def get_absolute_url(self):
        return "/news/view/" + str(self.id) + "/"
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-date', '-id']
