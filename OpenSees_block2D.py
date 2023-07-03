# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:02:11 2023

@author: User
"""
from openseespy.opensees import *
import opsvis as ops
import matplotlib.pyplot as plt

g = 9.81 ;# m/s2
LCol = 0.3
LBeam = 0.2
Weight = 196.2 ;# MPa
HCol = 0.1
BCol = 0.1
HBeam = 0.1
BBeam = 0.1
#---------------------- calculated parameters ------------------------------------------
PCol = Weight/2 ; 		# nodal dead-load weight per column
Mass = PCol/g ;		# nodal mass = 20 
MCol = 1./12.*(Weight/LBeam)*(LBeam*LBeam);	# beam-end moment due to distributed load.
# calculated geometry parameters
ACol = BCol * HCol;					# cross-sectional area
ABeam = BBeam * HBeam;
IzCol = (1./12.)* BCol*(HCol*HCol*HCol); 			# Column moment of inertia
IzBeam =  (1./12.)*BBeam*(HBeam*HBeam*HBeam); 		

wipe()
model('basic', '-ndm', 2, '-ndf' , 3)
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

eleArgs = [1,'PlaneStrain',2000]
# points = [1,0.0, 0,
#           2,0.1, 0,
#           3,0.1, 10.0,
#           4,0.0, 10.0]

points = [1,0.0, 0,
          2,10, 0,
          3,10, 10.0,
          4,0.0, 10.0]
block2D(nx, ny, e1, n1, 'quad', *eleArgs, *points) 

b = 10.0/100.0
n = 100
for k in range(1,n+1):
    equalDOF((2*k+1), (2*k+2), 1,2)    

#-------------- Recorder --------------------------------
# recorder('Node', '-file', 'node_disp1.out', '-time', '-node',1, '-dof', 1,2,3 ,'disp')

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
# pattern('Plain',703, 702)
# load(1, 0, 1)
# load(2, 0, 1) 

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# system("UmfPack")
# numberer("RCM")
# constraints("Transformation")
# integrator("Newmark", 0.5, 0.25)
# algorithm("Newton")
# test('EnergyIncr',1e-8, 200)
# analysis("Transient")
# analyze(8000,1e-4)
# print("finish analyze:0 ~ 0.8s")


ops.plot_model()
plt.show()

