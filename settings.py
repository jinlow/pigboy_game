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
        self.pig_walk_velocity = 10
        self.pig_jump_velocity = 50
        self.pig_mass = 2
        self.pig_jump_decay = 1
        self.pig_jump_cap = 8
        self.pig_run_factor = 3
        self.pg_start_height = 500

        # Platform #1 Settings
        self.p1_xloc  = 300
        self.p1_yloc = 500
        self.p1_imgw = 0
        self.p1_imgh = 0
        self.p1_img_path = 'platform_test.bmp'
        self.p1_w = 150
        self.p1_h = 50
        self.p1_color = (10, 100, 200)

        self.platform_list = [[400, 450, 150, 30],
                              [100, 300, 150, 30],
                              [800, 300, 150, 30],
                              [-600, self.screen_height-10, self.screen_width*10, 10]]
