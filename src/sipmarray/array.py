import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Rectangle

from sipmarray.unit import SiPMunit


class SiPMarray():
    """Class to represent a SiPM array.
    """
    def __init__(self, array_diameter: float = 150,
                 border_margin:float = -10, 
                 intra_sipm_distance: float = 0, 
                 sipm_model:str = 'quad',
                 custom_unit_params:dict = {}):
        """SiPMarray class

        Args:
            array_diameter (float): diameter of the array
            border_margin (float): margin between the sipms and the array border
            sipm_model (str): model of the sipm to use
        """
        
        self.array_diameter = array_diameter
        self.border_margin = border_margin
        self.intra_sipm_distance = intra_sipm_distance
        self.sipmunit = self.load_sipmunit(sipm_model, custom_unit_params)
        
        corner_meshes = self.make_corners()
        self.cut_outside_array(corner_meshes)
        self.n_sipms = self.A_corners_xx.count()

        self.total_array_area = np.pi * (self.array_diameter/2)**2
        self.total_sipm_area = self.n_sipms * self.sipmunit.total_area
        self.total_sipm_active_area = self.n_sipms * self.sipmunit.active_area
        self.sipm_coverage = self.total_sipm_active_area/self.total_array_area


    def make_corners(self) -> tuple:
        """Define where the corners of the sipms are

        Returns:
            tuple: (A_corner_xx, A_corner_yy, B_corner_xx, B_corner_yy, 
                    C_corner_xx, C_corner_yy, D_corner_xx, D_corner_yy)
        """
        half_intra_space = self.intra_sipm_distance/2

        # make the center a not
        D_corner_x = np.arange(
            0 + half_intra_space,
            self.array_diameter/2 + self.sipmunit.width_unit + self.intra_sipm_distance,
            self.sipmunit.width_unit + self.intra_sipm_distance)
        D_corner_y = np.arange(
            0 + half_intra_space, 
            self.array_diameter/2 +  self.sipmunit.height_unit + self.intra_sipm_distance, 
            self.sipmunit.height_unit + self.intra_sipm_distance)

        D_corner_x = np.concatenate(
            [-np.flip(D_corner_x) - self.sipmunit.width_unit,
             D_corner_x])
        D_corner_y = np.concatenate(
            [-np.flip(D_corner_y) - self.sipmunit.height_unit,
             D_corner_y])

        D_corner_xx, D_corner_yy = np.meshgrid(D_corner_x, D_corner_y, indexing = 'ij') 

        A_corner_xx = D_corner_xx
        A_corner_yy = B_corner_yy = D_corner_yy + self.sipmunit.height_unit

        B_corner_xx = C_corner_xx = D_corner_xx + self.sipmunit.width_unit
        C_corner_yy = D_corner_yy
        
        return (A_corner_xx, A_corner_yy, B_corner_xx, B_corner_yy, 
                C_corner_xx, C_corner_yy, D_corner_xx, D_corner_yy)
    
    def cut_outside_array(self, corner_meshes:tuple):
        """Mask the sipms that are outside the array in a masked array.

        Args:
            corner_meshes (tuple): tuple with all the corner meshes
        """        
        (A_corner_xx, A_corner_yy, B_corner_xx, B_corner_yy, 
                C_corner_xx, C_corner_yy, D_corner_xx, D_corner_yy) = corner_meshes
        D_corner_rr = np.sqrt(D_corner_xx**2 + D_corner_yy**2)

        A_corner_rr = np.sqrt(A_corner_xx**2 + A_corner_yy**2)
        B_corner_rr = np.sqrt(B_corner_xx**2 + B_corner_yy**2)
        C_corner_rr = np.sqrt(C_corner_xx**2 + C_corner_yy**2)
        
        A_mask_inside_array_rr = A_corner_rr < self.array_diameter/2 - self.border_margin
        B_mask_inside_array_rr = B_corner_rr < self.array_diameter/2 - self.border_margin
        C_mask_inside_array_rr = C_corner_rr < self.array_diameter/2 - self.border_margin
        D_mask_inside_array_rr = D_corner_rr < self.array_diameter/2 - self.border_margin
        
        merged_mask = (~A_mask_inside_array_rr | 
                       ~B_mask_inside_array_rr | 
                       ~C_mask_inside_array_rr | 
                       ~D_mask_inside_array_rr)
        
        self.D_corners_xx = np.ma.masked_array(D_corner_xx, mask= merged_mask)
        self.D_corners_yy = np.ma.masked_array(D_corner_yy, mask= merged_mask)

        self.A_corners_xx = np.ma.masked_array(A_corner_xx, mask= merged_mask)
        self.A_corners_yy = np.ma.masked_array(A_corner_yy, mask= merged_mask)

        self.B_corners_xx = np.ma.masked_array(B_corner_xx, mask= merged_mask)
        self.B_corners_yy = np.ma.masked_array(B_corner_yy, mask= merged_mask)

        self.C_corners_xx = np.ma.masked_array(C_corner_xx, mask= merged_mask)
        self.C_corners_yy = np.ma.masked_array(C_corner_yy, mask= merged_mask)
    
    def load_sipmunit(self, model: str,custom_unit_params:dict = {}):
        """Load the SiPM unit.

        Args:
            model (str): name of the SiPM model

        Returns:
            SiPMunit: a SiPM unit class object
        """
        return SiPMunit(model=model, custom_params=custom_unit_params)
    
    def get_centres(self, active_area: bool = True):
        """Get centres of the SiPMs.

        Args:
            active_area (bool, optional): Returns the centres of teh 
                active areas if true, otherwise the geometric centres of 
                the packaging if false. Defaults to True.
        Retuns:
            list: list of the centres of the SiPMs
        """
        if active_area:
            (x_sipm_centre, y_sipm_centre) = self.sipmunit.get_unit_active_centre()
        else:
            (x_sipm_centre, y_sipm_centre) = self.sipmunit.get_unit_centre()
        
        D_corners_x_flatten = self.D_corners_xx.flatten().compressed()
        D_corners_y_flatten = self.D_corners_yy.flatten().compressed()

        xs = D_corners_x_flatten + x_sipm_centre
        ys = D_corners_y_flatten + y_sipm_centre

        return np.vstack((xs, ys))
    
    def export_centres(self, file_name, active_area: bool = True) -> None:
        """Export the centres of the SiPMs to a file.

        Args:
            file_name (str): name of the file to write the centres into
        """
        centres = self.get_centres(active_area=active_area)
        np.savetxt(file_name, 
                   centres.T, 
                   header = 'x, y',
                   delimiter=", ", 
                   fmt='%.3f')
    
    def get_corners_active(self) -> np.ndarray:
        """Get all the positions of the corners of the active area of the SiPMs.

        Returns:
            np.ndarray: an array with the x and y coordinates of the 
                corners of the active area of the SiPMs
        """
        
        A_corner_x = (self.D_corners_xx.flatten().compressed() + 
                        self.sipmunit.D_corner_x_active)
        B_corner_x = (self.D_corners_xx.flatten().compressed() + 
                        self.sipmunit.D_corner_x_active +
                        self.sipmunit.width_active)
        C_corner_x = (self.D_corners_xx.flatten().compressed() + 
                        self.sipmunit.D_corner_x_active +
                        self.sipmunit.width_active)
        D_corner_x = (self.D_corners_xx.flatten().compressed() + 
                        self.sipmunit.D_corner_x_active)
        A_corner_y = (self.D_corners_yy.flatten().compressed() + 
                        self.sipmunit.D_corner_y_active + 
                        self.sipmunit.height_active)
        B_corner_y = (self.D_corners_yy.flatten().compressed() + 
                        self.sipmunit.D_corner_y_active + 
                        self.sipmunit.height_active)
        C_corner_y = (self.D_corners_yy.flatten().compressed() + 
                        self.sipmunit.D_corner_y_active)
        D_corner_y = (self.D_corners_yy.flatten().compressed() + 
                        self.sipmunit.D_corner_y_active)
        
        corners = np.vstack((A_corner_x, A_corner_y, B_corner_x, B_corner_y,
                             C_corner_x, C_corner_y, D_corner_x, D_corner_y))
        
        return corners
    
    def export_corners_active(self,file_name:str):
        """Export the corners of the active area of the SiPMs to a file.

        Args:
            file_name (str): name of the file to write the corners into
        """
        corners = self.get_corners_active()
        np.savetxt(file_name, corners.T, 
                       header = 'A_x, A_y, B_x, B_y, C_x, C_y, D_x, D_y', 
                       delimiter=', ',
                       fmt = '%.3f')


    def get_corners_package(self) -> np.ndarray:
        """Get all the positions of the corners of the total (includes 
        packaging) area of the SiPMs.

        Returns:
            np.ndarray: an array with the x and y coordinates of the 
                corners of the total area (including packaging) of the SiPMs
        """
        
        A_corner_x = (self.A_corners_xx.flatten().compressed() + 
                        self.sipmunit.width_tolerance)
        B_corner_x = (self.B_corners_xx.flatten().compressed() -
                        self.sipmunit.width_tolerance)
        C_corner_x = (self.C_corners_xx.flatten().compressed() -
                        self.sipmunit.width_tolerance)
        D_corner_x = (self.D_corners_xx.flatten().compressed() +
                        self.sipmunit.width_tolerance)
        A_corner_y = (self.A_corners_yy.flatten().compressed() -
                        self.sipmunit.height_tolerance)
        B_corner_y = (self.B_corners_yy.flatten().compressed() -
                        self.sipmunit.height_tolerance)
        C_corner_y = (self.C_corners_yy.flatten().compressed() +
                        self.sipmunit.height_tolerance)
        D_corner_y = (self.D_corners_yy.flatten().compressed() +
                        self.sipmunit.height_tolerance)
        
        corners = np.vstack((A_corner_x, A_corner_y, B_corner_x, B_corner_y,
                             C_corner_x, C_corner_y, D_corner_x, D_corner_y))

        return corners
    
    def export_corners_package(self,file_name:str):
        """Export the corners of the total area of the SiPMs to a file.

        Args:
            file_name (str): name of the file to write the corners into
        """
        corners = self.get_corners_package()
        np.savetxt(file_name, corners.T, 
                       header = 'A_x, A_y, B_x, B_y, C_x, C_y, D_x, D_y', 
                       delimiter=', ',
                       fmt = '%.3f')
    
    def plot_empty_array(self, unit_width: float, unit_height:float):
        """Plot simple division of the array circle in units.

        Args:
            unit_width (float): width of the unit
            unit_height (float): height of the unit
        """
               
        patches_sipms = []

        fig = plt.figure(figsize = (6,6))
        ax = plt.subplot(111)

        n_corner_x, n_corner_y = np.shape(self.D_corners_xx)

        for _x_i in range(n_corner_x):
            for _y_i in range(n_corner_y):
                patches_sipms.append(
                    Rectangle(xy = (self.D_corners_xx[_x_i,_y_i], 
                                    self.D_corners_yy[_x_i,_y_i]), 
                              width = unit_width, 
                              height = unit_height, 
                              fill = True,
                              edgecolor = 'k',
                              facecolor = 'b',
                              zorder = 0,
                              alpha = 0.2,)
                              )
        ax.add_patch(Circle(xy=(0,0),
                            radius = self.array_diameter/2, 
                            fill = False, 
                            color = 'r',
                            zorder = 0, 
                            label = 'Array diameter'))

        p1 = PatchCollection(patches_sipms, match_original=True, 
                             label = 'SiPM units 1')
        ax.add_collection(p1)
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_aspect('equal')

        ax.set_xlim(-self.array_diameter*1.2/2,self.array_diameter*1.2/2)
        ax.set_ylim(-self.array_diameter*1.2/2,self.array_diameter*1.2/2)

        # make patches for legend while it is not fixed in matplotlib
        ax.add_patch(Rectangle((1e6,1e6),1,1,fill = True,
                                         edgecolor = 'k',
                                         facecolor = 'b',
                                         alpha = 0.2,
                                         label = 'SiPM unit inside the array'))
        ax.legend()
        plt.show()
        
    def plot_sipm_array(self, figax:tuple = None):
        """Plot the array of SiPMs.

        Args:
            figax (tuple, optional): figure and axis objects to draw in. 
                Defaults to None.

        Returns:
            tuple: figure and axis objects
        """
        if figax is None:
            fig, ax = plt.subplots(figsize = (6,6))
        else:
            fig, ax = figax

        patches_sipms = []

        n_corner_x, n_corner_y = np.shape(self.D_corners_xx)

        for _x_i in range(n_corner_x):
            for _y_i in range(n_corner_y):
                patches_sipms += self.sipmunit.get_unit_patches(
                    (self.D_corners_xx[_x_i,_y_i], 
                     self.D_corners_yy[_x_i,_y_i]))
                
        ax.add_patch(Circle(xy=(0,0),
                            radius = self.array_diameter/2, 
                            fill = False, 
                            color = 'r',
                            zorder = 0, 
                            label = 'Array diameter'))

        p1 = PatchCollection(patches_sipms, match_original=True, 
                             label = 'SiPM units 1')
        ax.add_collection(p1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_aspect('equal')

        ax.set_xlim(-self.array_diameter*1.2/2,self.array_diameter*1.2/2)
        ax.set_ylim(-self.array_diameter*1.2/2,self.array_diameter*1.2/2)

        ax.legend()

        if figax is None:
            plt.show()
        else:
            return fig, ax
    
    def print_properties(self, unit_properties = False):
        """Prints the main properties of the array object.

        Args:
            unit_properties (bool, optional): _description_. Defaults to False.
        """
        print(f'Array diameter: {self.array_diameter} mm')
        print(f'Margin from the array edge: {self.border_margin} mm')
        print(f'Number of units: {self.n_sipms}')
        print(f'Total array area: {self.total_array_area:.2f} mm^2')
        print(f'Total photosensor area: {self.total_sipm_area:.2f} mm^2')
        print(f'Total SiPM active area: {self.total_sipm_active_area:.2f} mm^2')
        print(f'SiPM coverage: {self.sipm_coverage:.2f}')

        if unit_properties:
            self.sipmunit.print_properties()
           