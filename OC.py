#Author: Xiaoxuan Li
#Date: 2020/11/16
import pandas as pd
import numpy as np
import arcpy
from arcpy.sa import *
import os
import shutil
from datetime import date

#setup
YEAR = 2007
ws = r"E:\seadas\rui/"
ori_dir = ws + r"point\ori/" + str(YEAR) + "/"
csv_dir = ws + r"point\processed/" + str(YEAR) + "/"
nc_dir = ws + r"result\nc/" + str(YEAR) + "/"
tif_dir = ws + r"result\tif\reprojection/" + str(YEAR) + "/"
shp_dir = ws + r"result\shp/" + str(YEAR) + "/"
mosaic_dir = ws + r"result\tif\mosaic/" + str(YEAR) + "/"
result_dir = ws + r"result\result_csv/" + str(YEAR) + "/"
#auto subfolder generation
if not os.path.isdir(csv_dir):
    os.makedirs(csv_dir)
if not os.path.isdir(tif_dir):
    os.makedirs(tif_dir)
if not os.path.isdir(shp_dir):
    os.makedirs(shp_dir)
if not os.path.isdir(mosaic_dir):
    os.makedirs(mosaic_dir)
if not os.path.isdir(result_dir):
    os.makedirs(result_dir)


def clean20022010():
    suf = 1
    title = "Null"
    #A function used for cleaning 2002 ~ 2010 CSV files.
    path = ori_dir
    out = csv_dir
    csvs = os.listdir(path)
    for csv in csvs:
        print("Processing: " + csv)
        if csv[0:2] == "33":
            if "GG" in csv:
                title = "g_"
            elif "RO" in csv:
                title = "O_"
            else:
                title = "3_"
            df = pd.read_csv(path + "/" + csv, header=0)
            unique = df["DATE_UTC__ddmmyyyy"].unique()
            for value in unique:
                out_df = df.loc[df['DATE_UTC__ddmmyyyy'] == value]
                if len(str(int(value))) == 7:
                    value = "0" + str(int(value))
                    print("0" + str(value))
                if YEAR == 2010 or csv == "33RO20080101.csv":
                    out_name = title + str(value)[4:8] + str(value)[2:4] + str(value)[0:2] + ".csv"
                else:
                    out_name = title + str(value)[4:8] + str(value)[0:2] + str(value)[2:4] + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        elif "RB" in csv or "rhb" in csv or "Explorer" in csv or "FSH" in csv or "gu" in csv or "74X" in csv:
            df = pd.read_csv(path + csv, header=0)
            if "RB" in csv:
                title = "R_"
            elif "rhb" in csv:
                title = "h_"
            elif "FSH" in csv:
                title = "F_"
            elif "gu" in csv:
                title = "U_"
            elif "74X" in csv:
                title = "X_"
            elif "Explorer" in csv:
                if "st" in csv:
                    title = str(csv).split(".")[0][-4] + "_"
                else:
                    title = str(csv).split(".")[0][-2] + "_"
            df.dropna(subset=["DATE"], inplace=True)
            unique = df["DATE"].unique()
            for value in unique:
                out_df = df.loc[df['DATE'] == value]
                if len(str(int(value))) == 7:
                    value = "0" + str(int(value))
                    print(value)
                if "front" in csv:
                    out_name = title + str(value)[0:4] + str(value)[4:6] + str(value)[6:8] + ".csv"
                else:
                    out_name = title + str(value)[4:8] + str(value)[2:4] + str(value)[0:2] + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        elif "a.csv" in csv or "SAB" in csv or "GM" in csv or "AFT" in csv:
            df = pd.read_csv(path + "/" + csv, header=0)
            if "a.csv" in csv:
                title = "A_"
            elif "SAB" in csv:
                title = "B_"
            elif "AFT" in csv:
                title = "T_"
            elif "GM" in csv:
                title = "G_"
            df.dropna(subset=["DATE"], inplace=True)
            unique = df["DATE"].unique()
            for value in unique:
                out_df = df.loc[df['DATE'] == value]
                month = str(value).split("/")[0]
                day = str(value).split("/")[1]
                year = str(value).split("/")[2]
                if len(str(month)) == 1:
                    month = "0" + month
                if len(str(day)) == 1:
                    day = "0" + day
                out_name = title + year + month + day + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        else:
            print("No pattern found for the file: " + csv)


