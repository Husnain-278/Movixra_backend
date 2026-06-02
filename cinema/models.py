from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from movies.models import Movie
# Create your models here.


class Cinema(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
     if not self.slug:  
        self.slug = slugify(self.name)
     super().save(*args, **kwargs)
        
        
class Screen(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='screens')
    name = models.CharField(max_length=255)
    image = CloudinaryField("screen_images")
    slug = models.SlugField(blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
     if not self.slug:  
        self.slug = slugify(f"{self.cinema.name}-{self.name}")
     super().save(*args, **kwargs)
    
    @property
    def capacity(self):
        return self.seats.filter(is_active=True).count()
    
    class Meta:
        unique_together = ('cinema', 'name')  # Ensure screen names are unique within a cinema
    
    def __str__(self):  
        return f"{self.cinema.name} - {self.name}"
    
class SeatType(models.Model):

    name = models.CharField(max_length=50)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name
    

class Seat(models.Model):
    
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE, related_name="seats")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('screen', 'row', 'number')  # Ensure seat numbers are unique within a screen
        ordering = ['row', 'number']  # Order seats by row and number
        indexes = [
        models.Index(fields=['screen', 'row']),
    ]
        
    def __str__(self):
        return f"{self.screen.name} - {self.row}{self.number}"
    
    
    
    
    
class Show(models.Model):

    FORMAT_CHOICES = (
        ("2D", "2D"),
        ("3D", "3D"),
        ("IMAX", "IMAX"),
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    format_type = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES
    )

    show_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def save(self, *args, **kwargs):
     if not self.slug:  
        self.slug = slugify(f"{self.movie.title}-{self.screen.name}-{self.start_time}")
     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

    
    

