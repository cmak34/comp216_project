class Settings:
    MAX_VAL = 50.0 
    MIN_VAL = -50.0
    BUFFER_SIZE = 100
    MISSING_CHANCE = 1
    CORRUPTED_CHANCE = 1

    @staticmethod
    def get_max_val():
        return Settings.MAX_VAL

    @staticmethod
    def get_min_val():
        return Settings.MIN_VAL

    @staticmethod
    def get_buffer_size():
        return Settings.BUFFER_SIZE
    
    @staticmethod
    def get_missing_chance():
        return Settings.MISSING_CHANCE

    @staticmethod
    def get_corrupted_chance():
        return Settings.CORRUPTED_CHANCE