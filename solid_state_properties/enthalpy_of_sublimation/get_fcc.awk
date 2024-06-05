awk -v command='basename $0' -v nx=$1 -v ny=$2 -v nz=$3 -v a=$4 'BEGIN{

print "\n type: ./get_fcc 3 3 3 1.1"
print "4 numbers are required after the program name"
print "the first three are the number of molecules to put in the crystal,"
print "the last is the lattice constant.\n"
print "You also need a file named \"input.gro\" with the coordinates "
print "to be repeated and placed in the FCC crystal.\n\n"

# Input parameters: numbers of unit cells in x,y,z (nx,ny,nz)
#  and the lattice constant a

# Backup the previously made structure
system("mv fcc_lattice.gro old_fcc_lattice.gro")

# Offset for the atom positions, makes visualization with PBC nicer
ofs = 0.25*a

nz2 = int(nz/2)


##### Define crystal unit cell here ##################################

# Unit cell vectors for FCC:
pvx[1] = 0.0 ; pvy[1] = 0.0 ; pvz[1] = 0.0
pvx[2] = 0.0 ; pvy[2] = 0.5*a ; pvz[2] = 0.5*a 
pvx[3] = 0.5*a ; pvy[3] = 0.0 ; pvz[3] = 0.5*a
pvx[4] = 0.5*a ; pvy[4] = 0.5*a ; pvz[4] = 0.0

# Number of molecules in a unit cell
natcr = 4


##### Read in single molecule coordinates (gro format) ###############

getline < "input.gro"
getline < "input.gro"
nf = $1
printf ("nf = %d\n",nf)

for(i=1;i<=nf;i++){
	getline < "input.gro"
	x[i] = $4; y[i] = $5; z[i] = $6
	cmx = cmx + $4; cmy = cmy + $5; cmz = cmz + $6
#####	printf("%8.3f\n",x[i])
}
cmx = cmx/nf; cmy = cmy/nf; cmz = cmz/nf

# Set the molecule to origin
for(i=1;i<=nf;i++){
	x0[i] = x[i]-cmx
	y0[i] = y[i]-cmy
	z0[i] = z[i]-cmz
}


##### Make the crystal ###############################################

# Total number of atoms
ntot = nx*ny*nz*natcr*nf
printf("ntot = %d\n\n",ntot)

print "FCC lattice of fullerenes" > "fcc_lattice.gro"
printf("%6d\n",ntot) >> "fcc_lattice.gro"

for(i=1;i<=nx;i++){  
  for(j=1;j<=ny;j++){
    for(k=1;k<=nz;k++){

      for(tt=1;tt<=4;tt++){

        nmol++
  	mol = "F15"		

# Possibility to add some special type of molecule, not used at present
#        if(i == 1 && j == 1 && k == nz && tt == 4) mol = "VFUL"

	for(cc=1;cc<=nf;cc++){

	      at++
      	      name ="C"cc	
		
	      xn[cc] = x0[cc]+(i-1)*a+pvx[tt]+ofs	
	      yn[cc] = y0[cc]+(j-1)*a+pvy[tt]+ofs	
	      zn[cc] = z0[cc]+(k-1)*a+pvz[tt]+ofs	
		
printf("%5d%5-s%5s%5d%8.3f%8.3f%8.3f\n",nmol,mol,name,at,xn[cc],yn[cc],zn[cc]) >> "fcc_lattice.gro"
	
	}
      } 
  } 
 }
}

boxx = nx*a; boxy = ny*a; boxz = nz*a

printf("%10.5f%10.5f%10.5f\n",boxx,boxy,boxz) >> "fcc_lattice.gro"

print "Done!!\n\n"

}'

