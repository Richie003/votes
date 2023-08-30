from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:  # Check if the input looks like an email
                user = User.objects.get(email=username, admin=True)
            else:
                user = User.objects.get(reg_no=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
