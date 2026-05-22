from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):  
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    description = models.TextField()
    rating = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    trailer_url = models.URLField()
    poster = CloudinaryField('image')  
    release_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
     if not self.slug:
        base_slug = slugify(f"{self.title}-{self.release_date.year}")
        slug = base_slug
        counter = 1

        while Movie.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

     super().save(*args, **kwargs)
        

    

class Actor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    bio = models.TextField()
    birth_date = models.DateField()
    photo = CloudinaryField('image')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
      if not self.slug:
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        while Actor.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

      super().save(*args, **kwargs)
        
        

class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='casts')
    role_name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('movie', 'actor')
        
    def __str__(self):
        return f"{self.actor.name} as {self.role_name} in {self.movie.title}"
    