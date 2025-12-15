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
# Grid on by default
plt.rcParams['axes.grid'] = True
# DPI 300
plt.rcParams['figure.dpi'] = 300
yd = {'rotation': 0, 'ha': 'right', 'va': 'center'}

'''
    Post-process of 3D Euler equation simulations of single AD
    to check convergence.
'''


#######################################################################
#### Parameters ######################################
#######################################################################
Uinf = 8
rho = 1
D = 80
Ad = np.pi*(D/2)**2
CT = 0.75
a = 0.5 * (1.0 - np.sqrt(1 - CT))
CP = 4 * a * (1.0 - a)**2
T = 0.5*rho*Ad*Uinf**2*CT             
cases = ['case_grid0','case_grid1','case_grid2','case_grid3','case_grid4']
labels = ['$D/4$','$D/8$','$D/16$','$D/32$','$D/64$']
ncd = [4,8,16,32,64]  # Number of cells per diameter
lws = [2,2,2,2,2]
colors = plt.cm.viridis(np.linspace(0.5,1,len(cases)))


#######################################################################
#### Load AD data #################################################
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
    ads.append(load_ad_history(cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))

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
#### AD iteration history ######
#######################################################################
reduce = 0.8
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(8*reduce, 5*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.3)
for i in range(len(cases)):
    ad = ads[i]
    ax[0].plot(ad['Time'], ad['P']/(0.5*np.pi*(D/2)**2*Uinf**3), label=labels[i],color=colors[i], lw=1.5)
    ax[1].plot(ad['Time'], ad['T']/(0.5*np.pi*(D/2)**2*Uinf**2),color=colors[i], lw=1.5)

ax[0].set_ylim([0.4,1])
#ax[0].set_yticks([0.5,0.6,0.7,0.8,0.9])
ax[1].set_ylim([0.5,1])
#ax[1].set_yticks([0.7,0.8,0.9,1.0])
ax[1].set_xlim(left=0)
ax[1].set_xlabel('Iteration')
ax[0].set_ylabel(r'$\dfrac{P}{\frac{1}{2} \rho A U_\infty^3}$',**yd)
ax[1].set_ylabel(r'$\dfrac{T}{\frac{1}{2} \rho A U_\infty^2}$',**yd)
ax[0].plot(plt.gca().get_xlim(),[CP,CP],'k--', label='1D mom theory')
ax[1].plot(plt.gca().get_xlim(),[CT,CT],'k--')
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5)
fig.text(0.04, 0.88, "(a)", ha="center", fontsize=15)
fig.text(0.04, 0.45, "(b)", ha="center", fontsize=15)
fig.savefig('pow_thrust_history.png',bbox_inches='tight',dpi=300)


#######################################################################
#### Convergence plot ######
#######################################################################
reduce = 0.8
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(8*reduce, 5*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.3)
CPfinal = np.zeros(len(cases))
CTfinal = np.zeros(len(cases))
for i in range(len(cases)):
    ad = ads[i]
    # Calculate CP and CT at final iteration
    CPfinal[i] = ad['P'][-1]/(0.5*np.pi*(D/2)**2*Uinf**3)
    CTfinal[i] = ad['T'][-1]/(0.5*np.pi*(D/2)**2*Uinf**2)


# Calculate Richardson extrapolated value
def create_richardson_matrix(n_levels):
    """Create Richardson extrapolation matrix for n_levels grid levels"""
    Rmat = np.zeros((n_levels, n_levels))
    for i in range(n_levels):
        for j in range(n_levels):
            Rmat[i, j] = (2**j)**i
    return Rmat

# Create Richardson matrix for current number of cases
Rmat = create_richardson_matrix(len(cases))
#Rmat = create_richardson_matrix(3)
Rmati = np.linalg.inv(Rmat)
CPrichard = np.matmul(Rmati, np.flip(CPfinal).reshape(-1, 1))[0]
CTrichard = np.matmul(Rmati, np.flip(CTfinal).reshape(-1, 1))[0]


