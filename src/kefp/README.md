# The $k$-$`\varepsilon`$-$`f_p`$ turbulence model

## Theory
It is like a regular $k$-$`\varepsilon`$, but with

$$
\nu_t = C_\mu f_p \frac{k^2}{\varepsilon}
$$

$$
f_p = \frac{2 f_0}{1 + \sqrt{1 + 4 f_0 (f_0 - 1) ({\sigma/\tilde{\sigma}})^2}}
$$

where $f_0 = \frac{C_r}{C_r - 1}$ and $\tilde{\sigma} = 1/\sqrt{C_\mu}$ for neutral flow.


## Compiling the kEpsilonFp code

*G. P. Navarro Dias implemented a [version](https://www.researchgate.net/publication/340929542_code_available_k-epsilon-fp_turbulence_model_for_OpenFOAM_41_and_OpenFOAM_v2012_From_van_dar_Laan_et_al_2015) of the $`k`$-$`\varepsilon`$-$`f_p`$ model. The current version is similar, but with a few updates*. 



The $k$-$`\varepsilon`$-$`f_p`$ model is not included in the default OpenFoam installation, so you need to compile this first. 

0. If you don't already have it, create a user directory, [see here](https://github.com/mchba/actuatorDiskFoam/tree/main?tab=readme-ov-file#actuator-disk-ad-compilation).

1. Create the below folder tree in your `$WM_PROJECT_USER_DIR/src`-folder. You can just copy the `TurbulenceModels`-folder.


```bash 
src/
└── TurbulenceModels
    ├── incompressible
    │   ├── Make
    │   │   ├── files
    │   │   └── options
    │   └── turbulentTransportModels
    │       └── myTurbulentTransportModels.C
    └── turbulenceModels
        └── RAS
            └── kEpsilonFp
                ├── kEpsilonFp.C
                └── kEpsilonFp.H
```

2. `cd TurbulenceModels`
3. `wmakeLnInclude -u turbulenceModels`. This creates a `lnInclude`-folder in the `turbulenceModels`-folder. If you add other turbulence models in the future, this step should be repeated.
4. `cd incompressible`
5. `wmake`. This creates a `lnInclude`-folder in the current folder and a `libmyIncompressibleTurbulenceModels.dylib`-executable (.dylib for Mac or .so for Linux) in your `$WM_PROJECT_USER_DIR/platforms/*`-folder.  

Now you should be able to use the $k$-$`\varepsilon`$-$`f_p`$ model in your OpenFoam simulations.

See also the [guide](https://onlinelibrary.wiley.com/doi/abs/10.1002/we.1736)  by Håkan Nilsson (especially the section "Implement your own versions of kEpsilon and kOmegaSST").

## Example case

Can be found [here](https://github.com/mchba/actuatorDiskFoam/tree/main/examples/single_turbine_kefp).
