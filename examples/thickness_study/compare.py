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
    Compare the dx = {D/8, D/16, D/32} simulations.

    Each of these have been run with different AD thicknesses:
       Nt = {1, 2, 4, 8, 16} cells (from thin to thick AD).
'''


#######################################################################
#### Parameters ######################################
#######################################################################
Uinf = 8
rho = 1
D = 80
dx = D/32
Ad = np.pi*(D/2)**2
CT = 0.75
a = 0.5 * (1.0 - np.sqrt(1 - CT))
CP = 4 * a * (1.0 - a)**2
T = 0.5*rho*Ad*Uinf**2*CT             
cases = ['case_thick16','case_thick8','case_thick4','case_thick2','case_thick1']
nct = np.array([16,8,4,2,1])  # Number of cells per thickness (i.e. Nt)
cD = np.array([4,8,16,32,64])    # Number of cells per diameter (i.e. D/dx)

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

ads4 = []
ads8 = []
ads16 = []
ads32 = []
ads64 = []
for i in range(len(cases)):
    ads4.append(load_ad_history('cD4/'+cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))
    ads8.append(load_ad_history('cD8/'+cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))
    ads16.append(load_ad_history('cD16/'+cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))
    ads32.append(load_ad_history('cD32/'+cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))
    ads64.append(load_ad_history('cD64/'+cases[i]+'/postProcessing/disk1/0/actuatorDiskFoam.dat'))




#######################################################################
#### Extract final values #################################################
#######################################################################
# Initialize matrices for CP and CT values
CPfinal = np.zeros((5, len(cases)))  # 5 grid resolutions, len(cases) thickness cases
CTfinal = np.zeros((5, len(cases)))
ads_list = [ads4, ads8, ads16, ads32, ads64]

for j, ads in enumerate(ads_list):
    for i in range(len(cases)):
        ad = ads[i]
        # Calculate CP and CT at final iteration
        CPfinal[j, i] = ad['P'][-1]/(0.5*np.pi*(D/2)**2*Uinf**3)
        CTfinal[j, i] = ad['T'][-1]/(0.5*np.pi*(D/2)**2*Uinf**2)


#######################################################################
#### Compare power and thrust (as function of Nt) ######
#######################################################################
reduce = 0.9
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(8*reduce, 5*reduce))
ax = ax.flatten()
plt.subplots_adjust(hspace=0.3)

# Plot parameters
colors = plt.cm.viridis(np.linspace(0.0,1,len(cD)))
#colors = ['r', 'b', 'g', 'y']
linewidths = [1.5, 1.5, 1, 1, 1]
labels = ['$\Delta x = D/4$', '$\Delta x = D/8$', '$\Delta x = D/16$', '$\Delta x = D/32$', '$\Delta x = D/64$']

# Plot simulation results
for j in range(5):
    ax[0].plot(nct, CPfinal[j, :], marker='s', markersize=5,color=colors[j], lw=linewidths[j], label=labels[j])
    ax[1].plot(nct, CTfinal[j, :], marker='s',markersize=5,color=colors[j], lw=linewidths[j])

ax[0].set_ylim([0.39,0.6])
ax[1].set_ylim([0.59,0.8])
ax[1].set_xlim(left=0)
ax[1].set_xlabel(r'Number of cells over the AD thickness, $N_t = \Delta x_{\rm AD}/\Delta x$')
ax[0].set_ylabel(r'$\dfrac{P}{\frac{1}{2} \rho A U_\infty^3}$',**yd)
ax[1].set_ylabel(r'$\dfrac{T}{\frac{1}{2} \rho A U_\infty^2}$',**yd)
ax[0].set_yticks(np.arange(0.4,0.65,0.05))
ax[1].set_yticks(np.arange(0.6,0.85,0.05))
# Plot 1D momentum theory lines
ax[0].plot(plt.gca().get_xlim(),[CP,CP],'k--', label='1D mom theory')
ax[1].plot(plt.gca().get_xlim(),[CT,CT],'k--')
# Flip x-axis so it increases from right to left
ax[0].invert_xaxis()
ax[0].set_xticks(nct)
fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
          ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5,title='Grid resolution')
fig.savefig('thickness_study_Nt.png', dpi=300,bbox_inches='tight')


#######################################################################
#### Compare power and thrust (as function of cD) ######
#######################################################################
# reduce = 0.9
# fig, ax = plt.subplots(2, 1, sharex=True, sharey=False, figsize=(8*reduce, 5*reduce))
# ax = ax.flatten()
# plt.subplots_adjust(hspace=0.3)
# # Plot parameters
# colors = ['r', 'b', 'g', 'y', 'm']
# linewidths = [1.5, 1.5, 1, 1, 1]
# labels = ['Nt=16', 'Nt=8', 'Nt=4', 'Nt=2', 'Nt=1']
# # Plot simulation results
# for i in range(len(cases)):
#     ax[0].plot(cD, CPfinal[:, i], f'{colors[i]}s-', lw=linewidths[i], label=labels[i])
#     ax[1].plot(cD, CTfinal[:, i], f'{colors[i]}s-', lw=linewidths[i])
# ax[0].set_ylim([0.4,0.6])
# ax[1].set_ylim([0.6,0.8])
# ax[1].set_xlim(left=0)
# ax[1].set_xlabel(r'Number of cells over the AD diameter, $c_D = D/\Delta x$')
# ax[0].set_ylabel(r'$\dfrac{P}{\frac{1}{2} \rho A U_\infty^3}$',**yd)
# ax[1].set_ylabel(r'$\dfrac{T}{\frac{1}{2} \rho A U_\infty^2}$',**yd)
# ax[1].set_yticks(np.arange(0.60,0.85,0.05))
# # Plot 1D momentum theory lines
# ax[0].plot(plt.gca().get_xlim(),[CP,CP],'k--', label='1D mom theory')
# ax[1].plot(plt.gca().get_xlim(),[CT,CT],'k--')
# # Flip x-axis so it increases from right to left
# #ax[0].invert_xaxis()
# ax[0].set_xticks(cD)
# fig.legend(loc='center left',fontsize=12,bbox_to_anchor=(0.91, 0.5),
#           ncol=1, fancybox=True, shadow=True,scatterpoints=1, handlelength=1.5,title='AD thickness')


