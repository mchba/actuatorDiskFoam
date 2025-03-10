# actuatorDiskFoam

A simple actuator disk (AD) model for OpenFOAM. Tested with OpenFOAM v2206.

Flow assumptions:
- Incompressible
- Single-phase flow
- Freestream flow is parallel with rotor axis, i.e. no turbine yaw or tilt

These are typical assumptions for wind farm flows. The AD model can in theory be used for both RANS and LES, but has only been tested for RANS.

## Motivation

In the default AD model of OpenFOAM [actuationDisk](https://doc.openfoam.com/2312/tools/processing/numerics/fvoptions/sources/rtm/actuationDisk/):
- A "monitor" point is used to probe the freestream velocity in the "Froude's method" variant. This makes sense for a single turbine, but not for turbines in a wind farm.
- Since the "Froude's method" variant essentially just is a fixed force AD, it is unnessarcy to use 1D momentum theory for this.
- The variableScaling implementation is misunderstood in two ways: (i) "variable scaling" in the original paper by [van der Laan et al. (2015)](https://doi.org/10.1002/we.1816)  refers to scaling the force distribution on the AD, which is not done in the implementation, and (ii) the monitor point is still used, while van der Laan et al. used a calibration procedure to exactly avoid this.
- The implementation also accomodates compressible and multi-phase flow, which naturally makes the code longer and more complicated.

## AD variants in actuatorDiskFoam

An AD is not just an AD. There exist many, many versions and variants. Here are the variants currently available in actuatorDiskFoam:

| Variant            | Thrust calculation            | Force distribution | Tangential forces |
|--------------------|------------------------------|------------------------|-------------|
| fixed   | $T = \frac{1}{2} \rho A U_{\infty}^2 C_T$ | Uniform           | No |
| calaf   | $T = \frac{1}{2} \rho A U_{d}^2 C_T'$ | Uniform           | No |

Only the calaf AD should be used for wind farm studies, since the freestream velocity, $U_\infty$, is unknown for waked turbines.

### Fixed force

The thrust and power of the AD are
$$
T = \frac{1}{2} \rho A U_\infty^2 C_T,
$$
$$
P = \frac{1}{2} \rho A U_\infty^3 C_P.
$$

Since both $U_\infty$ and the coefficients are given as inputs, the thrust and power are thereby fixed a-priori.

Inputs:
- The freestream velocity, $U_\infty$.
- The thrust and power coefficients, $C_T$ and $C_P$ (based on freestream velocity).
- The disk area, $A = \pi \left(\frac{D}{2} \right)^2$.
- Position of AD.


### Calaf

The thrust and power of the AD
$$
T = \frac{1}{2} \rho A U_d^2 C_T',
$$
$$
P = \frac{1}{2} \rho A U_d^3 C_P',
$$
where $U_d$ is the disk-averaged velocity. Since $U_d$ is calculated from the CFD solution, the thrust and power are *not* fixed a-priori.

Note, that only $C_T$ is needed for the Calaf AD, because both $C_T'$ and $C_P'$ (based on disk-averaged velocity) can be calculated from 1D momentum theory as

$$
\begin{align}
    a &= \frac{1}{2} \left( 1 - \sqrt{1 - C_T}\right)
     , \\
    C_P &= 4 a (1 -a)^2, \\
    C_T' &= \frac{4}{a^{-1} - 1} , \\
    C_P' &= C_T' .
\end{align}
$$

Inputs:
- The thrust coefficient, $C_T$ (based on freestream velocity).
- The disk area, $A = \pi \left(\frac{D}{2} \right)^2$.
- Position of AD.


## OpenFOAM

The current setup has only been tested with v2206. You can see this [video](https://www.youtube.com/watch?v=CeEJS1eT9NE&t=477s) (start around 8:00) for a concise guide on how to download OpenFOAM.

To check that you have installed OpenFOAM correctly, type

```
simpleFoam -help
```

in the terminal, which, if successful, should print some information about the simpleFoam solver.

## Actuator Disk (AD) compilation

To be able to use this AD, it must first be compiled and linked to your OpenFOAM installation.

1. Activate your OpenFOAM (if `simpleFoam -help` works, it is activated) and check if you have a OpenFOAM user directory:

   `cd $WM_PROJECT_USER_DIR`

    If you don't have this directory, create it with `mkdir -p $WM_PROJECT_USER_DIR/{run,applications,src}`. The user directory is used to add custom code, see more info [here](https://www.tfd.chalmers.se/~hani/kurser/OS_CFD_2022/lectureNotes/01_initialPreparations.pdf).


2. `cp src $WM_PROJECT_USER_DIR/src/actuatorDiskFoam -r`.
3. `cd $WM_PROJECT_USER_DIR/src/actuatorDiskFoam`
4. `wmake`. This compiles the AD code and creates a library called `lib_actuatorDiskFoam.so` in the `$WM_PROJECT_USER_DIR/platforms` folder.

If you look at the examples, you will find that they all have a reference to the `lib_actuatorDiskFoam.so`-file in their `system/controlDict`-file.

## Examples

Examples are provided in the examples folder.


## Other AD implementations for OpenFOAM

Here is a list of other open-source AD models for OpenFOAM:

| Project            | Last commit | OpenFOAM version            | Force allocation method | Tangential forces |
|--------------------|--------------------|------------------------------|------------------------|-------------|
| [actuatorDiskFoam](https://github.com/your-repo)   | 2025 | Tested in v2206 | Cylinder volume           | No |
| [actuationDisk](https://doc.openfoam.com/2312/tools/processing/numerics/fvoptions/sources/rtm/actuationDisk/)     | 2024 | v2412 | Cylinder volume           | No |
| [actuationDiskRings](https://github.com/jteich99/actuationDiskRings/tree/main)    | 2024 | v2112 | Gaussian smearing           | Yes  |
| [ADM_NR_diskBased](https://github.com/AUfluids/k-epsilon-Sk/tree/main/ADM_NR_diskBased)  |  2024 | Used v1812 | Cylinder volume           | No  |
| [windTurbineModels](https://github.com/asimonder/windTurbineModels/tree/main)   | 2021  | No testcases | Gaussian smearing           | No  |
| [SOWFA](https://github.com/NREL/SOWFA/tree/master)   | 2020 | version 2.4 | Gaussian smearing           | Yes  |
| [diskBasedADM](https://github.com/DriesAllaerts/SOWFA-6/tree/f/customADM/src/fvOptions/sources/diskBasedADM)    | 2021 | No testcases | Cylinder volume           | No  |
| [actuatorDiskExplicitForce](https://github.com/Adellbengbeng/actuatorDiskExplicitForce/tree/master)   | 2016 | version 4.1 | Cylinder volume           | Yes  |
| [WindFarmOpenFOAM](https://github.com/IamMarkRichmond/WindFarmOpenFOAM)    | 2020 | version 4 and 5 | Cylinder volume           | Yes  |
| [multipleDiskOpenFOAM](https://github.com/EdgarAMO/multipleDiskSimpleFoam)    | 2021 | No testcases | Cylinder volume           | Yes  |




The `actuatorDiskExplicitForce`, `WindFarmOpenFOAM` and `multipleDiskOpenFOAM` projects are programmed by copying and modifying the simpleFoam solver, hence they can not be used in other solvers.


## License

This project is released under the MIT License.

You are free to use, modify, and distribute the code for academic purposes, commercial projects, personal experiments, or any other purpose. However, the code is provided "as-is," without any warranty of any kind. The developers of this project are not liable for any damages or issues arising from the use of this software. Users bear sole responsibility for the results obtained or consequences arising from its use.


