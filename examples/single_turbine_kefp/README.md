# single_turbine with $k$-$`\varepsilon`$-$`f_p`$

A single AD case with atmospheric surface layer (aka. log-law) inflow using the $k$-$`\varepsilon`$-$`f_p`$ turbulence model [(van der Laan et al., 2015)](https://onlinelibrary.wiley.com/doi/abs/10.1002/we.1736).

The 4cD and 8cD simulations took around 2s and 25s, respectively, to simulate on my laptop (Apple M4 pro).

## The $k$-$`\varepsilon`$-$`f_p`$ model

$$
\nu_t = C_\mu f_p \frac{k^2}{\varepsilon}
$$

$$
f_p = \frac{2 f_0}{1 + \sqrt{1 + 4 f_0 (f_0 - 1) ({\sigma/\tilde{\sigma}})^2}}
$$

where $f_0 = \frac{C_r}{C_r - 1}$ and $\tilde{\sigma} = 1/\sqrt{C_\mu}$ for neutral flow.


## Compiling the kEpsilonFp code

The $k$-$`\varepsilon`$-$`f_p`$ model is *not* included in the default OpenFoam installation, so you need to compile this first. See  [instructions here](https://github.com/mchba/actuatorDiskFoam/tree/main/src/kefp).


## Grid

A uniform grid is used in the center of the domain with stretching outwards from there. Streching is also applied in the vertical direction to better resolve the velocity gradient near the ground.

- Rotor diameter: $D = 80$ m.
- Domain size: $L_x/D = 24$, $L_y/D = 16$, $L_z/D = 8$.
- Resolution: Two grids are used, $\frac{D}{4}$ and $\frac{D}{8}$, respectively.
- Total number of cells: 82k and 337k.



## Inflow

Log-law (see single_turbine [readme](https://github.com/mchba/actuatorDiskFoam/tree/main/examples/single_turbine)).


## Comparison with reference data

We here compare with data from [Baungaard et al. (2022)](https://wes.copernicus.org/articles/7/1975/2022/), who simulated the same case.

![](U_contour.png)

![](centerline_U.png)
![](centerline_TKE.png)

Possible reasons for disagreement with EllipSys3D:
- Different implementations of the AD. The one in EllipSys can refine the AD independently of the background grid, hence the grid requirement is likely less.
- Different numerical schemes. EllipSys uses QUICK, while upwind and linearUpwind were tried in OpenFoam. Unfortunately, the QUICK scheme in OpenFoam does not work well for this case.
- The grids in the two codes are not the exactly the same (the EllipSys domain was larger and use another vertical stretching).

In summary: The current case is more difficult for OpenFoam (compared to the [case](https://github.com/mchba/actuatorDiskFoam/tree/main/examples/single_turbine) with the standard $k$-$`\varepsilon`$ model), probably because of the larger velocity gradients in the wake. It is nevertheless recommended to use the current setup, because the $k$-$`\varepsilon`$-$`f_p`$ model is more accurate than the standard $k$-$`\varepsilon`$ model [(van der Laan et al., 2015)](https://onlinelibrary.wiley.com/doi/abs/10.1002/we.1736).




