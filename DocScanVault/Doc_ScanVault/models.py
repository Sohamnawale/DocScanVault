from django.db import models

class User(models.Model):
    """
    Represents a user in the system.
    """
    User_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    Username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)  # Use EmailField for email validation
    Passwords = models.CharField(max_length=256)  # Store hashed passwords, not plain text!
    role = models.CharField(max_length=20, choices=[  # Assuming role is a string with limited options
        ('admin', 'Admin'),
        ('user', 'User'),
        # Add more roles as needed
    ])
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    last_login = models.DateTimeField(null=True, blank=True)  # Allow null if user hasn't logged in yet



    def __str__(self):
        return self.Username
    


# Create your models here.
