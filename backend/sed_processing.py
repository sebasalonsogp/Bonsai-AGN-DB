#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
import csv
from io import StringIO
import os

def process_sed_data(data_file, output_file):
    try:
        print(f"Processing SED data from {data_file}")  # Debug print
        print(f"Output will be saved to {output_file}")  # Debug print
        
        # Read the data
        with open(data_file, 'r') as f:
            content = f.read().strip()
        print(f"Raw content: {content}")  # Debug print
        
        # Split the content into individual data points
        data_points = content.split()
        print(f"Number of data points: {len(data_points)}")  # Debug print
        print(f"Data points: {data_points}")  # Debug print
        
        wavelengths = []
        fluxes = []
        
        for point in data_points:
            try:
                # Split each point by comma
                parts = point.split(',')
                print(f"Processing point: {point}")  # Debug print
                print(f"Split parts: {parts}")  # Debug print
                
                if len(parts) >= 2:
                    wavelength = float(parts[0])
                    flux = float(parts[1])
                    
                    wavelengths.append(wavelength)
                    fluxes.append(flux)
                    print(f"Successfully processed point: {point}")  # Debug print
                else:
                    print(f"Invalid point format: {point}")  # Debug print
            except ValueError as e:
                print(f"Error processing point {point}: {str(e)}")  # Debug print
                continue
        
        if not wavelengths:
            print("Error: No valid data points found")
            return False
        
        print(f"Successfully processed {len(wavelengths)} data points")  # Debug print
        
        # Convert to numpy arrays
        wavelength = np.array(wavelengths)
        flux = np.array(fluxes)
        
        print(f"Wavelength range: {min(wavelength)} - {max(wavelength)}")  # Debug print
        print(f"Flux range: {min(flux)} - {max(flux)}")  # Debug print
        
        try:
            # Create the plot
            print("Creating plot...")  # Debug print
            plt.figure(figsize=(10, 6))
            
            # Create the basic plot
            plt.plot(wavelength, flux, 'o-', label='Data points')
            
            # Set axis labels and title
            plt.xlabel('Wavelength (Å)')
            plt.ylabel('Flux (arbitrary units)')
            plt.title('Spectral Energy Distribution (SED)')
            
            # Set log scale for both axes if all values are positive
            if np.all(wavelength > 0) and np.all(flux > 0):
                plt.xscale('log')
                plt.yscale('log')
            
            # Add grid and legend
            plt.grid(True, which="both", ls="-", alpha=0.2)
            plt.legend()
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                print(f"Creating output directory: {output_dir}")  # Debug print
                os.makedirs(output_dir, exist_ok=True)
            
            # Save the plot
            print(f"Saving plot to {output_file}")  # Debug print
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Verify file was created
            if os.path.exists(output_file):
                print(f"Plot saved successfully to {output_file}")  # Debug print
                return True
            else:
                print(f"Error: Plot file was not created at {output_file}")  # Debug print
                return False
                
        except Exception as plot_error:
            print(f"Error creating/saving plot: {str(plot_error)}")  # Debug print
            import traceback
            print(f"Plot error traceback: {traceback.format_exc()}")  # Debug print
            return False
        
    except Exception as e:
        print(f"Error in process_sed_data: {str(e)}")  # Debug print
        import traceback
        print(f"Traceback: {traceback.format_exc()}")  # Debug print
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process SED data and create a plot')
    parser.add_argument('--data_file', required=True, help='Input data file')
    parser.add_argument('--output_file', required=True, help='Output plot file')
    
    args = parser.parse_args()
    
    success = process_sed_data(args.data_file, args.output_file)
    sys.exit(0 if success else 1)
