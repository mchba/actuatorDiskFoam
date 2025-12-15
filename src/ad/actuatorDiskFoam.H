/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2011-2017 OpenFOAM Foundation
    Copyright (C) 2020 ENERCON GmbH
    Copyright (C) 2020 OpenCFD Ltd.

    This is a modification of the actuationDisk code.
    Author of modifications: Mads Baungaard
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Class
    Foam::fv::actuatorDiskFoam

Group
    grpFvOptionsSources

Description
    Simple actuator disk (AD) model.

    Two variants:
    - (i)  Calaf AD, T = 0.5*rho*A*Ud**2*Ctp
    - (ii) Fixed AD, T = 0.5*rho*A*Uinf**2*Ct
    where
    Ud = disk-averaged velocity
    Uinf = freestream velocity
    Ctp = thrust coefficient based on Ud
    Ct  = thrust coefficient based on Uinf.

    For both variants, the thrust force is distributed uniformly over the
    disk. No tangential forces are applied.

    Since the freestream velocity is unknown for turbines in waked situations,
    only the Calaf AD should be used for wind farm studies.

\*---------------------------------------------------------------------------*/

#ifndef actuatorDiskFoam_H
#define actuatorDiskFoam_H

#include "cellSetOption.H"
#include "writeFile.H"
#include "Function1.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{
namespace fv
{

/*---------------------------------------------------------------------------*\
                     Class actuatorDiskFoam Declaration
\*---------------------------------------------------------------------------*/

// Define actuatorDiskFoam class, which inherits functionality from cellSetOption and writeFile.
class actuatorDiskFoam
:
    public cellSetOption,
    public functionObjects::writeFile
{
protected:

    // Variants of AD models
    enum forceMethodType
    {
        CALAF, //!< "Uniform thrust Calaf AD"
        FIXED, //!< "Uniform thrust fixed-force AD"
    };
    static const Enum<forceMethodType> forceMethodTypeNames;

    //- The type of the force computation method
    const enum forceMethodType forceMethod_;

    //- Start time for file output
    scalar writeFileStart_;

    //- End time for file output
    scalar writeFileEnd_;

    //- Actuator disk planar surface area [m2]
    scalar diskArea_;

    //- Surface-normal vector of the actuator disk pointing upstream
    vector diskDir_;

    //- Thrust coefficient
    scalar Ct_;

    //- Power coefficient (only used in the fixed force AD)
    scalar Cp_fixed_;

    //- Reference speed (only used in the fixed force AD)
    scalar Uref_fixed_;

    //- Function to output file header information
    virtual void writeFileHeader(Ostream& os);


private:
    // Private Member Functions

    //- Select force computation method
    void calc
    (
        fvMatrix<vector>& eqn
    );

    //- Compute Calaf AD method
    void calcCalafMethod
    (
        fvMatrix<vector>& eqn
    );

    //- Compute Calaf AD method
    void calcFixedMethod(
        fvMatrix<vector> &eqn);

public:

    //- Runtime type information
    TypeName("actuatorDiskFoam");

    // Constructor: When initilizing a actuatorDiskFoam class, you need to specify these!
    actuatorDiskFoam
    (
        const word& name,
        const word& modelType,
        const dictionary& dict,
        const fvMesh& mesh
    );

    //- No copy construct
    actuatorDiskFoam(const actuatorDiskFoam&) = delete;

    //- No copy assignment
    void operator=(const actuatorDiskFoam&) = delete;

    //- Destructor
    virtual ~actuatorDiskFoam() = default;


    // ----------  Member Functions ----------------

    //- Normal disk direction
    const vector& diskDir() const
    {
        return diskDir_;
    }

    //- Disk area
    scalar diskArea() const
    {
        return diskArea_;
    }

    //- Source term to momentum equation
    virtual void addSup
    (
        fvMatrix<vector>& eqn,
        const label fieldi
    );

    //- IO. Read dictionary
    virtual bool read(const dictionary& dict);
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace fv
} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //
