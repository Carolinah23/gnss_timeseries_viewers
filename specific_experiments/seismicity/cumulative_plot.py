# Get the cumulative seismicity


import numpy as np 
import matplotlib.pyplot as plt 
import datetime as dt 
from collections import namedtuple

SeisCat = namedtuple("SeisCat",['dtarray','lon','lat','dep','mag']);

def configure():
	input_file = "../../GPS_POS_DATA/Seismicity/MTJ_box_search.txt";
	return input_file;

def inputs(input_file):
	ifile=open(input_file,'r');
	dtarray=[]; lon=[]; lat=[]; dep=[]; mag=[];
	for line in ifile:
		temp=line.split();
		if temp[0]=="#":
			continue;
		lon.append(float(temp[3]));
		lat.append(float(temp[2]));
		dep.append(float(temp[4]));
		mag.append(float(temp[5]));
		dtarray.append(dt.datetime.strptime(temp[0]+' '+temp[1][0:8],"%Y/%m/%d %H:%M:%S"))
	ifile.close();
	mycat = SeisCat(lon=lon, lat=lat, dtarray=dtarray, dep=dep, mag=mag);
	return mycat;

def compute(mycat):
	cdts=[]; cnums=[];
	cdts_shallow=[]; cnums_shallow=[];
	cdts_shallow.append(mycat.dtarray[0]);
	cnums_shallow.append(1);
	cdts.append(mycat.dtarray[0]);
	cnums.append(1);
	for i in range(1,len(mycat.dtarray)):
		if mycat.lon[i]>=-123.8 and mycat.lon[i]<=-122.9:
			if mycat.dep[i]>=20:
				cdts.append(mycat.dtarray[i]);
				cdts.append(mycat.dtarray[i]);
				cnums.append(cnums[-1]);
				cnums.append(cnums[-1]+1);
			else:
				cdts_shallow.append(mycat.dtarray[i]);
				cdts_shallow.append(mycat.dtarray[i]);
				cnums_shallow.append(cnums_shallow[-1]);
				cnums_shallow.append(cnums_shallow[-1]+1);			
	return [cdts, cnums, cdts_shallow, cnums_shallow];

def outputs(mycat, cdts, cnums, cdts_shallow, cnums_shallow):
	eqtimes=[];
	eqtimes.append(dt.datetime.strptime("20050615","%Y%m%d"));
	eqtimes.append(dt.datetime.strptime("20100110","%Y%m%d"));
	eqtimes.append(dt.datetime.strptime("20140310","%Y%m%d"));
	eqtimes.append(dt.datetime.strptime("20161208","%Y%m%d"));
	starttime=dt.datetime.strptime("20090606","%Y%m%d");
	endtime=dt.datetime.strptime("20190505","%Y%m%d");

	plt.figure();
	plt.plot(cdts, cnums, color='indianred',label='Deep (>20 km depth)');
	plt.plot(cdts_shallow, cnums_shallow, color='blue',label='Shallow (<20 km depth)');
	plt.grid(True);
	[ymin, ymax] = plt.gca().get_ylim();
	for i in range(len(eqtimes)):
		plt.plot([eqtimes[i], eqtimes[i]],[ymin, ymax],'--k');
	plt.ylabel("Cumulative Seismicity (number of earthquakes) ");
	plt.xlabel("Time");
	plt.legend();
	plt.savefig('Seismicity.jpg');
	return;


if __name__=="__main__":
	infile = configure();
	mycat = inputs(infile);
	[cdts, cnums, cdts_shallow, cnums_shallow] = compute(mycat);
	outputs(mycat, cdts, cnums, cdts_shallow, cnums_shallow);