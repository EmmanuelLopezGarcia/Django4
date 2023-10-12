from django.db import models
from django.db.models.query import QuerySet
# Timezone for dates and time
from django.utils import timezone
# Adding the Django authentication framework
from django.contrib.auth.models import User

# The reverse function will build the URL dynamically using the URL name defined
# in the URL pattern.
from django.urls import reverse

# Creating a model manager like "object" but mine to chose all published posts.

class PublishedManager(models.Manager):

    def get_queryset(self):

        return super().get_queryset().filter(status = Post.Status.PUBLISHED)
    

# Create your models here.

# Post model that will allow us to store blog posts in the database

class Post(models.Model):

    # Adding a status field that will tell the post' status (Published or Draft)
    # This is an enumeration class by subclassing models.TextChoices
    class Status(models.TextChoices):

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB' , 'Published'
    
    # Attributes
    title = models.CharField(max_length = 250)
    
    # A slug is a short label that contains only letters, numbers, underscores, or hyphens.
    #   
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')

    # This field defines a many-to-one relationship, meaning that each post is written by a user,
    # and a user can write any number of posts. For this field, Django will create a foreign key
    # in the database using the primary key of the related model.
    # We use related_name to specify the name of the reverse relationship, from User to Post.
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')

    body = models.TextField()

    publish = models.DateTimeField(default = timezone.now)

    created = models.DateTimeField(auto_now_add = True)

    updated = models.DateTimeField(auto_now = True)

    status = models.CharField(max_length = 2, choices = Status.choices, default = Status.DRAFT)

    # The default manager
    objects = models.Manager()

    # My custom manager
    published = PublishedManager()

    # This class defines metadata for the model.
    class Meta:
        # This ordering will apply by default for database queries when no specific order is
        # provided in the query. 
        # The hyphen indicates descending order, posts will be returned in reverse 
        # chronological order by default.
        ordering = ['-publish']

        indexes = [

            models.Index(fields = ['-publish'])

        ]
    # This is the default Python method to return a string with the human-readable representation
    # of the object.
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        # This URL has a required parameter that is the id of the blog post to retrieve.
        # We have included the id of the Post oject as a positional argument by using args=[self.id]
        return reverse('blog:post_detail', args = [self.publish.year, self.publish.month, self.publish.day, self.slug])
    
