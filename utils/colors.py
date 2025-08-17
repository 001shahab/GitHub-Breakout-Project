"""
Color schemes for the game
"""

class Colors:
    # GitHub contribution colors (dark mode)
    CONTRIB_NONE = (22, 27, 34)      # #161b22
    CONTRIB_LOW = (14, 68, 41)       # #0e4429
    CONTRIB_MEDIUM = (0, 109, 50)    # #006d32
    CONTRIB_HIGH = (38, 166, 65)     # #26a641
    CONTRIB_MAX = (57, 211, 83)      # #39d353
    
    # Game colors (dark mode)
    BACKGROUND = (13, 17, 23)        # #0d1117
    PADDLE = (88, 166, 255)          # #58a6ff
    BALL = (255, 255, 255)           # #ffffff
    TEXT = (201, 209, 217)           # #c9d1d9
    TEXT_SECONDARY = (139, 148, 158) # #8b949e
    GRID_LINE = (48, 54, 61)         # #30363d
    
    @classmethod
    def update_theme(cls, dark_mode):
        """Update colors based on theme."""
        if dark_mode:
            # Dark mode (default)
            cls.CONTRIB_NONE = (22, 27, 34)
            cls.CONTRIB_LOW = (14, 68, 41)
            cls.CONTRIB_MEDIUM = (0, 109, 50)
            cls.CONTRIB_HIGH = (38, 166, 65)
            cls.CONTRIB_MAX = (57, 211, 83)
            
            cls.BACKGROUND = (13, 17, 23)
            cls.PADDLE = (88, 166, 255)
            cls.BALL = (255, 255, 255)
            cls.TEXT = (201, 209, 217)
            cls.TEXT_SECONDARY = (139, 148, 158)
            cls.GRID_LINE = (48, 54, 61)
        else:
            # Light mode
            cls.CONTRIB_NONE = (235, 237, 240)   # #ebedf0
            cls.CONTRIB_LOW = (155, 233, 168)    # #9be9a8
            cls.CONTRIB_MEDIUM = (64, 196, 99)   # #40c463
            cls.CONTRIB_HIGH = (48, 161, 78)     # #30a14e
            cls.CONTRIB_MAX = (33, 110, 57)      # #216e39
            
            cls.BACKGROUND = (255, 255, 255)
            cls.PADDLE = (36, 41, 47)
            cls.BALL = (36, 41, 47)
            cls.TEXT = (36, 41, 47)
            cls.TEXT_SECONDARY = (106, 115, 125)
            cls.GRID_LINE = (234, 236, 239)