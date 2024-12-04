

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GraphSetup(metaclass=Singleton):

    def __init__(self):
        self.response_time_unit = "sec"
        # self.response_time_line = False
        # self.use_std = True