def clean20132020():
    suf = 1
    title = "Null"
    #A function used for cleaning 2010 ~ 2018 CSV files.
    path = ori_dir
    out = csv_dir
    csvs = os.listdir(path)
    for csv in csvs:
        print("Processing: " + csv)
        #pattern ddmmyyyy
        if csv[0:2] == "33" or csv[0:4] == "BMBE" or csv[0:4] == "BHAF" or csv[0:4] == "MLCE":
            if csv[2:4] == "WA":
                if YEAR == 2016:
                    df = pd.read_csv(path + "/" + csv, skiprows=5, header=0)
                elif YEAR == 2017 or YEAR == 2019:
                    df = pd.read_csv(path + "/" + csv, skiprows=4, header=0)
                else:
                    df = pd.read_csv(path + "/" + csv, skiprows=2,header=0)
                title = "W_"
            elif csv[2:4] == "GG":
                if YEAR == 2016:
                    df = pd.read_csv(path + "/" + csv, skiprows=5, header=0)
                elif YEAR == 2017:
                    df = pd.read_csv(path + "/" + csv, skiprows=4, header=0)
                else:
                    df = pd.read_csv(path + "/" + csv, skiprows=2, header=0)
                title = "G_"
            elif csv[0:4] == "BMBE":
                df = pd.read_csv(path + "/" + csv, skiprows=5, header=0)
                title = "B_"
            elif csv[0:4] == "BHAF":
                df = pd.read_csv(path + "/" + csv, skiprows=5, header=0)
                title = "H_"
            elif csv[0:4] == "MLCE":
                df = pd.read_csv(path + "/" + csv, skiprows=4, header=0)
                title = "M_"
            unique = df["DATE_UTC__ddmmyyyy"].unique()
            for value in unique:
                out_df = df.loc[df['DATE_UTC__ddmmyyyy'] == value]
                if len(str(value)) == 7:
                    value = "0" + str(value)
                    print("0" + str(value))
                else:
                    print(str(value))
                out_name = title + str(value).split(".")[0][4:8]+ str(value).split(".")[0][2:4] + str(value).split(".")[0][0:2] + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        #pattern yyyymmdd
        elif csv[0:4] == "GOME":
            df = pd.read_csv(path + csv, header=0)
            if "BOT" in csv :
                title = "O_"
            elif "UW" in csv:
                title = "U_"
            df.dropna(subset=["DATE"], inplace=True)
            unique = df["DATE"].unique()
            for value in unique:
                out_df = df.loc[df['DATE'] == value]
                if len(str(int(value))) == 7:
                    value = "0" + str(int(value))
                    print(value)
                out_name = title + str(value)[0:4] + str(value)[4:6] + str(value)[6:8] + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        #pattern mm/dd/yyyy
        elif csv[2:4] == "RO":
            title = "R_"
            df = pd.read_csv(path + "/" + csv, header=0)
            df.dropna(subset=["Date"], inplace=True)
            unique = df["Date"].unique()
            for value in unique:
                out_df = df.loc[df['Date'] == value]
                month = str(value).split("/")[0]
                day = str(value).split("/")[1]
                year = str(value).split("/")[2]
                if len(str(month)) == 1:
                    month = "0" + month
                if len(str(day)) == 1:
                    day = "0" + day
                out_name = title + year + month + day + ".csv"
                print(out_name)
                feature = out + out_name
                if os.path.isfile(feature):
                    suf = suf + 1
                    new_out_name = out_name.split(".")[0] + "_" + str(suf) + ".csv"
                    print("Warning: file already exists: " + feature + ", renamed it to: " + new_out_name)
                    feature = out + new_out_name
                out_df.to_csv(feature)
        else:
            print("No pattern found for the file: " + csv)


def toshp20022010():
    #This function is not strictly defined. The settings may vary case by case. Plz modify the function settings before you run.
    csvs = os.listdir(csv_dir)
    for csv in csvs:
        print("Processing: " + csv)
        name = str(csv).split(".")[0]
        lat = "Null"
        lon = "Null"
        if "csv" in csv and not os.path.isfile(shp_dir + name + ".shp"):
            if "R" in name or "h" in name:
                lon = "LONG_DEC_DEGREE"
                lat = "LAT_DEC_DEGREE"
            elif "3_" in name or "g" in name or "U" in name or "X" in name or "O" in name:
                lon = "LONG_dec_degree"
                lat = "LAT_dec_degree"
            elif "E" in name or "W" in name or "N" in name:
                lon = "Long_dec_degree"
                lat = "Lat_dec_degree"
            elif "A" in name or "G" in name or "F" in name:
                lon = "LONGITUDE"
                lat = "LATITUDE"
            elif "B" in name or "S" in name:
                lon = "long"
                lat = "lat"
            arcpy.MakeXYEventLayer_management(csv_dir + csv, lon, lat, name)
            arcpy.FeatureClassToShapefile_conversion(name, shp_dir)
            arcpy.Delete_management(name)
        else:
            print("Irrelevant file or Shp already exist: " + name + ".shp")


def toshp20132020():
    #This function is not strictly defined. The settings may vary case by case. Plz modify the function settings before you run.
    #csv_dir = r"E:\seadas\rui\missed\point/"
    #shp_dir = r"E:\seadas\rui\missed\shp/"
    lat = "Null"
    lon = "Null"
    csvs = os.listdir(csv_dir)
    for csv in csvs:
        print("Processing: " + csv)
        name = str(csv).split(".")[0]
        if "csv" in csv and not os.path.isfile(shp_dir + name + ".shp"):
            if "B" in name or "W" in name or "G" in name or "H" in name or "M" in name:
                lon = "LONG_dec_degree"
                lat = "LAT_dec_degree"
            elif "O" in name or "U" in name or "R" in name:
                lon = "LONGITUDE"
                lat = "LATITUDE"
            arcpy.MakeXYEventLayer_management(csv_dir + csv, lon, lat, name)
            arcpy.FeatureClassToShapefile_conversion(name, shp_dir)
            arcpy.Delete_management(name)
        else:
            print("Irrelevant file or Shp already exist: " + name + ".shp")


def datematch():
    csvs = os.listdir(csv_dir)
    for file in csvs:
        if "csv" in file:
            print(file)
            csv_year = str(file)[2:6]
            csv_month = str(file)[6:8]
            csv_day = str(file)[8:10]
            csv_date = csv_year + csv_month + csv_day
            print("csv_date: " + csv_date)
            ncs = os.listdir(nc_dir)
            for nc in ncs:
                nc_year = "None"
                nc_month = "None"
                nc_day = "None"
                if "MODIS" in nc:
                    print("Matching: "+ nc)
                    nc_date = str(nc).split(".")[1]
                    nc_type = "SST"
                    nc_year = str(nc_date)[0:4]
                    nc_month = str(nc_date)[4:6]
                    nc_day = str(nc_date)[6:8]
                    rename = nc_dir + "/" + nc_type + nc_date + ".nc"
                elif "LAC" in nc:
                    print("Matching: " + nc)
                    nc_type = "OC"
                    nc_year = str(nc)[1:5]
                    nc_days = str(nc)[5:8]
                    dat = datetime.datetime(int(nc_year), 1, 1) + datetime.timedelta(int(nc_days) - 1)
                    nc_month = dat.month
                    nc_day = dat.day
                    if nc_month < 10:
                        nc_month = "0" + str(nc_month)
                    if nc_day < 10:
                        nc_day = "0" + str(nc_day)
                    rename = nc_dir + nc_type + \
                                str(nc_year) + str(nc_month) + str(nc_day) + \
                                str(nc).split(".")[0][8:] + ".nc"
                else:
                    print("Skip this file: " + nc)
                nc_date = str(nc_year) + str(nc_month) + str(nc_day)
                print(nc_date)
                print(csv_date)
                if csv_date == nc_date:
                    print("Matched nc date: " + nc_date)
                    os.rename(nc_dir + nc,rename)
                    print("nc file: " + nc + " has been transfered to: " + rename)
                else:
                    print("No matched file or duplicate file: " + nc + ", skipped to the next one...")


def seadas_txt():
    # output Lvisbullseye syntax list
    nc_dir = r"E:\OC\nc/"
    VM_nc_dir = r'/home/shawn/Desktop/OC/nc/'
    VM_raster_dir = r'/home/shawn/Desktop/OC/result/reproject/'
    ncs = os.listdir(nc_dir)
    with open(nc_dir + "run_seadas.txt", 'w') as output:
        for nc in ncs:
            if "x" not in nc:
                print("Processing: " + nc)
                output.write("sh gpt.sh -e ReprojectGeoLatLon.xml -p ReprojectGeoLatLon.par -Ssource=" + VM_nc_dir + nc
                             + " -t " + VM_raster_dir + str(nc).split(".")[0] + ".tif -f Geotiff" + '\n')


'''after run seadas_txt function, run seadas gpt reprojection tool'''
'''after seadas gpt reprojection, run r mosaic'''
'''after r mosaic, run function multivaluestopoint'''


def multivaluestopoint():
    arcpy.env.workspace = shp_dir
    for shp in arcpy.ListFeatureClasses():
        shp_prefix = str(shp).split(".")[0][2:10]
        print("Processing shp: " + shp)
        tif_OC = mosaic_dir + "OC" + shp_prefix + "_mosaic.tif"
        tif_SST = mosaic_dir + "SST" + shp_prefix + "_mosaic.tif"
        feature = shp_dir + shp
        if os.path.isfile(tif_OC):
            print("Matching: " + tif_OC + " and " + shp)
            field = "'" + "OC" + shp_prefix + "'"
            try:
                ExtractMultiValuesToPoints(feature, tif_OC + ' ' + field, "NONE")
            except:
                print("No interection between " + tif_OC + " and " + shp)
        if os.path.isfile(tif_SST):
            print("Matching: " + tif_SST + " and " + shp)
            field = "'" + "SST" + shp_prefix + "'"
            try:
                ExtractMultiValuesToPoints(feature, tif_SST + ' ' + field, "NONE")
            except:
                print("No interection between " + tif_SST + " and " + shp)





def misscsvmerge():
    path = r"E:\seadas\rui\missed\point/"
    csvs = os.listdir(path)
    for csv1 in csvs:
        csv_subname1 = str(csv1)[0:10]
        for csv2 in csvs:
            csv_subname2 = str(csv2)[0:10]
            if csv_subname1 == csv_subname2:
                print("Processing test case: " + csv_subname1)
                df1 = pd.read_csv(path + "/" + csv1, header=0)
                df2 = pd.read_csv(path + "/" + csv2, header=0)
                df_merge = pd.concat([df1,df2])
                out = path + csv_subname1 + "_merge.csv"
                df_merge.to_csv(out, index=None)


def missvaluetopoint():
    shp_dir = r"E:\seadas\rui\missed\shp/"
    arcpy.env.workspace = shp_dir
    for shp in arcpy.ListFeatureClasses():
        shp_prefix = str(shp).split(".")[0][2:10]
        print("Processing shp: " + shp)
        year = str(shp).split(".")[0][2:6]
        tif_OC = r"E:\seadas\rui\result\tif\mosaic/" + str(year) + "\OC" + shp_prefix + "_mosaic.tif"
        tif_SST = r"E:\seadas\rui\result\tif\mosaic/" + str(year) + "\SST" + shp_prefix + "_mosaic.tif"
        feature = shp_dir + shp
        if os.path.isfile(tif_OC):
            print("Matching: " + tif_OC + " and " + shp)
            field = "'" + "OC" + shp_prefix + "'"
            ExtractMultiValuesToPoints(feature, tif_OC + ' ' + field, "NONE")
        if os.path.isfile(tif_SST):
            print("Matching: " + tif_SST + " and " + shp)
            field = "'" + "SST" + shp_prefix + "'"
            ExtractMultiValuesToPoints(feature, tif_SST + ' ' + field, "NONE")


def qualitycheck():
    # check if OC or SST has been extracted to points
    path = r"E:\seadas\rui\result\result_csv/"
    folders = os.listdir(path)
    for folder in folders:
        oc_check = 0
        sst_check = 0
        path_folder = path + folder + "/"
        csvs = os.listdir(path_folder)
        for csv in csvs:
            df = pd.read_csv(path_folder + csv)
            names = list(df.columns)
            if 'Rrs_412' not in names:
                oc_check = oc_check + 1
                print("Failure oc file: " + csv)
            elif 'sst' not in names:
                sst_check = sst_check + 1
                print("Failure sst file: " + csv)
        print("Match folder: " + str(folder))
        print("Total file count: " + str(len(csvs)))
        print("OC match failures: " + str(oc_check))
        print("SST match failures: " + str(sst_check))


def mosaic_match():
    #detect unaligned OC/SST
    mosaics = os.listdir(mosaic_dir)
    for file in mosaics:
        date = str(file)[-19:]
        OC = "OC" + date
        SST = "SST" + date
        if not os.path.isfile(mosaic_dir+OC):
            print("No oc file: " + OC)
        elif not os.path.isfile(mosaic_dir+SST):
            print("No sst file: " + SST)

# extent function()

def copy():
    year = 2017
    out = r"C:\Users\Shawn\Desktop\New folder/"
    nc_dir = r"C:\Users\Shawn\Downloads\New folder\nc/" + str(year) + "/"
    ncs = os.listdir(nc_dir)
    file = r"C:\Users\Shawn\Desktop\mylist.csv"
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        print(row["x"])
        if str(year) in str(row["x"]):
            for nc in ncs:
                if str(row["x"]) in nc:
                    shutil.copy2(nc_dir + nc,out + nc)


def compband():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"E:/OC/result/"
    out_dir = r"E:/OC/subset/"
    raster_list = arcpy.ListRasters("*", "TIF")
    print(raster_list)
    for r in raster_list:
        print("Extracting bands from: " + r)
        output = out_dir + r
        if "OC" in r:
            arcpy.MakeRasterLayer_management(r, "rdlayer", "#", "#", [1,3,5,7,9,11,13,15,17,19,21,23])
        else:
            arcpy.MakeRasterLayer_management(r, "rdlayer", "#", "#", [1, 3])
        arcpy.CopyRaster_management("rdlayer", output)


def drop():
    path = r"E:\OC\csv/"
    out = r"E:\OC\csv_2/"
    csvs = os.listdir(path)
    for csv in csvs:
        print("Removing joined OC and SST..." + csv)
        df = pd.read_csv(path + csv)
        df.drop(columns=['Rrs_412', 'Rrs_443','Rrs_469','Rrs_488','Rrs_531','Rrs_547','Rrs_555','Rrs_645',
                         'Rrs_667','Rrs_678','chlor_a','Kd_490','sst','qual_sst'], axis=1, inplace=True)
        df.to_csv(out + csv)


def csv_find():
    path = r"E:\OC\csv_2/"
    mosaic_dir = r"E:\OC\subset/"
    out = r"E:\OC\trash/"
    csvs = os.listdir(path)
    for csv in csvs:
        prefix = str(csv).split(".")[0][2:10]
        print("Processing csv: " + csv)
        tif_OC = mosaic_dir + "OC" + prefix + ".tif"
        if not os.path.isfile(tif_OC):
            shutil.move(path + csv, out + csv)
        else:
            print("Keep..." + csv)


