class Building:
    def __init__(self, x, y, building_type, resources_needed):
        self.x = x
        self.y = y
        self.building_type = building_type
        self.resources_needed = resources_needed
        self.health = 100
        self.max_health = 100
