from importlib import import_module
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


class SiPMunit():
    """Class to represent a SiPM unit."""

    def __init__(self, model, custom_params = {}):
        if model == 'custom':
            self.check_custom_params(custom_params)
            self.build_custom_model(custom_params)
        else:
            self.get_model_file(model)
            self.get_model_geometry()
        self.set_dependant_properties()

    def get_model_file(self, model):
        from sipmarray.models import model_lib
        if model in model_lib.keys():
            self.model = model_lib[model]
        else:
            raise ValueError('Model not found. Please make a PR to add it.')

    def check_custom_params(self, custom_params):
        """Check if the custom_params dictionary have all the correct params.
        """
        params_list = ['name',
                       'width_package',
                       'height_package',
                       'width_tolerance',
                       'height_tolerance',
                       'width_active',
                       'height_active',
                       'active_area_correction',
                       'D_corner_x_active',
                       'D_corner_y_active',
                       'fill_factor',
                       'pde']
       
        params_missing = [
            param for param in params_list if param not in custom_params]
        if len(params_missing) > 0:
            raise ValueError('The custom_params dictionary must have all the '
                             'correct parameters.\nMissing parameters: '
                             f'{params_missing}')
            
    def build_custom_model(self,config_dict):
        """Build a custom model of the SiPM unit.

        Args:
            config_dict (dict): dictionary with the main properties of the
                SiPM unit.
        """

        self.name = config_dict['name']
        self.width_package = config_dict['width_package']
        self.height_package = config_dict['height_package']
        self.width_tolerance = config_dict['width_tolerance']
        self.height_tolerance = config_dict['height_tolerance']
        self.width_active = config_dict['width_active']
        self.height_active = config_dict['height_active']
        self.active_area_correction = config_dict['active_area_correction']
        self.D_corner_x_active = config_dict['D_corner_x_active']
        self.D_corner_y_active = config_dict['D_corner_y_active']
        self.fill_factor = config_dict['fill_factor']
        self.pde = config_dict['pde']


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
            self.fill_factor = _model.fill_factor
            self.pde = _model.pde

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
        self.active_area_fraction = self.active_area/self.total_area

    def get_unit_centre(self) -> Tuple[float, float]:
        """Get the centre of the SiPM unit

        Returns:
            tuple: (x,y) of the centre of the SiPM unit in SiPM unit 
                coordinates.
        """

        return (self.width_unit/2, self.height_unit/2)

    def get_unit_active_centre(self) -> Tuple[float, float]:
        """Get the centre of the active area of the SiPM unit

        Returns:
            tuple: (x,y) of the centre of the active area of the SiPM unit 
                in SiPM unit coordinates.
        """

        x = self.D_corner_x_active + self.width_active/2
        y = self.D_corner_y_active + self.height_active/2

        return (x, y)

    def plot_model(self, xy=(0, 0), figax=None):
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
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.add_patch(Rectangle((xy[0]+self.width_tolerance,
                                xy[1]+self.height_tolerance),
                               width=self.width_package,
                               height=self.height_package,
                               facecolor='gray',
                               alpha=0.3, edgecolor='k',
                               label='Packaging area', zorder=1))
        ax.add_patch(Rectangle((xy[0]+self.D_corner_x_active,
                                xy[1]+self.D_corner_y_active),
                               width=self.width_active,
                               height=self.height_active,
                               facecolor='k', alpha=0.8, edgecolor='k',
                               label='Active area', zorder=2))

        geometric_centre = self.get_unit_centre()
        active_centre = self.get_unit_active_centre()

        ax.plot(geometric_centre[0], geometric_centre[1], 'o',
                c='g', label='Geometric centre')
        ax.plot(active_centre[0], active_centre[1], 'x',
                c='r', label='Active centre')

        ax.set_xlim(xy[0]-0.1*self.width_unit, xy[0]+1.1*self.width_unit)
        ax.set_ylim(xy[1]-0.1*self.height_unit, xy[1]+1.1*self.height_unit)
        ax.set_aspect('equal')
        ax.legend()
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_aspect('equal')
        ax.grid(zorder=-10)

        if figax == None:
            plt.show()
        else:
            return fig, ax

    def get_unit_patches(self, xy: np.ndarray) -> list:
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
                       facecolor='gray',
                       alpha=0.3, edgecolor='k', zorder=3),
             Rectangle((xy[0]+self.D_corner_x_active,
                        xy[1]+self.D_corner_y_active),
                       width=self.width_active,
                       height=self.height_active,
                       facecolor='k', alpha=0.98,
                       edgecolor='k', zorder=4)
             ]
        return p

    def get_properties_str(self) -> str:
        """Return a string with the main properties of the SiPM model.
        """

        main_string = f'Model: {self.name}\n'
        main_string += f'--------------------------------------------\n'
        main_string += f'Width: {self.width_package} mm\n'
        main_string += f'Height: {self.height_package} mm\n'
        main_string += f'Active width: {self.width_active} mm\n'
        main_string += f'Active height: {self.height_active} mm\n'
        main_string += f'Width tolerance: {self.width_tolerance} mm\n'
        main_string += f'Height tolerance: {self.height_tolerance} mm\n'
        main_string += '--------------------------------------------\n'
        main_string += f'Total unit area: {round(self.total_area):.2f} mm^2\n'
        main_string += f'Active area geometric correction: {round(self.active_area_correction):.2f}\n'
        main_string += f'Active area: {round(self.active_area):.2f} mm^2\n'
        main_string += '--------------------------------------------\n'
        main_string += f'Active area fraction: {round(self.active_area_fraction)*100:.2f} %\n'
        main_string += f'Photon detection efficiency: {self.pde*100:.2f} %'

        return main_string

    def print_properties(self) -> None:
        """Print the main properties of the SiPM model
        """
        print(self.get_properties_str())

    def get_properties_df(self) -> pd.DataFrame:
        """Get the main properties of the SiPM model in a DataFrame

        Returns:
            pd.DataFrame: DataFrame of the main properties of the SiPM model
        """
        properties = {'Property': ['Model',
                                   'Width [mm]',
                                   'Height [mm]',
                                   'Active width [mm]',
                                   'Active height [mm]',
                                   'Width tolerance [mm]',
                                   'Height tolerance [mm]',
                                   'Total area [mm^2]',
                                   'Active area geometric correction',
                                   'Active area [mm^2]',
                                   'Active area fraction',
                                   'Photon detection efficiency'],

                      'Value': [self.name,
                                self.width_package,
                                self.height_package,
                                self.width_active,
                                self.height_active,
                                self.width_tolerance,
                                self.height_tolerance,
                                round(self.total_area, 2),
                                round(self.active_area_correction, 2),
                                round(self.active_area, 2),
                                round(self.active_area_fraction, 2),
                                self.pde]}
        return pd.DataFrame(properties)
