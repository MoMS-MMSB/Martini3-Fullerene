#!/bin/bash
val=$(tail -n 1 solid/run.gro | awk '{print $1}')
echo "scale = 2; $val/4" | bc -l > lattice.txt
