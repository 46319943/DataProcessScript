# encoding: utf-8
import arcpy
from arcpy.sa import *
import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists
import glob
import traceback
import pickle

from const_variables import poi_shp_folder_filepath, kde_temp_folder_filepath, ked_house_folder_filepath


def input_house(house_shp_folder_filepath):
    for csv_filepath in glob.glob(join(house_shp_folder_filepath, '*.shp')):
        kde_house(csv_filepath)


def kde_house(house_shp_filepath):
    house_shp_filename = splitext(basename(house_shp_filepath))[0]

    poi_shp_filepath = join(poi_shp_folder_filepath, house_shp_filename, 'AdvanComp.shp')

    raster = KernelDensity(poi_shp_filepath, None)
    ExtractValuesToPoints(house_shp_filepath, raster, join(ked_house_folder_filepath, basename(house_shp_filepath)))


if __name__ == "__main__":
    input_house(r'D:\Document\HousePricing\Data\House\RentSHP1')
