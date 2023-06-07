#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt

from sipmarray import SiPMarray


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Script to quickly get a SiPM array plot or geometry.'))

    parser.add_argument('-m', '--model',
                        help='Define the SiPM model.',
                        default= '6x6',
                        type = str,
                        required=True)
    parser.add_argument('-d', '--diameter',
                        help='Define the SiPM array diameter in mm.',
                        required= True,
                        type= float)
    parser.add_argument('-b', '--border',
                        help='Define the SiPM array border margin in mm.',
                        required= False,
                        type= float,
                        default= 0)
    parser.add_argument('-p', '--plot',
                        help='Plot the SiPM array.',
                        type= bool,
                        default= False,
                        required=False)
    parser.add_argument('-o', '--output',
                        help ='Output the SiPM array geometry to a file.',
                        type = bool,
                        default = True,
                        required=False)
    parser.add_argument('-v', '--verbose',
                        help ='Print the SiPM array properties in the terminal.',
                        type = bool,
                        default = False,
                        required=False)
    args = parser.parse_args()

    model = args.model
    diameter = args.diameter
    border = args.border
    plot = args.plot
    output = args.output
    verbose = args.verbose
    return model,diameter,border,plot,output,verbose

def make_plot(model, diameter, array):
    fig, ax = plt.subplots(1,1)
    fig, ax = array.plot_sipm_array(figax= (fig,ax))
    fig.savefig(f'sipmarray_{model}_{diameter}mm.png')

def make_output(model, diameter, array):
    array.export_corners_active(
            file_name = f'sipmarray_corners_active_{model}_{diameter}mm.csv')
    array.export_corners_package(
            file_name = f'sipmarray_corners_package_{model}_{diameter}mm.csv')
    array.export_centres(
            file_name = f'sipmarray_centres_{model}_{diameter}mm.csv')

def main():
    model, diameter, border, plot, output, verbose = parse_args()
    if verbose: print('Building SiPM array.')

    array = SiPMarray(array_diameter = diameter, 
                      border_margin = border, 
                      sipm_model = model)
    
    if verbose: array.print_properties(unit_properties=True)
    if plot: make_plot(model, diameter, array)
    if output: make_output(model, diameter, array)
    if verbose: print('Done!')

if __name__ == '__main__':
    main()


