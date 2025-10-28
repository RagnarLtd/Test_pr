from django.db import models
from passlib.hash import bcrypt

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw: str):
        self.password_hash = bcrypt.hash(raw)


    def check_password(self, raw: str) -> bool:
        try:
            return bcrypt.verify(raw, self.password_hash)
        except Exception:
            return False


    def __str__(self):
        return self.email


    @property
    def is_authenticated(self) -> bool:
        return True


    @property
    def is_anonymous(self) -> bool:
        return False