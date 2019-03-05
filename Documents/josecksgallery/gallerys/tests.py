from django.test import TestCase
from .models import Image,Location,Category

# Create your tests here.
class LocationTestClass(TestCase):

    def setUp(self):
        self.joseck=Location(name='ogachi')

    def test_instance(self):
        self.assertTrue(isinstance(self.joseck,Location))

    def test_save_method(self):
        self.joseck.save_location()
        locations = Location.objects.all()
        self.assertTrue(len(locations) > 0)

    def test_delete_method(self):
        self.joseck.save_location()
        self.joseck.delete_location()
        locations = Location.objects.all()
        self.assertTrue(len(locations) == 0)

    def test_display_locations_methods(self):
        self.joseck.save_location()
        self.joseck.display_locations()
        locations = Location.objects.all()
        self.assertTrue(len(locations) > 0)

class CategoryTestClass(TestCase):

    def setUp(self):
        self.joseck=Category(name="aurelia")

    def test_instance(self):
        self.assertTrue(isinstance(self.joseck,Category))

    def test_save_method(self):
        self.joseck.save_category()
        categorys = Category.objects.all()
        self.assertTrue(len(categorys) > 0)

    def test_delete_method(self):
        self.joseck.save_category()
        self.joseck.delete_category()
        categorys = Category.objects.all()
        self.assertTrue(len(categorys) == 0)

    def test_display_categorys_methods(self):
        self.joseck.save_category()
        self.joseck.display_categorys()
        categorys = Category.objects.all()
        self.assertTrue(len(categorys) > 0)

class ImageTestClass(TestCase):
    def setUp(self):
        self.joseck=Category(name="ogachi")
        self.joseck.save_category()

        self.new_location=Location(name="Dubai")
        self.new_location.save()

        self.new_image=Image(image_name="cubism",title="realism",location=self.new_location,category=self.joseck)
        self.new_image.save_image()

    def test_instance(self):
        self.assertFalse(isinstance(self.joseck,Image))

    def test_save_method(self):
        self.new_image.save_image()
        image = Image.objects.all()
        self.assertTrue(len(image) > 0)

    def test_delete_method(self):
        self.new_image.save_image()
        self.new_image.delete_image()
        image = Image.objects.all()
        self.assertTrue(len(image) == 0)

    def test_display_images_methods(self):
        self.new_image.save_image()
        self.new_image.display_images()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)

    def tearDown(self):
        Location.objects.all().delete()
        Category.objects.all().delete()
        Image.objects.all().delete()
