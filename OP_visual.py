# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:07:45 2023

@author: User
"""

from openseespy.opensees import *
import opsvis as ops
import matplotlib.pyplot as plt

wipe()
model('basic', '-ndm', 2, '-ndf' , 2)

b = 10.0/100.0
n = 100

for i in range(n+1):
    node((2*i+1), 0, (i*b))
    node((2*i+2), b, (i*b)) 

E = 15005714.286
nu = 0.3
rho = 2020
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)
#--------------- B.C --------------------------------
# fix(1, 1, 0)
# fix(2, 1, 0)
for k in range(1,n+1):
    equalDOF((2*k+1), (2*k+2), 1,2)    
#--------------- quad element --------------------------
for j in range(n):
    element('quad', (j+1) , (2*j+1), (2*j+2), (2*j+4), (2*j+3), 1,'PlaneStrain',2000)
    
#==================== Beam element ============================
model('basic', '-ndm', 2, '-ndf' , 3)
node(203,0.0, 0.0)
node(204,0.1, 0.0)

#------------------- B.C (Beam) --------------------------
fix(203, 0, 0, 1)
fix(204, 0, 0, 1)

#------------------ Build Beam --------------------------
A = 0.1*1
E1 = 1E05
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)
element('elasticBeamColumn',105, 203,204, A, E1, Iz, 1)

equalDOF(203,1, 1,2)
equalDOF(204,2, 1,2)
#-------------- Recorder --------------------------------
recorder('Node', '-file', 'node_disp1.out', '-time', '-node',1, '-dof', 1,2,3 ,'disp')
   
#------------- Load Pattern ----------------------------
timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
# timeSeries('Linear',702)

pattern('Plain',703, 702)
eleLoad('-ele', 105, '-type','-beamUniform',20,0)
# load(1, 0, 1)
# load(2, 0, 1) 
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(8000,1e-4)
print("finish analyze:0 ~ 0.8s")

#================== Show model shape ===================
ops.plot_model()
ops.plot_loads_2d()  #;show pattern plain draft
# ops.plot_defo()  # show the deformation
# ops.section_force_diagram_2d("N",sfac= 5e-5)
# ops.plot_stress_2d()
# plt.grid()

plt.axis('equal')
ops.plot_loads_2d()
ops.plot_defo()
plt.axis('equal')
sig_out = opsv.sig_out_per_node()
j, jstr = 1, 'syy'
nds_val = sig_out[:, j]

plt.figure()
ops.plot_loads_2d(nds_val)
plt.show()