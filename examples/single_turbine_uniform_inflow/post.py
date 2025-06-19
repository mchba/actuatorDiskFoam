import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.style.use('classic')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams["legend.scatterpoints"] = 1
plt.rcParams["legend.numpoints"] = 1
plt.rcParams['grid.linestyle'] = ':' # Dotted gridlines
mpl.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = 17
plt.rcParams['axes.grid']=True
mpl.rcParams['axes.formatter.useoffset'] = False
yd = dict(rotation=0,ha='right',va='center')
plt.close('all')

#######################################################################
########### PARAMETERS ########################
#######################################################################
D = 40.0
Uref = 10.0
zh = 70.0

#######################################################################
################## REFERENCE DATA ###################
#######################################################################
centerline_TI20 = np.genfromtxt('fei2025/centerline_TI20.csv',delimiter=',')
spanwise10D_TI20 = np.genfromtxt('fei2025/spanwise10D_TI20.csv',delimiter=',')



#######################################################################
#### Load line plane data #################################################
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


# Decaying turbulence inflow
itc = extract_number_of_iterations('%s/log.simpleFoam'%('decaying_turbulence'))
lc = np.genfromtxt('%s/postProcessing/lines/%d/xlineCenter_epsilon_k_nut_p_U.xy'%('decaying_turbulence',itc))
sc = np.genfromtxt('%s/postProcessing/lines/%d/ylineSpanwise10D_epsilon_k_nut_p_U.xy'%('decaying_turbulence',itc))
uc = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%('decaying_turbulence',itc))
kc = np.genfromtxt('%s/postProcessing/surfaces/%d/k_zNormal.raw'%('decaying_turbulence',itc))






#######################################################################
########## Centerline plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(centerline_TI20[:,0],centerline_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
plt.plot(lc[:,0]/D,lc[:,5]/Uref,label='actuatorDiskFoam')
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-5,25])
plt.ylim([0.7,1.0])
plt.legend(loc='lower right',fontsize=17)
plt.savefig('centerline_U.png',bbox_inches='tight')


#######################################################################
########## Spanwise x=10D plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(spanwise10D_TI20[:,0],spanwise10D_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
plt.plot(sc[:,0]/D,sc[:,5]/Uref,label='actuatorDiskFoam')
plt.xlabel(r'$y/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-15,15])
plt.ylim([0.94,1.01])
plt.legend(loc='lower right',fontsize=17)
plt.savefig('spanwise10D_U.png',bbox_inches='tight')

#######################################################################
########## U CONTOUR ############################################################
#######################################################################
def make_contour(X,Y,VAR,lvls,varname):
    fig = plt.figure()
    p = plt.tricontourf(X, Y, VAR, lvls, cmap=cm.jet)
    plt.ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
    plt.xlabel('$x/D$')
    divider = make_axes_locatable(fig.gca())
    cax = divider.append_axes("right", size="4%", pad=0.1)
    plt.colorbar(p, cax=cax)
    cax.set_ylabel(varname,rotation=0,va='center',ha='left')
    return fig

# U
fig = make_contour(uc[:,0]/D,uc[:,1]/Uref,uc[:,3]/Uref,np.arange(0.65, 1.1, 0.05),r'$\dfrac{U}{U_\infty}$')
fig.savefig('U_contour.png',bbox_inches='tight',dpi=300)

# TKE
fig = make_contour(kc[:,0]/D,kc[:,1]/Uref,kc[:,3],np.arange(0.0, 6.0, 0.2),r'$k$ [m2/s2]')
fig.savefig('TKE_contour.png',bbox_inches='tight',dpi=300)

# TI
fig = make_contour(kc[:,0]/D,kc[:,1]/Uref,np.sqrt(2/3*kc[:,3])/uc[:,3]*100,np.arange(0.0, 26.0, 1.0),r'$I$ [%]')
fig.savefig('TI_contour.png',bbox_inches='tight',dpi=300)



