import numpy as np
import xarray
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import cm

mpl.style.use('classic')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams["legend.scatterpoints"] = 1
plt.rcParams["legend.numpoints"] = 1
plt.rcParams['grid.linestyle'] = ':' # Dotted gridlines
mpl.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = 17
plt.rcParams['axes.grid']=True
yd = dict(rotation=0,ha='right',va='center')
plt.close('all')

#######################################################################
########### PARAMETERS ########################
#######################################################################
D = 80.0
Uref = 8.0
zh = 70.0

#######################################################################
################## REFERENCE DATA ###################
#######################################################################
refdata = xarray.open_dataset('baungaard2022_ke_zeli_hubheight.nc')
X, Y = np.meshgrid(refdata.x, refdata.y)


#######################################################################
#### Load plane data #################################################
#######################################################################
def extract_number_of_iterations(filename):
    iterations = None
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('Time = '):
                parts = line.split()
                try:
                    iterations = float(parts[2])
                except (IndexError, ValueError):
                    pass
    return int(iterations)


# Calaf AD case
itc = extract_number_of_iterations('%s/log.simpleFoam'%('calaf'))
pc = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%('calaf',itc))

# Fixed AD case
itf = extract_number_of_iterations('%s/log.simpleFoam'%('fixed'))
pf = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%('fixed',itf))



#######################################################################
########## U CONTOUR ############################################################
#######################################################################
labels = ['Reference','calaf', 'fixed']

reduce = 1.3
fig, ax = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(5*reduce, 3*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.3)

p = ax[0].contourf(X/D, Y/D, refdata['U'].T/Uref, np.linspace(0.5, 1.05, 12), cmap=cm.jet)
p = ax[1].tricontourf(pc[:,0]/D, pc[:,1]/D, pc[:,3]/Uref, np.linspace(0.5, 1.05, 12), cmap=cm.jet)
p = ax[2].tricontourf(pf[:,0]/D, pf[:,1]/D, pf[:,3]/Uref, np.linspace(0.5, 1.05, 12), cmap=cm.jet)


for i in range(3):
    ax[i].text(0.03, 0.9, labels[i], transform=ax[i].transAxes, fontsize=12,
               verticalalignment='top', horizontalalignment='left', 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.75))
    ax[i].axis('scaled')
    
fig.subplots_adjust(right=0.9)
cbar = fig.add_axes([0.85, 0.1, 0.03, 0.8])
comcolRANS = plt.colorbar(p, cax=cbar)
cbar.set_ylabel(r'$\dfrac{U}{U_\infty}$',rotation=0,va='center',ha='left')
ax[0].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
ax[1].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
ax[0].set_xlim(-2,10)
ax[0].set_ylim(-1.5,1.5)
ax[0].set_yticks([-1,0,1])
ax[2].set_xlabel('$x/D$')
ax[2].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
fig.savefig('U_contour.png',bbox_inches='tight',dpi=300)




