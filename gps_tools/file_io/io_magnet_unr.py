
"""
File to read and write data from Magnet / University of Nevada Reno formats
"""
import datetime as dt
import sys

import numpy as np
from gps_tools import utilities
from gps_tools.gps_objects import Station_Vel, Timeseries


def read_unr_vel_file(infile, coordinate_file):
    """
    Read velocity files from the MAGNET/MIDAS website, looking up coordinates from associated file.
    Returns a list of station_vel objects.
    """
    myVelfield = []
    # open cache of coordinates and start-dates
    [cache_name, cache_lat, cache_lon, dtbeg, dtend] = np.loadtxt(coordinate_file, unpack=True, skiprows=1,
                                                                  usecols=(0, 1, 2, 7, 8), dtype={
            'names': ('name', 'lat', 'lon', 'dtbeg', 'dtend'),
            'formats': ('U4', float, float, 'U10', 'U10')});
    if 'IGS14_' in infile:
        refframe = 'ITRF';
    else:
        refframe = 'NA';

    print("Reading %s" % infile);
    ifile = open(infile, 'r');
    for line in ifile:
        temp = line.split();
        if temp[0] == "#":
            continue;
        else:
            name = temp[0];
            e = float(temp[8]) * 1000.0;
            n = float(temp[9]) * 1000.0;
            u = float(temp[10]) * 1000.0;
            se = float(temp[11]) * 1000.0;
            sn = float(temp[12]) * 1000.0;
            su = float(temp[13]) * 1000.0;

            myindex = np.where(cache_name == name);
            if len(myindex[0]) == 0:
                print("Error! Could not find cache record for station %s in %s " % (name, coordinate_file));
                sys.exit(0);
            else:
                first_epoch = dt.datetime.strptime(dtbeg[myindex[0][0]], '%Y-%m-%d');
                last_epoch = dt.datetime.strptime(dtend[myindex[0][0]], '%Y-%m-%d');
                elon = cache_lon[myindex[0][0]];
                elon = utilities.check_lon_sanity(elon);
                nlat = cache_lat[myindex[0][0]];

            myStationVel = Station_Vel(name=name, elon=elon, nlat=nlat, e=e, n=n, u=u,
                                       se=se, sn=sn, su=su, first_epoch=first_epoch, last_epoch=last_epoch,
                                       proccenter='unr', subnetwork='', refframe=refframe, survey=0, meas_type='gnss');
            myVelfield.append(myStationVel);
    ifile.close();
    return [myVelfield];


def read_UNR_magnet_ts_file(filename, coordinates_file):
    print("Reading %s" % filename);
    [datestrs, dE, dN, dU, Se, Sn, Su] = np.loadtxt(filename, usecols=(1, 8, 10, 12, 14, 15, 16), skiprows=1,
                                                    unpack=True,
                                                    dtype={'names': ('datestrs', 'dE', 'dN', 'dU', 'Se', 'Sn', 'Su'),
                                                           'formats': ('U7', float, float, float,
                                                                       float, float, float)});

    station_name = filename.split('/')[-1][0:4];  # the first four characters of the filename
    dtarray = [dt.datetime.strptime(x, '%y%b%d') for x in datestrs];  # has format 07SEP19
    dN = [i * 1000.0 for i in dN];
    dE = [i * 1000.0 for i in dE];
    dU = [i * 1000.0 for i in dU];
    Sn = [i * 1000.0 for i in Sn];
    Se = [i * 1000.0 for i in Se];
    Su = [i * 1000.0 for i in Su];

    [lon, lat] = get_coordinates_for_unr_stations([station_name], coordinates_file);  # format [lat, lon]
    lon = utilities.check_lon_sanity(lon[0]);
    coords = [lon, lat[0]];

    myData = Timeseries(name=station_name, coords=coords, dtarray=dtarray, dN=dN, dE=dE, dU=dU, Sn=Sn, Se=Se, Su=Su,
                        EQtimes=[]);
    print("Reading data for station %s in time range %s:%s" % (
        myData.name, dt.datetime.strftime(myData.dtarray[0], "%Y-%m-%d"),
        dt.datetime.strftime(myData.dtarray[-1], "%Y-%m-%d")));
    return [myData];


def get_coordinates_for_unr_stations(station_names, coordinates_file):
    """
    Read UNR coordinates for set of stations.

    :param station_names: array of strings
    :param coordinates_file: cache of coordinates and start-dates
    """
    [cache_names, cache_lat, cache_lon] = np.loadtxt(coordinates_file, unpack=True, skiprows=2,
                                                     usecols=(0, 1, 2), dtype={'names': ('name', 'lat', 'lon'),
                                                                               'formats': ('U4', float, float)});
    lon, lat = [], [];
    # find the stations
    for i in range(len(station_names)):
        myindex = np.where(cache_names == station_names[i]);
        if not myindex[0]:
            print("Error! No UNR cache record for station %s in %s " % (station_names[i], coordinates_file));
            sys.exit(0);
        else:
            elon = cache_lon[myindex[0][0]];
            elon = utilities.check_lon_sanity(elon);
            nlat = cache_lat[myindex[0][0]];
            lon.append(elon);
            lat.append(nlat);
    return [lon, lat];