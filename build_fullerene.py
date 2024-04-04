from numpy import cos, sin, pi, sqrt
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-np", "--points", type = int, help = "number of beads")
parser.add_argument("-b", "--bead", type = str, help = "bead type")
parser.add_argument("-r", "--radius", type = float, help = "radius of sphere")
parser.add_argument("-n", "--name", type = str, help = "name")

args = parser.parse_args()

no_of_points = args.points       # Define here the number of points
bead_type = args.bead
radius_of_sphere = args.radius  # Define here the radius of the sphere (in angstroms!)
name      = args.name
def GetPointsEquiAngularlyDistancedOnSphere(numberOfPoints):
    """ each point you get will be of form 'x, y, z'; in cartesian coordinates
        eg. the 'l2 distance' from the origion [0., 0., 0.] for each point will be 1.0 
        ------------
        converted from:  
        http://web.archive.org/web/20120421191837/http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere ) 
    """
    dlong = pi*(3.0-sqrt(5.0))  # ~2.39996323 
    dz   =  2.0/numberOfPoints
    long =  0.0
    z    =  1.0 - dz/2.0
    ptsOnSphere =[]
    for k in range( 0, numberOfPoints): 
        r    = sqrt(1.0-z*z)
        ptNew = (cos(long)*r, sin(long)*r, z)
        ptsOnSphere.append( ptNew )
        z    = z - dz
        long = long + dlong
    return ptsOnSphere

if __name__ == '__main__':                
    ptsOnSphere = GetPointsEquiAngularlyDistancedOnSphere( no_of_points)

    #toggle True/False to print them
    if( False ):    
        for pt in ptsOnSphere:  print( "bead coordinates: " + str(pt))

    #toggle True/False to plot them
    if(True):
        from numpy import *
        

        x_s=[];y_s=[]; z_s=[]

        for pt in ptsOnSphere:
            x_s.append( pt[0]*radius_of_sphere); 
            y_s.append( pt[1]*radius_of_sphere); 
            z_s.append( pt[2]*radius_of_sphere)
x_s_array = np.asarray(x_s)
y_s_array = np.asarray(y_s)
z_s_array = np.asarray(z_s)

# make superarray
xyz_s_array = np.asarray((x_s_array,y_s_array,z_s_array))

# transpose it
xyz_s_array_transposed = np.matrix.transpose(xyz_s_array)
with open('fullerene.itp', 'w') as itpout:
    itpout.write(";                                                                     " + '\n')
    itpout.write("; MARTINI C60 fullerene model                                         " + '\n')
    itpout.write("; Described by " + str(no_of_points) + " " + str(bead_type) + " beads, and with a radius of " + str(radius_of_sphere*0.1) + " nm." + '\n')
    itpout.write("; Topology generated by build-CG-fullerene.ipynb                      " + '\n')
    itpout.write(";                                                                     " + '\n')
    itpout.write("                                                                      " + '\n')
    itpout.write("[ moleculetype ]                                                      " + '\n')
    itpout.write("; Name            nrexcl                                              " + '\n')
    itpout.write(str(name) + "         1                                                " + '\n')
    itpout.write("                                                                      " + '\n')
    itpout.write("[ atoms ]                                                             " + '\n')
    itpout.write(";   nr   type  resnr  residue  atom   cgnr   charge   mass            " + '\n')
    #
    # atoms
    for i in range(1, no_of_points+1):
        itpout.write('{:>6} {:>6} {:>5} {:>7} {:>5}{:0=2d} {:>5} {:>9.3f} {:>6} \n'
                      .format(str(i), str(bead_type), str(1), str(name),
                              str("C"), i, 
                              str(i), 0, str("")))
    #
    itpout.write("                                                                      " + '\n')
    #
    # bonds
    itpout.write("[ bonds ]" + "\n")
    itpout.write(";    i      j     funct  length  force_k" + '\n')
    for i in range(1, no_of_points):
        for j in range(i+1, no_of_points+1):
            itpout.write('{:>6} {:>6} {:>7} {:>9.3f} {:>7} \n'
                          .format(str(i), 
                                  str(j), 
                                  str(1),
                                  round(np.linalg.norm(xyz_s_array_transposed[i-1]-xyz_s_array_transposed[j-1])*0.1,3),
                                  str(1250)))
    #
    print("ITP file generated. Check the current folder!")

with open('new_fulle.pdb', 'w') as pdbout:
    pdbout.write('{:6s}   {:40s} \n'
                 .format("HEADER","  PDB generated by build-CG-fullerene.ipynb"))
    for i in range(1, no_of_points+1):
        i_name = ('{:>0}{:0=2d}'.format(str("C"),i)) # create atom label (does not work for i > 99..!)
        pdbout.write('{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f} \n'
                     .format("ATOM", i, i_name, "", name, "", 1, "", 
                             xyz_s_array_transposed[i-1][0],
                             xyz_s_array_transposed[i-1][1],
                             xyz_s_array_transposed[i-1][2],))
    #
    pdbout.write("END")
    print("PDB file generated. Check the current folder!")
with open('new_fulle.gro', 'w') as groout:
    groout.write('GRO generated by build-CG-fullerene.ipynb \n')
    groout.write(str(no_of_points) + '\n')
    for i in range(1, no_of_points+1):
        i_name = ('{:>0}{:0=2d}'.format(str("C"),i)) # create atom label (does not work for i > 99..!)
        groout.write('{:5d}{:5s}{:>5s}{:5d}{:8.3f}{:8.3f}{:8.3f}\n'
                     .format(1, name, i_name, i, 
                             xyz_s_array_transposed[i-1][0]*0.1,
                             xyz_s_array_transposed[i-1][1]*0.1,
                             xyz_s_array_transposed[i-1][2]*0.1,))
    #
    groout.write('{:10.5f}{:10.5f}{:10.5f}'.format(0,0,0))
    print("GRO file generated. Check the current folder!")
#os.system('cp new_fulle.gro input.gro')
#os.system('bash get_fcc.awk 4 4 4 1.417')