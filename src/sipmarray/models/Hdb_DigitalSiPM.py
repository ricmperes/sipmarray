from sipmarray.unit import SiPMunit

class Hdb_DigitalSiPM(SiPMunit):
    """Class of the Digital SiPM from University of Heidelberg, group of 
    Prof. Peter Fischer.
    """
    def __init__(self):
        self.name = 'digital_sipm, from Peter Fischer (Uni. Heidelberg)'
        self.width_package = 65.218
        self.height_package = 75.606
        self.width_tolerance = 0.5
        self.height_tolerance = 0.5
        self.width_active = 65.218
        self.height_active = 75.606
        self.active_area_correction = 0.9065
        self.D_corner_x_active = ((self.width_package - 
                                    self.width_active)/2 + 
                                    self.width_tolerance)
        self.D_corner_y_active = ((self.height_package - 
                                    self.height_active)/2 + 
                                    self.height_tolerance)
        self.fill_factor = 0.776
        self.pde = self.fill_factor * 0.2

        self.set_dependant_properties()