def new_toshp():
    path = r"E:\OC\csv_2/"
    out = r"E:\OC\shp"
    csvs = os.listdir(path)
    for csv in csvs:
        df = pd.read_csv(path + csv)
        names = list(df.columns)
        if "LAT_DEC_DE" in names:
            lat = "LAT_DEC_DE"
            lon = "LONG_DEC_D"
            df_coor = df[(df["LAT_DEC_DE"] > 17)
                         & (df["LAT_DEC_DE"] < 32)
                         & (df["LONG_DEC_D"] > -98)
                         & (df["LONG_DEC_D"] < -79.9)]
        elif "Lat_dec_de" in names:
            lat = "Lat_dec_de"
            lon = "Long_dec_d"
            df_coor = df[(df["Lat_dec_de"] > 17)
                         & (df["Lat_dec_de"] < 32)
                         & (df["Long_dec_d"] > -98)
                         & (df["Long_dec_d"] < -79.9)]
        elif "LAT_dec_de" in names:
            lat = "LAT_dec_de"
            lon = "LONG_dec_d"
            df_coor = df[(df["LAT_dec_de"] > 17)
                         & (df["LAT_dec_de"] < 32)
                         & (df["LONG_dec_d"] > -98)
                         & (df["LONG_dec_d"] < -79.9)]
        elif "LATITUDE" in names:
            lat = "LATITUDE"
            lon = "LONGITUDE"
            df_coor = df[(df["LATITUDE"] > 17)
                         & (df["LATITUDE"] < 32)
                         & (df["LONGITUDE"] > -98)
                         & (df["LONGITUDE"] < -79.9)]
        elif "lat" in names:
            lat = "lat"
            lon = "long"
            df_coor = df[(df["lat"] > 17)
                         & (df["lat"] < 32)
                         & (df["long"] > -98)
                         & (df["long"] < -79.9)]
        else:
            print("check coor name of file: " + csv )
        if df_coor.empty:
            print("csv coords out of extent: " + csv)
            os.rename(path + csv, path + csv.split(".")[0] + "_out.csv")
        else:
            name = csv.split(".")[0]
            arcpy.MakeXYEventLayer_management(path + csv, lon, lat, name)
            arcpy.FeatureClassToShapefile_conversion(name, out)
            arcpy.Delete_management(name)


def new_extraction():
    mosaic_dir = r"E:\OC\subset/"
    shp_dir = r"E:\OC\shp/"
    arcpy.env.workspace = shp_dir
    for shp in arcpy.ListFeatureClasses():
        shp_prefix = str(shp).split(".")[0][2:10]
        print("Processing shp: " + shp)
        tif_OC = mosaic_dir + "OC" + shp_prefix + ".tif"
        tif_SST = mosaic_dir + "SST" + shp_prefix + ".tif"
        feature = shp_dir + shp
        if os.path.isfile(tif_OC):
            print("Matching: " + tif_OC + " and " + shp)
            field = "'" + "OC" + shp_prefix + "'"
            try:
                ExtractMultiValuesToPoints(feature, tif_OC + ' ' + field, "NONE")
            except:
                print("No interection between " + tif_OC + " and " + shp)
        if os.path.isfile(tif_SST):
            print("Matching: " + tif_SST + " and " + shp)
            field = "'" + "SST" + shp_prefix + "'"
            try:
                ExtractMultiValuesToPoints(feature, tif_SST + ' ' + field, "NONE")
            except:
                print("No interection between " + tif_SST + " and " + shp)

