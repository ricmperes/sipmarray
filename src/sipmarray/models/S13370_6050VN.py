from sipmarray.unit import SiPMunit

class S13370_6050VN(SiPMunit):
    """Class of the 6x6 low dead space VUV4 Hamamatsu SiPM unit.
    Ref: 
    """
    
    def __init__(self):
        self.name = 'S13370_6050VN, "6x6" low dead space, by Hamamatsu'
        self.width_package = 6.4
        self.height_package = 6.4
        self.width_tolerance = 0
        self.height_tolerance = 0
        self.width_active = 6
        self.height_active = 6
        self.active_area_correction = 1.
        self.D_corner_x_active = ((self.width_package - 
                                    self.width_active)/2 + 
                                    self.width_tolerance)
        self.D_corner_y_active = ((self.height_package - 
                                    self.height_active)/2 + 
                                    self.height_tolerance)
        self.fill_factor = 0.996
        self.pde = 0.20
        self.set_dependant_properties()