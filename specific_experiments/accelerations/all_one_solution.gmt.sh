#!/bin/bash

# Plot that shows data in integrated way

lonW="-124.9"
lonE="-118.7"
latS="35.5"
latN="42.2"
range="$lonW/$lonE/$latS/$latN"
projection="M3.3i"  # used for medium experiments.
horiz_scale=0.3  # used for velocity change vectors (0.3 sometimes, sometimes smaller)
output1='Figures/NorCal.ps'
offset=9

folder="pbo_lssq_NA/"
file1=2010.txt
name1="2010"
file2=2014.txt
name2="2014"
file3=2016.txt
name3="2016"


gmt makecpt -T-29000/8000/500 -Cgray -Z > blue_topo.cpt


# THE FIRST MAP
infile=$folder$file1
gmt pscoast -R$range -J$projection -Slightblue -N1 -N2 -B1.0WeSn -Dh -K -X2 -Y2 > $output1

gmt grdgradient ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -A320 -R$range -Getopo1.grad -Nt
gmt grdhisteq etopo1.grad -Getopo1.hist -N
gmt grdinfo etopo1.hist 
gmt grdmath etopo1.hist 8.41977 DIV = etopo1.norm
gmt grdimage ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -Ietopo1.norm -R$range -J$projection -Cblue_topo.cpt -K -O >> $output1

gmt pscoast -R$range -J$projection -Lf-123.7/37.2/37.2/50+jt -N1 -N2 -Wthinner,black -Dh -K -O >> $output1 

# Add the plate boundaries
gmt psxy ../../../Misc/Mapping_Resources/transform.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/ridge.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/trench.gmt -R$range -J$projection -Wthin,red -Sf1.5/0.6+r+t+o1.8 -K -O >> $output1

# Add PBO velocity vectors
awk '{print $1, $2, $3, $4, $7, $8, $10}' $infile | gmt psvelo -R$range -J$projection -O -K -Se$horiz_scale/0.68/8 -A+e+gblack+pthickest -Wthinnest,black >> $output1
gmt psvelo -R$range -J$projection -A+e+gblack+pthickest -Se$horiz_scale/0.68/10 -Wthinnest,black -K -O <<EOF >> $output1
-125.2 41.8 2 0 0.2 0.2 0.0 2+-0.2mm/yr
EOF

grep 'nan' $infile | awk '{print $1, $2}' | gmt psxy -R$range -J$projection -O -K -Gdarkblue -Sc0.05 >> $output1

gmt pstext -R$range -J$projection -F+f18p,Helvetica -Gwhite -K -O <<EOF >> $output1
-119.5 41.8 $name1
-124 41.8 A
EOF




# THE SECOND MAP
infile=$folder$file2
gmt pscoast -R$range -J$projection -Slightblue -N1 -N2 -B1.0weSn -Dh -K -O -X$offset -Y0 >> $output1

gmt grdgradient ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -A320 -R$range -Getopo1.grad -Nt
gmt grdhisteq etopo1.grad -Getopo1.hist -N
gmt grdinfo etopo1.hist 
gmt grdmath etopo1.hist 8.41977 DIV = etopo1.norm
gmt grdimage ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -Ietopo1.norm -R$range -J$projection -Cblue_topo.cpt -K -O >> $output1

gmt pscoast -R$range -J$projection -Lf-123.7/37.2/37.2/50+jt -N1 -N2 -Wthinner,black -Dh -K -O >> $output1 

# Add the plate boundaries
gmt psxy ../../../Misc/Mapping_Resources/transform.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/ridge.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/trench.gmt -R$range -J$projection -Wthin,red -Sf1.5/0.6+r+t+o1.8 -K -O >> $output1

# Add PBO velocity vectors
awk '{print $1, $2, $3, $4, $7, $8, $10}' $infile | gmt psvelo -R$range -J$projection -O -K -Se$horiz_scale/0.68/8 -A+e+gblack+pthickest -Wthinnest,black >> $output1
gmt psvelo -R$range -J$projection -A+e+gblack+pthickest -Se$horiz_scale/0.68/10 -Wthinnest,black -K -O <<EOF >> $output1
-125.2 41.8 2 0 0.2 0.2 0.0 2+-0.2mm/yr
EOF

grep 'nan' $infile | awk '{print $1, $2}' | gmt psxy -R$range -J$projection -O -K -Gdarkblue -Sc0.05 >> $output1

gmt pstext -R$range -J$projection -F+f18p,Helvetica -Gwhite -K -O <<EOF >> $output1
-119.5 41.8 $name2
-124 41.8 B
EOF




# THE THIRD MAP
infile=$folder$file3
gmt pscoast -R$range -J$projection -Slightblue -N1 -N2 -B1.0weSn -Dh -K -O -X$offset -Y0 >> $output1

gmt grdgradient ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -A320 -R$range -Getopo1.grad -Nt
gmt grdhisteq etopo1.grad -Getopo1.hist -N
gmt grdinfo etopo1.hist 
gmt grdmath etopo1.hist 8.41977 DIV = etopo1.norm
gmt grdimage ../../../Misc/Mapping_Resources/Global_topography_data/ETOPO1_Bed_g_gmt4.grd -Ietopo1.norm -R$range -J$projection -Cblue_topo.cpt -K -O >> $output1

gmt pscoast -R$range -J$projection -Lf-123.7/37.2/37.2/50+jt -N1 -N2 -Wthinner,black -Dh -K -O >> $output1 

# Add the plate boundaries
gmt psxy ../../../Misc/Mapping_Resources/transform.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/ridge.gmt -R$range -J$projection -Wthin,red -K -O >> $output1
gmt psxy ../../../Misc/Mapping_Resources/trench.gmt -R$range -J$projection -Wthin,red -Sf1.5/0.6+r+t+o1.8 -K -O >> $output1

# Add PBO velocity vectors
awk '{print $1, $2, $3, $4, $7, $8, $10}' $infile | gmt psvelo -R$range -J$projection -O -K -Se$horiz_scale/0.68/8 -A+e+gblack+pthickest -Wthinnest,black >> $output1
gmt psvelo -R$range -J$projection -A+e+gblack+pthickest -Se$horiz_scale/0.68/10 -Wthinnest,black -K -O <<EOF >> $output1
-125.2 41.8 2 0 0.2 0.2 0.0 2+-0.2mm/yr
EOF

grep 'nan' $infile | awk '{print $1, $2}' | gmt psxy -R$range -J$projection -O -K -Gdarkblue -Sc0.05 >> $output1

gmt pstext -R$range -J$projection -F+f18p,Helvetica -Gwhite -K -O <<EOF >> $output1
-119.5 41.8 $name3
-124 41.8 C
EOF



rm gmt.history
rm etopo1.grad
rm etopo1.hist
rm etopo1.norm

open $output1
