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
refdata = xarray.open_dataset('baungaard2022_kefp_hubheight.nc')
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


# Case
cases = ['4cD','8cD','8cD_linUp']
results = []
for i in range(len(cases)):
    case = cases[i]
    itc = extract_number_of_iterations('%s/log.simpleFoam'%(case))
    uc = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%(case,itc))
    kc = np.genfromtxt('%s/postProcessing/surfaces/%d/k_zNormal.raw'%(case,itc))
    lc = np.genfromtxt('%s/postProcessing/lines/%d/xlineCenter_epsilon_k_nut_p_U.xy'%(case,itc))
    resi = {'Xc': uc[:,0],'Yc': uc[:,1], 'itc': itc, 'uc': uc, 'kc': kc, 'lc': lc}
    results.append(resi)
labels = ['EllipSys3D',
          'OpenFoam ($D/4$)',
          'OpenFoam ($D/8$)',
          'OpenFoam ($D/8$, linUp)']

#######################################################################
########## U CONTOUR ############################################################
#######################################################################


def make_contour(VARREF,VAR,varname,lvls):
    fig, ax = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 4))
    ax = ax.flatten()
    plt.subplots_adjust(hspace=0.1)
    
    p = ax[0].contourf(X/D, Y/D, VARREF, lvls, cmap=cm.jet)
    p = ax[1].tricontourf(Xc/D, Yc/D, VAR, lvls, cmap=cm.jet)
    
    
    for i in range(2):
        ax[i].axis('scaled')
    
    # EllipSys
    ax[0].text(0.03, 0.9, labels[0], transform=ax[0].transAxes, fontsize=12,
               verticalalignment='top', horizontalalignment='left', 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.75))
    ax[1].text(0.03, 0.9, labels[2], transform=ax[1].transAxes, fontsize=12,
               verticalalignment='top', horizontalalignment='left', 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.75))
    
    fig.subplots_adjust(right=0.8)
    cbar = fig.add_axes([0.85, 0.15, 0.03, 0.7])
    comcolRANS = plt.colorbar(p, cax=cbar)
    cbar.set_ylabel(varname,rotation=0,va='center',ha='left')
    ax[0].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
    ax[1].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
    ax[0].set_xlim(-2,10)
    ax[0].set_ylim(-1.5,1.5)
    ax[0].set_yticks([-1,0,1])
    ax[1].set_xlabel('$x/D$')
    return fig

res0 = results[1]
Xc = res0['Xc']; Yc = res0['Yc'] 
fig = make_contour(refdata['U'].T/Uref, res0['uc'][:,3]/Uref, r'$\dfrac{U}{U_\infty}$', np.linspace(0.5, 1.05, 12))
fig.savefig('U_contour.png',bbox_inches='tight',dpi=300)
make_contour(refdata['tke'].T, res0['kc'][:,3], r'$k$ [m2/s2]', np.linspace(0.0, 2, 12))


#######################################################################
########## Centerline plot ############################################################
#######################################################################
refsty = {'marker':'o','linestyle':'None','mfc':'None', 'mew':1, 'markersize':6}

figx = 8; figy = 4
# U
fig = plt.figure(figsize=(figx,figy))
plt.plot(refdata.x/D,refdata.interp(y=0).U/Uref,label=labels[0],**refsty)
for i in range(len(cases)):
    lc = results[i]['lc']
    plt.plot(lc[:,0]/D,lc[:,5]/Uref,label=labels[i+1])
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-5,15])
plt.ylim([0.5,1.0])
plt.legend(loc='lower right',fontsize=13)
plt.title('At centerline')
plt.savefig('centerline_U.png',bbox_inches='tight')


# TKE
fig = plt.figure(figsize=(figx,figy))
plt.plot(refdata.x/D,refdata.interp(y=0).tke,label=labels[0],**refsty)
for i in range(len(cases)):
    lc = results[i]['lc']
    plt.plot(lc[:,0]/D,lc[:,2],label=labels[i+1])
plt.xlabel(r'$x/D$')
plt.ylabel(r'$k$ $\left[\frac{\text{m}^2}{\text{s}^2}\right]$',**yd)
plt.xlim([-5,15])
plt.legend(loc='upper left',fontsize=13)
plt.title('At centerline')
plt.savefig('centerline_TKE.png',bbox_inches='tight')

