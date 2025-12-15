import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 17
plt.rcParams['xtick.top'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.right'] = True
plt.rcParams['ytick.direction'] = 'in'
yd = {'rotation': 0, 'ha': 'right', 'va': 'center'}

'''
    Comparision with the analytical model from Madsen (1988).
    See more details in Appendix B of Baungaard, Nishino & van der Laan (2025).

'''


#######################################################################
#### Parameters ######################################
#######################################################################
Uinf = 8
rho = 1
D = 80
CT = 0.01
T = 0.5*rho*D*Uinf**2*CT  # Unit: N/m (because we are in 2D)
dp = -T/D                  # Unit: N/m = Pa*m
xin = 3*D # Position of turbine from inlet
cases = ['fixed','calaf']
lws = [3,1]
pcolor = plt.cm.viridis(np.linspace(0.5,1,len(cases)))


#######################################################################
#### Load AD data ######################################
#######################################################################
def load_ad_history(filename):
    # Get headers
    with open(filename, 'r') as file:
        #file.readline()  # Skip the first line
        #headers = file.readline().strip().split()  # Read the second line for headers
        file.readline()  # Skip the first line
        headers = file.readline().strip().split()
        headers = [h for h in headers if h != '#']  # Remove all '#' symbols
        
    # Read actually data
    data = np.genfromtxt(filename,skip_header=2)
    
    # Create a dictionary to store all iterations of each column
    disk = {header: data[:, i] for i, header in enumerate(headers)}
    
    return disk

ads = []
for i in range(len(cases)):
    # Load AD data
    ads.append(load_ad_history('%s/postProcessing/disk1/0/actuatorDiskFoam.dat'%cases[i]))


#######################################################################
#### Iteration history of thrust ######################################
#######################################################################
reduce = 0.8
dz = 1 # Grid thickness
fig = plt.figure(figsize=(reduce*8,reduce*4))
for i in range(len(cases)):
    ad = ads[i]
    cfdCT = ad['T']/dz/(0.5*D*Uinf**2)
    plt.plot(ad['Time'], cfdCT, label='%s'%(cases[i]),color=pcolor[i], lw=lws[i])

plt.ylim([0.0099,0.0101])
plt.xlabel('Iteration')
plt.ylabel(r'$\dfrac{T}{\frac{1}{2} \rho A U_\infty^2}$',**yd)
plt.plot(plt.gca().get_xlim(),[CT,CT],'k--', label='1D mom theory')
plt.grid()
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5)
fig.savefig('thrust_history.png',bbox_inches='tight',dpi=300)


#######################################################################
#### Load line data #################################################
#######################################################################
def load_line(filename):
    data = np.genfromtxt(filename)
    result = {}
    result['x'] = data[:,0] - xin # Translate to have 0 at turbine
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
def madsen_model_nd(x,y,D,CT):
    '''
        Non-dimensional version of the Madsen (1988 model). Used by Rethore & Sørensen (2012)
        to verify their AD model and also by Baungaard, Nishino & van der Laan (2025).
        
        The model assumes no viscosity and CT << 1. 
        
        The model has been re-derived in the recent WES paper by Helge Madsen
        from 2023 (see eq.25-26).
        
        Non-dimensionalization:
            U is non-dimensionalized with Uinf.
            P is non-dimensionalized with rho*Uinf**2
    '''
    # Non-dim pressure (normalized by rho*Uinf^2)
    P = -CT/(4*np.pi)*(np.arctan(((D/2)-y)/x) + np.arctan(((D/2)+y)/x))
    # It is well known (see discussion in Madsen 1988) that the above formula gives
    # singularities at the tips of the AD. Replace these with 0.
    P = np.nan_to_num(P, nan=0)
    # Check if point in wake region
    mask = (x >= 0) & (y < D/2) & (y > -D/2)
    wake_term = np.where(mask, -0.5*CT, 0)
    # Normalized by Uinf
    U = 1 - P + wake_term
    return U, P

xmads = np.linspace(-5*D,5*D,100)
ymads = np.zeros_like(xmads)
Umadsnd, Pmadsnd = madsen_model_nd(xmads, ymads, D, CT)
Umads = Umadsnd*Uinf
Pmads = Pmadsnd*rho*Uinf**2
mads_sty = {'color': 'k', 'ls': '-', 'lw': 3} 


#######################################################################
#### Velocity and pressure at the centerline through the AD axis ###########
#######################################################################
reduce = 1.4
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(3.8*reduce, 4*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.2)

# Velocity
ax[0].plot(xmads/D,Umads/Uinf,label='Madsen (1988)',**mads_sty)
for i in range(len(cases)):
    line = lines[i]
    ax[0].plot(line['x']/D,line['U']/Uinf,color=pcolor[i],label='%s'%cases[i], lw=lws[i])
#plt.xlabel('$x/D$')
ax[0].set_ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
ax[0].set_xlim([-5,5])
ax[0].set_ylim([0.994,1.001])
ax[0].grid()

# Pressure
pNorm = (rho*Uinf**2)
ax[1].plot(xmads/D,Pmads/pNorm,**mads_sty)
for i in range(len(cases)):
    line = lines[i]
    #plt.plot(line['x']/D,line['P']/pNorm,color=pcolor[i],label='D/%s'%cases[i],)
    ax[1].plot(line['x']/D,line['P']/pNorm,color=pcolor[i], lw=lws[i])
ax[1].set_xlabel('$x/D$')
ax[1].set_ylabel(r'$\dfrac{P}{\rho U_\infty^2}$',**yd)  
#ax[1].legend(loc='upper right',fontsize=12)
ax[1].set_xlim([-5,5])
ax[1].grid()
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5)
fig.savefig('madsen_ad.png',bbox_inches='tight',dpi=300)


    
