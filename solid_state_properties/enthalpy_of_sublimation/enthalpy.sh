#!/bin/bash
echo "Potential" | gmx energy -f solid/run.edr -o solid.xvg
gmx analyze -f solid.xvg -ac -ee solid_est.xvg 
s_w=$(grep "\"av" solid_est.xvg | awk {'print $NF}' | sed 's/\"//g')
S_U=$(echo "scale = 2; $s_w/256" | bc -l)
echo "Potential" | gmx energy -f vapor/run.edr -o gas.xvg
gmx analyze -f gas.xvg -ac -ee gas_est.xvg 
g_w=$(grep "\"av" gas_est.xvg | awk {'print $NF}' | sed 's/\"//g')
G_U=$(echo "scale = 2; $g_w" | bc -l)
echo "scale = 2; $G_U - $S_U + 2.5" | bc -l > enthalpy.txt
