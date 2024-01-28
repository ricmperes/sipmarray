from sipmarray.unit import SiPMunit

class UZH_Tile(SiPMunit):
    """Class of the tile of VUV4 quads designed at UZH.
    Ref: DOI 10.1088/1748-0221/18/03/C03027
    """
    
    def __init__(self):
        self.name = 'UZH Tile'
        self.width_package = 34.
        self.height_package = 34.
        self.width_tolerance = 1.
        self.height_tolerance = 1.

        # All the interior area is considered active an then corrected
        # This means 15 + 2.38 + 15 = 32.38 mm of side length
        self.width_active = 32.38
        self.height_active = 32.38

        # Correction is a composite of three parameters:
        #   - the space between SiPMs in the quads - 12*12/(12.5*12.5)
        #   - the fraction of active area inside the quad packaging, 0.61
        #   - the space between quads, self.width_package**2 - (15+15)**2
        self.active_area_correction = ((12*12/(12.5*12.5)) * 
                                       0.61 * 
                                       (15+15)**2/(self.width_package**2))
        
        self.D_corner_x_active = ((self.width_package - 
                                    self.width_active)/2 + 
                                    0.85)
        self.D_corner_y_active = ((self.height_package - 
                                    self.height_active)/2 + 
                                    0.85)
        self.fill_factor = 0.6
        self.pde = 0.24
        self.set_dependant_properties()