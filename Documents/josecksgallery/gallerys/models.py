from django.db import models
import datetime as dt

class Category(models.Model):
    name = models.CharField(max_length = 60) 
    

    @classmethod
    def images(cls):
        galleries = cls.objects.all()
        return galleries  

    def __str__(self):
        return self.name

    def save_category(self):
        self.save()  

    def delete_category(self):
        self.delete()  

    @classmethod
    def display_categorys(cls):
        categorys = Category.objects.all()
        for category in categorys:
            return category      


class Location(models.Model):
    name = models.CharField(max_length = 60 )
    def __str__(self):
        return self.name
    
    @classmethod
    def today_gallerys(cls):
        location = cls.objects.filter(name = today)
        return location

    def save_location(self):
        self.save()  

    def delete_location(self):
        self.delete() 

    @classmethod
    def display_locations(cls):
        locations= Location.objects.all()
        for location in locations:
            return location        

class Image(models.Model):
    image_name = models.CharField(max_length =30)
    title = models.CharField(max_length=40)
    post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image_upload = models.ImageField(upload_to = 'images/' )
    category = models.ForeignKey(Category, null=True)
    location = models.ForeignKey(Location)
    
    @classmethod
    def search_by_category(cls,search_term):
        gallerys = cls.objects.filter(category__name__icontains=search_term).all()
        return gallerys

    @classmethod
    def search_by_category(cls,search_term):
        gallerys = cls.objects.filter(category__name__icontains=search_term).all()
        return gallerys

    def __str__(self):
        return self.title
    @classmethod
    def today_gallerys(cls):
        today = dt.date.today()
        galleries = cls.objects.filter(pub_date__date = today)
        return galleries

    def save_image(self):
        self.save() 

    def delete_image(self):
        self.delete() 

    @classmethod
    def display_images(cls):
        images= Image.objects.all()
        for image in images:
            return image        
    



      