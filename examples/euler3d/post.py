import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.integrate as spi
mpl.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 17
plt.rcParams['xtick.top'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.right'] = True
plt.rcParams['ytick.direction'] = 'in'
yd = {'rotation': 0, 'ha': 'right', 'va': 'center'}

'''
    Post-process of 3D Euler equation simulation of single AD.
'''


#######################################################################
#### Parameters ######################################
#######################################################################
Uinf = 8
rho = 1
D = 80
Ad = np.pi*(D/2)**2
CT = 0.01
T = 0.5*rho*Ad*Uinf**2*CT  
dp = -T/Ad                 
cases = ['coarse','fine']
labels = ['D/4','D/32']
lws = [2,2]
pcolor = plt.cm.viridis(np.linspace(0.5,1,len(cases)))



#######################################################################
#### Load line data #################################################
#######################################################################
def load_line(filename):
    data = np.genfromtxt(filename)
    result = {}
    result['x'] = data[:,0]
    result['P'] = data[:,1]
    result['U'] = data[:,2]
    return result

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

lines = []
for i in range(len(cases)):
    it = extract_number_of_iterations('%s/log.simpleFoam'%(cases[i]))
    lines.append(load_line('%s/postProcessing/lines/%s/xlineCenter_p_U.xy'%(cases[i],it)))


#######################################################################
#### Analytical model #################################################
#######################################################################
# Koning lightly loaded disk
def pint(rp, tp, x, r):
    return rp*x/(rp**2 + r**2 + x**2 - 2*rp*r*np.cos(tp))**(1.5)
def konsol(x,r,dp,D):
    # Compute the integral using nquad
    result, error = spi.nquad(pint, [[0, D/2], [0, 2*np.pi]], args=(x, r))
    # Pressure
    P = dp/(4*np.pi)*result
    P = np.nan_to_num(P, nan=0)
    # Check if point in wake region
    mask = (x >= 0) & (r < D/2) & (r > -D/2)
    wake_term = np.where(mask, -dp/Uinf, 0)
    # Streamwise velocity
    U = Uinf - P/Uinf - wake_term

    return U, P

kon_sty = {'color': 'k', 'ls': '-', 'lw': 2}
# Solve at various locations in space
xsol = np.arange(-5*D-1e-3,5*D,0.01*D)
psol = np.zeros_like(xsol)
Usol = np.zeros_like(xsol)
for i in range(len(xsol)):
    Usol[i], psol[i] = konsol(x=xsol[i], r=0, dp=dp, D=D)

#######################################################################
#### Velocity and pressure at the centerline through the AD axis ###########
#######################################################################
reduce = 1.4
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(3.8*reduce, 4*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.2)

# Velocity
ax[0].plot(xsol/D,Usol/Uinf,label='Koning',**kon_sty)
for i in range(len(cases)):
    line = lines[i]
    ax[0].plot(line['x']/D,line['U']/Uinf,'--',color=pcolor[i],label=labels[i], lw=lws[i])
ax[0].set_ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
ax[0].set_xlim([-5,5])
ax[0].set_ylim([0.994,1.001])
ax[0].grid()

# Pressure
pNorm = (rho*Uinf**2)
ax[1].plot(xsol/D,psol/pNorm,**kon_sty)
for i in range(len(cases)):
    line = lines[i]
    ax[1].plot(line['x']/D,line['P']/pNorm,'--',color=pcolor[i], lw=lws[i])
ax[1].set_xlabel('$x/D$')
ax[1].set_ylabel(r'$\dfrac{P}{\rho U_\infty^2}$',**yd)
ax[1].set_xlim([-5,5])
ax[1].grid()
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=2)
fig.savefig('koning_ad.png',bbox_inches='tight',dpi=300)



