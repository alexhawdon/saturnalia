from django.db import models

ACT_TYPES=(('BA', 'Band/Solo Artist'),
           ('PA', 'Electronic Live PA'),
           ('DJ', 'DJ Set'))
           
ARENAS=(('PA', 'Pandora'),
        ('TI', 'Titan'),
        ('AC', 'Accoustic Stage'))

class Artist(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="artists/", help_text="310x236", blank=True)
    thumbnail = models.ImageField(upload_to="artists/", help_text="150x114", blank=True)
    description = models.TextField()
    performance_detail = models.CharField(max_length=10, blank=True)
    act_type = models.CharField(max_length=2, choices=ACT_TYPES, blank=True)
    display = models.BooleanField(default=False, verbose_name="Display on website")
    tbc = models.BooleanField(default=True)
    promotion_priority = models.IntegerField(help_text="1-9, 1 is highest.", default=9)
    arena = models.CharField(max_length=2, choices=ARENAS, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    lastfm = models.URLField(blank=True)
    soundcloud = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    myspace = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    resident_advisor = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/artists/" + self.name.replace(' ', '-') + "/"

class ArtistDetailLine(models.Model):
    line = models.CharField(max_length=40, blank=True)
    line_number = models.IntegerField()
    artist = models.ForeignKey(Artist)