# Plot simulation results
ax[0].plot(ncd, CPfinal,'ks-', lw=1.5)
ax[1].plot(ncd, CTfinal,'ks-', lw=1.5)

ax[0].set_ylim([0.45,0.6])
ax[1].set_ylim([0.65,0.8])
ax[1].set_xlim(left=0)
ax[1].set_xlabel('$D/ \Delta x$')
ax[0].set_ylabel(r'$\dfrac{P}{\frac{1}{2} \rho A U_\infty^3}$',**yd)
ax[1].set_ylabel(r'$\dfrac{T}{\frac{1}{2} \rho A U_\infty^2}$',**yd)
# Plot 1D momentum theory lines
ax[0].plot(plt.gca().get_xlim(),[CP,CP],'k--', label='1D mom theory')
ax[1].plot(plt.gca().get_xlim(),[CT,CT],'k--')

# Plot Richardson extrapolated values
ax[0].plot(plt.gca().get_xlim(),[CPrichard,CPrichard],'g--', label='RE')
ax[1].plot(plt.gca().get_xlim(),[CTrichard,CTrichard],'g--')
#ax[0].legend(fontsize=12)

fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5)



#######################################################################
#### Convergence plot (with error compared to finest resolution)
#######################################################################
reduce = 1
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(8*reduce, 5*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.3)

# Fine resolution values
CPfine = CPfinal[-1]
CTfine = CTfinal[-1]

# Plot simulation results
ax[0].plot(ncd, (CPfinal-CPfine)/CPfine*100,'ks-', lw=1.5)
ax[1].plot(ncd, (CTfinal-CTfine)/CTfine*100,'ks-', lw=1.5)

ax[0].set_ylim([-10,1.5])
ax[1].set_ylim([-6.5,1.5])
ax[1].set_xlim(left=0)
ax[1].set_xlabel('$D/ \Delta x$')
ax[0].set_ylabel(r'$\dfrac{P - P_{\rm fine}}{P_{\rm fine}}$ [%]',**yd)
ax[1].set_ylabel(r'$\dfrac{T - T_{\rm fine}}{T_{\rm fine}}$ [%]',**yd)
# Change xlabel to ncd
ax[1].set_xticks(ncd)
# Title
ax[0].set_title('Error compared to finest resolution ($%d$ cells pr. D)'%ncd[-1], pad=15, fontsize=15)    

# Make grayed area representing +/- 1% error
ax[0].fill_between(plt.gca().get_xlim(), -1, 1, color='gray', alpha=0.3)
ax[1].fill_between(plt.gca().get_xlim(), -1, 1, color='gray', alpha=0.3)
ax[0].text(ncd[0]+1, 0.2, '±1%', fontsize=12, color='gray')
ax[1].text(ncd[0]+1, 0.2, '±1%', fontsize=12, color='gray')
fig.savefig('error.png',bbox_inches='tight',dpi=300)



#######################################################################
#### Velocity and pressure at the centerline through the AD axis ###########
#######################################################################
reduce = 1.4
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(3.8*reduce, 4*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.2)

# Velocity
for i in range(len(cases)):
    line = lines[i]
    ax[0].plot(line['x']/D,line['U']/Uinf,'--',color=colors[i],label=labels[i], lw=lws[i])
ax[0].set_ylabel(r'$\dfrac{U}{U_\infty}$',**yd)
ax[0].set_xlim([-5,5])
ax[0].set_ylim([0.5,1.001])
ax[0].set_title('Axial velocity and pressure along centerline', pad=15, fontsize=15)

# Pressure
pNorm = (rho*Uinf**2)
for i in range(len(cases)):
    line = lines[i]
    ax[1].plot(line['x']/D,line['P']/pNorm,'--',color=colors[i], lw=lws[i])
ax[1].set_xlabel('$x/D$')
ax[1].set_ylabel(r'$\dfrac{P}{\rho U_\infty^2}$',**yd)
ax[1].set_xlim([-5,5])
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=2)
fig.savefig('vel_pres.png',bbox_inches='tight',dpi=300)



