from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    # We need to create many-to-one relationship (single user can have many items, many users can be in a single app)
    # If a user is deleted, each child task has to be deleted (CASCADE), they are erased from database (null),
    # and user's form should be set to blank as well (blank).
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)  # Single line
    description = models.TextField(null=True, blank=True)  # Form (null & blank = True returns a text box)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # Query the 'complete' attribute from the Task class in the inner Meta class
        ordering = ['complete']


