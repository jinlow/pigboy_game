class Settings():
    """Class for all game settings."""

    def __init__(self):
        """Initialize game settings."""
        # Screen settings
        self.bg_color = (135, 206, 250)
        self.screen_width = 1200
        self.screen_height = 700
        self.fps = 60

        # Pigboy settings
        self.pig_walk_velocity = 6
        self.pig_jump_velocity = 8
        self.pig_mass = 3
        self.pig_jump_decay = 1
        self.pig_jump_cap = 8
        self.pig_run_factor = 3
        self.pg_start_height = 200

        # Platform #1 Settings
        self.p1_xloc  = 400
        self.p1_yloc = 500
        self.p1_imgw = 0
        self.p1_imgh = 0
        self.p1_img_path = 'platform_test.bmp'
        self.p1_w = 600
        self.p1_h = 100
        self.p1_color = (10, 100, 200)
