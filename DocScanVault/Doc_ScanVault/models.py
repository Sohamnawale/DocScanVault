from django.db import models

class User(models.Model):
    """
    Represents a user in the system.
    """
    User_id = models.AutoField(primary_key=True)  #autoincrement
    Username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)  
    Passwords = models.CharField(max_length=256)  
    role = models.CharField(max_length=20, choices=[ 
        ('admin', 'Admin'),
        ('user', 'User'),
        
    ])
    created_at = models.DateTimeField(auto_now_add=True)  
    last_login = models.DateTimeField(null=True, blank=True)  



    def __str__(self):
        return self.Username


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    file_path = models.CharField(max_length=100)
    file_size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    content_hash = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    class Meta:
        app_label = 'Doc_ScanVault'

class Log(models.Model):
    
    class ActivityType(models.TextChoices):
        LOGIN = 'LOGIN', 'Login'
        LOGOUT = 'LOGOUT', 'Logout'
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'
        
    
    log_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
    )
    description = models.TextField()
    ip_address = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Log #{self.log_id} - {self.activity_type} by User {self.user_id}"   
    class Meta:
        app_label = 'Doc_ScanVault'

class CreditRequest(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        
    
    request_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField() 
    amount = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.IntegerField(null=True, blank=True)  
    
    def __str__(self):
        return f"Credit Request #{self.request_id} - {self.amount} by User {self.user_id}"
    class Meta:
        app_label = 'Doc_ScanVault'

class Credit(models.Model):
    user_id = models.IntegerField(primary_key=True) 
    balance = models.IntegerField()
    last_reset_date = models.DateTimeField()
    
    def __str__(self):
        return f"User #{self.user_id} - Balance: {self.balance}"
    class Meta:
        app_label = 'Doc_ScanVault'
    
class ScanTransaction(models.Model):
    scan_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()  
    document_id = models.IntegerField()  
    scan_date = models.DateTimeField()
    credits_used = models.IntegerField()
    
    def __str__(self):
        return f"Scan #{self.scan_id} - User: {self.user_id}, Document: {self.document_id}"
    class Meta:
        app_label = 'Doc_ScanVault'
    
class DocumentMatch(models.Model):
    match_id = models.AutoField(primary_key=True)
    scan_id = models.IntegerField()  # Foreign key to scan_transaction table
    source_document_id = models.IntegerField()  
    matched_document_id = models.IntegerField()  
    similarity_score = models.FloatField()
    match_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Match #{self.match_id} - Score: {self.similarity_score}"
    class Meta:
        app_label = 'Doc_ScanVault'

class DocumentMetadata(models.Model):
    metadata_id = models.AutoField(primary_key=True)
    document_id = models.IntegerField()  
    key = models.CharField(max_length=50)
    value = models.TextField()
    
    def __str__(self):
        return f"{self.key}: {self.value[:30]}{'...' if len(self.value) > 30 else ''}"
    class Meta:
        app_label = 'Doc_ScanVault'

# Create your models here.
