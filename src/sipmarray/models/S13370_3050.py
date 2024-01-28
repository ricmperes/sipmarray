from sipmarray.unit import SiPMunit

class S13370_3050(SiPMunit):
    """Class of the 3x3 VUV4 Hamamatsu SiPM unit.
    Ref: https://web.archive.org/web/20220401162036/https://hamamatsu.su/files/uploads/pdf/3_mppc/s13370_vuv4-mppc_b_(1).pdf
    """
    
    def __init__(self):
        self.name = 'S13370-3050, "3x3", by Hamamatsu'
        self.width_package = 5.9
        self.height_package = 6.55
        self.width_tolerance = 0.15
        self.height_tolerance = 0.15
        self.width_active = 3
        self.height_active = 3
        self.active_area_correction = 1.
        self.D_corner_x_active = ((self.width_package - 
                                    self.width_active)/2 
                                    + self.width_tolerance)
        self.D_corner_y_active = ((self.height_package - 
                                    self.height_active)/2 -0.33 + 
                                    self.height_tolerance)
        self.fill_factor = 0.6
        self.pde = 0.24
        self.set_dependant_properties()