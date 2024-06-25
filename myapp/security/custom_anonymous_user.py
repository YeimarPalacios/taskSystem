# Define tu clase de usuario anónimo personalizada
class CustomAnonymousUser:
    def __init__(self):
        self.username = 'Anonymous'
        self.is_authenticated = False
        self.is_active = False
        self.is_staff = False
        self.is_superuser = False

    def __str__(self):
        return self.username