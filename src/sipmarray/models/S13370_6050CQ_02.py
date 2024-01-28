from sipmarray.unit import SiPMunit

class S13370_6050CQ_02(SiPMunit):
    """Class of the quad (12x12) VUV4 Hamamatsu SiPM unit.
    Ref: https://web.archive.org/web/20220401162036/https://hamamatsu.su/files/uploads/pdf/3_mppc/s13370_vuv4-mppc_b_(1).pdf
    """

    def __init__(self):
        self.name = 'S13370-6050CQ-02, "12x12", by Hamamatsu'
        self.width_package = 15.
        self.height_package = 15.
        self.width_tolerance = 0.2
        self.height_tolerance = 0.2
        self.width_active = 12 + 0.5
        self.height_active = 12 + 0.5

        # correction for the active area due to space between individual
        # 6x6 SiPMs
        self.active_area_correction = 12*12/(12.5*12.5)

        self.D_corner_x_active = ((self.width_package - 
                                    self.width_active)/2 + 
                                    self.width_tolerance)
        self.D_corner_y_active = ((self.height_package - 
                                    self.height_active)/2 + 
                                    self.height_tolerance)
        self.fill_factor = 0.6
        self.pde = 0.24
        self.set_dependant_properties()