from importlib import import_module
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class SiPMunit():
    """Class to represent a SiPM unit."""

    def __init__(self, model):
        self.get_model_file(model)
        self.get_model_geometry()
        self.set_dependant_properties()

    def get_model_file(self, model):
        from sipmarray.models import model_lib
        if model in model_lib.keys():
            self.model = model_lib[model]
        else:
            raise ValueError('Model not found. Please make a PR to add it.')
        
    def get_model_geometry(self):
        """Loads model geometric properties from the model file.

        Raises:
            ModuleNotFoundError: raised if the model file is not found.
        """
        try:
            model_module = import_module(f'sipmarray.models.{self.model}')
            model_class = getattr(model_module, self.model)
            _model = model_class()

            self.name = _model.name
            self.width_package = _model.width_package
            self.height_package = _model.height_package
            self.width_tolerance = _model.width_tolerance
            self.height_tolerance = _model.height_tolerance
            self.width_active = _model.width_active
            self.height_active = _model.height_active
            self.active_area_correction = _model.active_area_correction
            self.D_corner_x_active = _model.D_corner_x_active
            self.D_corner_y_active = _model.D_corner_y_active

            self.set_dependant_properties()

        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                'Model not found. Please make a PR to add it.')
    
    def set_dependant_properties(self):
        """Defines dependant properties of the SiPM unit: total area, active
        area and active area fraction.
        """
        self.width_unit = self.width_package + 2*self.width_tolerance
        self.height_unit = self.height_package + 2*self.height_tolerance
        self.total_area = self.width_unit*self.height_unit
        self.active_area = (self.width_active *
                            self.height_active *
                            self.active_area_correction)
            
    def get_unit_centre(self)->Tuple[float, float]:
        """Get the centre of the SiPM unit

        Returns:
            tuple: (x,y) of the centre of the SiPM unit in SiPM unit 
                coordinates.
        """

        return (self.width_unit/2, self.height_unit/2)
    
    def get_unit_active_centre(self)->Tuple[float, float]:
        """Get the centre of the active area of the SiPM unit

        Returns:
            tuple: (x,y) of the centre of the active area of the SiPM unit 
                in SiPM unit coordinates.
        """

        x = self.D_corner_x_active + self.width_active/2
        y = self.D_corner_y_active + self.height_active/2

        return (x,y)
    
    def plot_model(self, xy = (0,0), figax = None):
        """Make a plot of the SiPM unit model

        Args:
            xy (tuple, optional): coordinates of the bottom left corner. 
                Defaults to (0,0).
            figax (_type_, optional): figure and axis environment. 
                Defaults to None.

        Returns:
            _type_: updated figure and axis environment
        """
        if figax == None:
            fig, ax = plt.subplots(1,1,figsize = (5,5))
        ax.add_patch(Rectangle((xy[0]+self.width_tolerance, 
                                xy[1]+self.height_tolerance), 
                   width=self.width_package,
                   height=self.height_package,
                   facecolor = 'gray',
                   alpha = 0.3, edgecolor = 'k',
                   label = 'Packaging area', zorder = 1))
        ax.add_patch(Rectangle((xy[0]+self.D_corner_x_active,
                                xy[1]+self.D_corner_y_active), 
                               width=self.width_active, 
                               height=self.height_active, 
                               facecolor = 'k', alpha = 0.8, edgecolor = 'k',
                              label = 'Active area', zorder = 2))
        
        geometric_centre = self.get_unit_centre()
        active_centre = self.get_unit_active_centre()

        ax.plot(geometric_centre[0], geometric_centre[1], 'o', 
                c = 'g', label = 'Geometric centre')
        ax.plot(active_centre[0], active_centre[1], 'x',
                c = 'r', label = 'Active centre')
        
        ax.set_xlim(xy[0]-0.1*self.width_unit, xy[0]+1.1*self.width_unit)
        ax.set_ylim(xy[1]-0.1*self.height_unit, xy[1]+1.1*self.height_unit)
        ax.set_aspect('equal')
        ax.legend()
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_aspect('equal')
        ax.grid(zorder = -10)
        
        if figax == None:
            plt.show()
        else:
            return fig, ax
    
    def get_unit_patches(self,xy:np.ndarray) -> list:
        """Get the patches of the SiPM unit for plotting.

        Args:
            xy (np.ndarray): the coordinates of the bottom left corner of
                the SiPM unit.

        Returns:
            list: list of patches of the SiPM units
        """
        p = [Rectangle((xy[0]+self.width_tolerance, 
                        xy[1]+self.height_tolerance), 
                       width=self.width_package,
                       height=self.height_package,
                       facecolor = 'gray',
                       alpha = 0.3, edgecolor = 'k', zorder = 3),
             Rectangle((xy[0]+self.D_corner_x_active,
                        xy[1]+self.D_corner_y_active), 
                       width=self.width_active, 
                       height=self.height_active, 
                       facecolor = 'k', alpha = 0.98, 
                       edgecolor = 'k', zorder = 4)
            ]
        return p
    
    def print_properties(self) -> None:
        """Print the main properties of the SiPM model
        """
        
        print(f'Model: {self.name}')
        print(f'Total unit area: {self.total_area:.2f} mm^2')
        print(f'Active area geometric correction: '
              f'{self.active_area_correction:.2f}')
        print(f'Active area: {self.active_area:.2f} mm^2')
        print(f'Active area fraction: '
              f'{self.active_area/self.total_area:.2f}')
        print(f'Width tolerance: {self.width_tolerance} mm')
        print(f'Height tolerance: {self.height_tolerance} mm')