def tocsv():
    shp_dir = r"E:\OC\shp_20022010/"
    result_dir = r"E:\OC\result_csv_20022010/"
    arcpy.env.workspace = shp_dir
    for shp in arcpy.ListFeatureClasses():
        YEAR = str(shp).split(".")[0][2:6]
        print("Shapefile to csv: " + shp + " Year: "+ str(YEAR))
        xls = result_dir + str(shp).split(".")[0] + ".xls"
        csv = result_dir + str(shp).split(".")[0] + ".csv"
        feature = shp_dir + shp
        arcpy.TableToExcel_conversion(feature, xls)
        data_xls = pd.read_excel(xls)
        names = list(data_xls.columns)
        id = "b1_OC" + str(YEAR) + "0"
        if id in names:
            n = "0"
        else:
            n = "1"
        suf1 = "_OC" + str(YEAR) + n
        suf2 = "_OC" + str(YEAR)
        Rrs_412 = "b1" + suf1
        Rrs_443 = "b2" + suf1
        Rrs_469 = "b3" + suf1
        Rrs_488 = "b4" + suf1
        Kd_490 = "b5" + suf1
        Rrs_531 = "b6" + suf1
        Rrs_547 = "b7" + suf1
        Rrs_555 = "b8" + suf1
        Rrs_645 = "b9" + suf1
        Rrs_667 = "b10" + suf2
        Rrs_678 = "b11" + suf2
        chlor_a = "b12" + suf2
        sst = "b1_SST" + str(YEAR)
        qual_sst = "b2_SST" + str(YEAR)
        data_xls = data_xls.rename({Rrs_412: 'Rrs_412', Rrs_443: 'Rrs_443',
                                    Rrs_469: 'Rrs_469', Rrs_488: 'Rrs_488',
                                    Rrs_531: 'Rrs_531', Rrs_547: 'Rrs_547',
                                    Rrs_555: 'Rrs_555', Rrs_645: 'Rrs_645',
                                    Rrs_667: 'Rrs_667', Rrs_678: 'Rrs_678',
                                    chlor_a: 'chlor_a', Kd_490: 'Kd_490',
                                    sst: 'sst', qual_sst: 'qual_sst'}, axis=1)
        names = list(data_xls.columns)
        if 'Rrs_412' not in names:
            print("OC match failed: " + shp)
        elif 'sst' not in names:
            print("SST match failed: " + shp)
        else:
            data_xls.to_csv(csv)
            print("csv file has been saved to： " + csv)
        os.remove(xls)



def date_change_all():
    nc_dir = r"C:\Users\Shawn\Downloads\OC_2\requested_files/"
    ncs = os.listdir(nc_dir)
    for nc in ncs:
        nc_year = "None"
        nc_month = "None"
        nc_day = "None"
        if "MODIS" in nc:
            print("Matching: "+ nc)
            nc_date = str(nc).split(".")[1]
            nc_type = "SST"
            nc_year = str(nc_date)[0:4]
            nc_month = str(nc_date)[4:6]
            nc_day = str(nc_date)[6:8]
            rename = nc_dir + nc_type + nc_date + ".nc"
        elif "LAC" in nc:
            print("Matching: " + nc)
            nc_type = "OC"
            nc_year = str(nc)[1:5]
            nc_days = str(nc)[5:8]
            dat = datetime.datetime(int(nc_year), 1, 1) + datetime.timedelta(int(nc_days) - 1)
            nc_month = dat.month
            nc_day = dat.day
            if nc_month < 10:
                nc_month = "0" + str(nc_month)
            if nc_day < 10:
                nc_day = "0" + str(nc_day)
            rename = nc_dir + nc_type + \
                        str(nc_year) + str(nc_month) + str(nc_day) + \
                        str(nc).split(".")[0][8:] + ".nc"
        else:
            print("Skip this file: " + nc)
        nc_date = str(nc_year) + str(nc_month) + str(nc_day)
        print(nc_date)
        os.rename(nc_dir + nc,rename)



#clean20022010()
#toshp20022010()

#clean20132020()
#toshp20132020()

#datematch()
seadas_txt()

#multivaluestopoint()
#tocsv() modified, find the previous one

#qualitycheck()



#copy()
#compband()
#drop()
#csv_find()
#new_toshp()
#new_extraction()
#tocsv()
#date_change_all()