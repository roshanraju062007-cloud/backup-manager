from django.db import models
from django.contrib.auth.models import User


# Profile table to store per-user metadata (second table in schema)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    storage_used = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Profile({self.user.username})"


# File table: stores metadata and the file path via a FileField
class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=512)
    file = models.FileField(upload_to='uploads/')
    size = models.BigIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            try:
                self.size = self.file.size
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"File({self.name})"
