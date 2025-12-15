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

# Case
cases = ['ke','ke_sources','kefp','kefp_sources']
results = []
for i in range(len(cases)):
    case = cases[i]
    itc = extract_number_of_iterations('%s/log.simpleFoam'%(case))
    uc = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%(case,itc))
    kc = np.genfromtxt('%s/postProcessing/surfaces/%d/k_zNormal.raw'%(case,itc))
    lc = np.genfromtxt('%s/postProcessing/lines/%d/xlineCenter_epsilon_k_nut_p_U.xy'%(case,itc))
    sc = np.genfromtxt('%s/postProcessing/lines/%d/ylineSpanwise10D_epsilon_k_nut_p_U.xy'%(case,itc))
    resi = {'Xc': uc[:,0],'Yc': uc[:,1], 'itc': itc, 'uc': uc, 'kc': kc, 'lc': lc, 'sc': sc}
    results.append(resi)
labels = [r'$k$-$\varepsilon$',
          r'$k$-$\varepsilon$ + sources',
          r'$k$-$\varepsilon$-$f_p$',
          r'$k$-$\varepsilon$-$f_p$ + sources']
stys = ['b-',
        'c--',
        'r-',
        'm--']


#######################################################################
########## Centerline plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(centerline_TI20[:,0],centerline_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
for i in range(len(cases)):
    lc = results[i]['lc']
    plt.plot(lc[:,0]/D,lc[:,5]/Uref,stys[i],label=labels[i])
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-5,25])
plt.ylim([0.65,1.0])
plt.legend(loc='lower right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_U.png',bbox_inches='tight')


# TKE
fig = plt.figure()
for i in range(len(cases)):
    lc = results[i]['lc']
    plt.plot(lc[:,0]/D,lc[:,2],stys[i],label=labels[i])
plt.xlabel(r'$x/D$')
plt.ylabel(r'$k$ $\left[\frac{\text{m}^2}{\text{s}^2}\right]$',**yd)
plt.xlim([-5,25])
plt.legend(loc='center right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_TKE.png',bbox_inches='tight')

# nut
fig = plt.figure()
for i in range(len(cases)):
    lc = results[i]['lc']
    plt.plot(lc[:,0]/D,lc[:,3],stys[i],label=labels[i])
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\nu_t$ $\left[\frac{\text{m}^2}{\text{s}}\right]$',**yd)
plt.xlim([-5,25])
plt.legend(loc='center right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_nut.png',bbox_inches='tight')


#######################################################################
########## Spanwise x=10D plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(spanwise10D_TI20[:,0],spanwise10D_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
for i in range(len(cases)):
    sc = results[i]['sc']
    plt.plot(sc[:,0]/D,sc[:,5]/Uref,stys[i],label=labels[i])
plt.xlabel(r'$y/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-15,15])
plt.ylim([0.87,1.01])
plt.legend(loc='lower right',fontsize=17)
plt.title('At $x/D = 10$')
plt.savefig('spanwise10D_U.png',bbox_inches='tight')


#######################################################################
########## U CONTOUR ############################################################
#######################################################################
def mmake_contour():
    fig, ax = plt.subplots(len(labels), 1, sharex=True, sharey=True, figsize=(8, 10))
    ax = ax.flatten()
    plt.subplots_adjust(hspace=0.1)
    
    for i in range(len(labels)):
        ax[i].axis('scaled')
        ax[i].text(0.03, 0.9, labels[i], transform=ax[i].transAxes, fontsize=12,
                   verticalalignment='top', horizontalalignment='left', 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.75))
        ax[i].set_ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
    
    ax[-1].set_xlabel('$x/D$')
    ax[0].set_xlim(-2.5,25)
    ax[0].set_ylim(-5,5)
    return fig, ax

# U combined
fig, ax = mmake_contour()
fig.subplots_adjust(right=0.8)
for i in range(len(labels)):
    casei = results[i]
    Xc = casei['Xc']
    Yc = casei['Yc']
    Uc = casei['uc'][:,3]
    p = ax[i].tricontourf(Xc/D, Yc/D, Uc/Uref, np.arange(0.65, 1.1, 0.05), cmap=cm.jet)
cbar = fig.add_axes([0.85, 0.15, 0.03, 0.7])
comcolRANS = plt.colorbar(p, cax=cbar)
cbar.set_ylabel(r'$\dfrac{U}{U_\infty}$',rotation=0,va='center',ha='left')
fig.savefig('U_contours.png',bbox_inches='tight')

# TKE combined
fig, ax = mmake_contour()
fig.subplots_adjust(right=0.8)
for i in range(len(labels)):
    casei = results[i]
    Xc = casei['Xc']
    Yc = casei['Yc']
    kc = casei['kc'][:,3]
    p = ax[i].tricontourf(Xc/D, Yc/D, kc, np.arange(0.0, 7.5, 0.2), cmap=cm.jet)
cbar = fig.add_axes([0.85, 0.15, 0.03, 0.7])
comcolRANS = plt.colorbar(p, cax=cbar)
cbar.set_ylabel(r'$k$ $\left[\frac{\text{m}^2}{\text{s}^2}\right]$',rotation=0,va='center',ha='left')
fig.savefig('TKE_contours.png',bbox_inches='tight')

# TI combined
fig, ax = mmake_contour()
fig.subplots_adjust(right=0.8)
for i in range(len(labels)):
    casei = results[i]
    Xc = casei['Xc']
    Yc = casei['Yc']
    kc = casei['kc'][:,3]
    Uc = casei['uc'][:,3]
    p = ax[i].tricontourf(Xc/D, Yc/D, np.sqrt(2/3*kc)/Uc*100, np.arange(4.5, 31.0, 1.0), cmap=cm.jet)
cbar = fig.add_axes([0.85, 0.15, 0.03, 0.7])
comcolRANS = plt.colorbar(p, cax=cbar)
cbar.set_ylabel(r'$I$ [%]',rotation=0,va='center',ha='left')
fig.savefig('TI_contours.png',bbox_inches='tight')

