# single_turbine_uniform_inflow

A single AD case with uniform inflow. The case is similar to the 20\% TI case from [Fei et al. (2025)](https://iopscience.iop.org/article/10.1088/1742-6596/3016/1/012033).

Takes around 55 seconds to simulate on my laptop (Apple M4 Pro). 

## Grid

- Rotor diameter: $D = 40$ m.
- Domain size: $L_x/D = L_y/D = L_z/D = 27.5$.
- Background resolution: $\frac{D}{\Delta x} = \frac{D}{\Delta y} = \frac{D}{\Delta z} = 2$.
- Resolution in first refined region: $\frac{D}{\Delta x} = \frac{D}{\Delta y} = \frac{D}{\Delta z} = 8$
- Resolution in second refined region: $\frac{D}{\Delta x} = \frac{D}{\Delta y} = \frac{D}{\Delta z} = 16$
- Total number of cells: 550k.

![](grid.png)



## Inflow

At the inlet, the following values are set:

- Velocity: $U = 10$ m/s.
- TKE: $k = 6.0~\textrm{m}^2~\textrm{s}^{-2}$.
- Dissipation: $\varepsilon = 0.243~\textrm{m}^2~\textrm{s}^{-3}$.

The turbulence will decay throughout the domain, because there is no shear and therefore to turbulence production. This can be prevented by adding source terms to the turbulence equations.

## Results

### Decaying turbulence
![](U_contour_decay.png)

![](TKE_contour_decay.png)

![](TI_contour_decay.png)

### With turbulence source terms

![](U_contour_nondecay.png)

![](TKE_contour_nondecay.png)

![](TI_contour_nondecay.png)

## Comparison with reference data

We here compare with data from [Fei et al. (2025)](https://iopscience.iop.org/article/10.1088/1742-6596/3016/1/012033).

![](centerline_U.png)
![](spanwise10D_U.png)

![](centerline_TKE.png)

![](centerline_nut.png)



