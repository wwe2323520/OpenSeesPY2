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

node(1, 0, 0)
node(2, LBeam, 0)
node(3, 0, LCol)
node(4, LBeam, LCol)

# nDMaterial('ElasticIsotropic', 2000, E, nu, rho)
fix(1, 1, 1, 0)
fix(2, 1, 1, 0)
fix(3, 0, 0, 0)
fix(4, 0, 0, 0)

mass(3, Mass, 0.0,  0.0)
mass(4, Mass, 0.0,  0.0)

ColTransfTag = 1; 			# associate a tag to column transformation
BeamTransfTag = 2; 			# associate a tag to beam transformation (good practice to keep col and beam separate)
ColTransfType = 'Linear' ;			# options, Linear PDelta Corotational 
geomTransf(ColTransfType, ColTransfTag) ; 	# only columns can have PDelta effects (gravity effects)
geomTransf('Linear', BeamTransfTag)  ; 	

# Define ELEMENTS -------------------------------------------------------------
# Material parameters (1 ksi = 6.89 MPa)/ 

fc  = 25; 		# CONCRETE Compressive Strength (+Tension, -Compression)
Ec =  4700*((fc)**(1/2)); 	# Concrete Elastic Modulus
print(Ec)

element('elasticBeamColumn',1, 1, 3, ACol, Ec, IzCol, ColTransfTag)
element('elasticBeamColumn',2, 2, 4, ACol, Ec, IzCol, ColTransfTag)
element('elasticBeamColumn',3, 3, 4, ABeam, Ec, IzBeam, BeamTransfTag)
#-------------- Recorder --------------------------------
# recorder('Node', '-file', 'node_disp1.out', '-time', '-node',1, '-dof', 1,2,3 ,'disp')
recorder('Node', '-file', 'DFree.out', '-time', '-node',3,4, '-dof', 1,2,3 ,'disp')
recorder('Node', '-file', 'DBase.out', '-time', '-node',1,2, '-dof', 1,2,3 ,'disp')
#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
# pattern('Plain',703, 702)
# load(1, 0, 1)
# load(2, 0, 1) 
WzBeam = Weight/LBeam

timeSeries('Linear', 1)
pattern('Plain', 1, 1)
eleLoad('-ele',3,'-type','-beamUniform',-WzBeam)
print("finish Input Force File:0 ~ 0.1s(+1), Input Stress B.C:0.2~0.3s(-1)")


NstepGravity = 10
DGravity = 1./NstepGravity
system("BandGeneral")
numberer("Plain")
constraints("Plain")
integrator("LoadControl", DGravity)
algorithm("Newton")
test('NormDispIncr',1e-8, 6)
analysis("Static")
analyze(NstepGravity)
print("finish analyze:0 ~ 0.8s")

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
# ops.plot_loads_2d() # watch loads
# ops.section_force_diagram_2d("M", sfac = 5e-5) # 'V'/'M' watch shearforce/ Moment
# ops.plot_defo()   # watch deformation
plt.show()

