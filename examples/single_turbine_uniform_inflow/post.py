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


# Decaying turbulence inflow
case = 'decaying_turbulence'
itc = extract_number_of_iterations('%s/log.simpleFoam'%(case))
lc = np.genfromtxt('%s/postProcessing/lines/%d/xlineCenter_epsilon_k_nut_p_U.xy'%(case,itc))
sc = np.genfromtxt('%s/postProcessing/lines/%d/ylineSpanwise10D_epsilon_k_nut_p_U.xy'%(case,itc))
uc = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%(case,itc))
kc = np.genfromtxt('%s/postProcessing/surfaces/%d/k_zNormal.raw'%(case,itc))

# Non-decaying turbulence inflow
case = 'nondecaying_turbulence'
itn = extract_number_of_iterations('%s/log.simpleFoam'%(case))
ln = np.genfromtxt('%s/postProcessing/lines/%d/xlineCenter_epsilon_k_nut_p_U.xy'%(case,itn))
sn = np.genfromtxt('%s/postProcessing/lines/%d/ylineSpanwise10D_epsilon_k_nut_p_U.xy'%(case,itn))
un = np.genfromtxt('%s/postProcessing/surfaces/%d/U_zNormal.raw'%(case,itn))
kn = np.genfromtxt('%s/postProcessing/surfaces/%d/k_zNormal.raw'%(case,itn))






#######################################################################
########## Centerline plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(centerline_TI20[:,0],centerline_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
plt.plot(lc[:,0]/D,lc[:,5]/Uref,label='Decaying')
plt.plot(ln[:,0]/D,ln[:,5]/Uref,label='Non-decaying')
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-5,25])
plt.ylim([0.7,1.0])
plt.legend(loc='lower right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_U.png',bbox_inches='tight')

# TKE
fig = plt.figure()
plt.plot(lc[:,0]/D,lc[:,2],label='Decaying')
plt.plot(ln[:,0]/D,ln[:,2],label='Non-decaying')
plt.xlabel(r'$x/D$')
plt.ylabel(r'$k$ $\left[\frac{\text{m}^2}{\text{s}^2}\right]$',**yd)
plt.xlim([-5,25])
plt.legend(loc='lower right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_TKE.png',bbox_inches='tight')

# nut
fig = plt.figure()
plt.plot(lc[:,0]/D,lc[:,3],label='Decaying')
plt.plot(ln[:,0]/D,ln[:,3],label='Non-decaying')
plt.xlabel(r'$x/D$')
plt.ylabel(r'$\nu_t$ $\left[\frac{\text{m}^2}{\text{s}}\right]$',**yd)
plt.xlim([-5,25])
plt.legend(loc='upper right',fontsize=17)
plt.title('At centerline')
plt.savefig('centerline_nut.png',bbox_inches='tight')

#######################################################################
########## Spanwise x=10D plot ############################################################
#######################################################################
# U
fig = plt.figure()
plt.plot(spanwise10D_TI20[:,0],spanwise10D_TI20[:,1],'ko', mfc='White', mew=1, markersize=6,label='Fei et al. (2025)')
plt.plot(sc[:,0]/D,sc[:,5]/Uref,label='Decaying')
plt.plot(sn[:,0]/D,sn[:,5]/Uref,label='Non-decaying')
plt.xlabel(r'$y/D$')
plt.ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
plt.xlim([-15,15])
plt.ylim([0.94,1.01])
plt.legend(loc='lower right',fontsize=17)
plt.title('At $x/D = 10$')
plt.savefig('spanwise10D_U.png',bbox_inches='tight')

#######################################################################
########## U CONTOUR ############################################################
#######################################################################
def make_contour(X,Y,VAR,lvls,varname,savename):
    fig = plt.figure()
    p = plt.tricontourf(X, Y, VAR, lvls, cmap=cm.jet)
    plt.ylabel('$\dfrac{y}{D}$',rotation=0,va='center',ha='right')
    plt.xlabel('$x/D$')
    divider = make_axes_locatable(fig.gca())
    cax = divider.append_axes("right", size="4%", pad=0.1)
    plt.colorbar(p, cax=cax)
    cax.set_ylabel(varname,rotation=0,va='center',ha='left')
    fig.savefig(savename,bbox_inches='tight',dpi=300)
    return fig

##### Decaying turbulence ########
# U
fig = make_contour(uc[:,0]/D,uc[:,1]/D,uc[:,3]/Uref,np.arange(0.65, 1.1, 0.05),r'$\dfrac{U}{U_\infty}$','U_contour_decay.png')
# TKE
fig = make_contour(kc[:,0]/D,kc[:,1]/D,kc[:,3],np.arange(0.0, 6.0, 0.2),r'$k$ [m2/s2]','TKE_contour_decay.png')
# TI
fig = make_contour(kc[:,0]/D,kc[:,1]/D,np.sqrt(2/3*kc[:,3])/uc[:,3]*100,np.arange(0.0, 26.0, 1.0),r'$I$ [%]','TI_contour_decay.png')
##### Non-decaying turbulence ########
# U
fig = make_contour(un[:,0]/D,un[:,1]/D,un[:,3]/Uref,np.arange(0.65, 1.1, 0.05),r'$\dfrac{U}{U_\infty}$','U_contour_nondecay.png')
# TKE
fig = make_contour(kn[:,0]/D,kn[:,1]/D,kn[:,3],np.arange(5.95, 7.1, 0.1),r'$k$ [m2/s2]','TKE_contour_nondecay.png')
# TI
fig = make_contour(kn[:,0]/D,kn[:,1]/D,np.sqrt(2/3*kn[:,3])/uc[:,3]*100,np.arange(19.5, 29.0, 1.0),r'$I$ [%]','TI_contour_nondecay.png')



