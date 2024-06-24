class CustomSessionInfo:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.session_info = {}
        return cls._instance

    def set_session_info(self, session_info):
        self.session_info = session_info

    def get_session_info(self):
        return self.session_info
