# docs

The DLFIND manual is attached. For convenience, a non-exhaustive list of default parameter values is provided here. 
The "under-the-hood" algorithms for choosing default parameters are in some cases more complicated than those presented here:
e.g., multistate optimizations sometimes change defaults relative to their single-state congeners. 

#### ``printl``
Printout level.
- 0: none 
- 2: some (default)
- 4: verbose
- 6: debug

#### ``icoord``
Type of coordinate system—many options possible (see DLFIND manual).
- 0: Cartesian (default)

#### ``iopt``
Controls optimization algorithm.
- 0: steepest descent 
- 1: Polak-Ribiere conjugate gradient w/ automatic restart
- 2: Polak-Ribiere conjugate gradient w/ restart every 10 steps
- 3: L-BGFS (default)
- 9: P-RFO, for transition state searches

#### ``iline``
Type of line search or trust radius.
- 0: simple scaling (default for ``iopt`` > 3)
- 1: trust radius based on energy criterion (default when ``iopt`` is 3)
- 2: trust radius based on gradient criterion (default when ``iopt`` is 0, 1, or 2)

#### ``inithessian``
Method used to generate initial Hessian matrix.
- 0: external calculation using ``dlf_get_hessian`` (default if ``dlf_get_hessian`` defined)
- 1: build with one-point finite difference of gradient
- 2: build with two-point finite difference of gradient (default otherwise)
- 3: build diagonal Hessian with one-point finite difference
- 4: set Hessian to be an identity matrix

#### ``update``
How the Hessian is updated.
- 0: no update
- 1: Powell update
- 2: Bofill update (default)
- 3: BGFS update

#### ``spec``
Freezing atoms, etc for optimization. (``spec`` is an array with an entry for each atom.)
- \>0: active, treated normally. The value can be used to encode residue/fragment number.
- 0: active in optimization, but treated in Cartesian coordinates no matter what.
- -1: frozen
- -2: x-coordinate frozen
- -3: y-coordinate frozen
- -4: z-coordinate frozen
- -23: x-coordinate and y-coordinate frozen
- -24: x-coordinate and z-coordinate frozen
- -34: y-coordinate and z-coordinate frozen

``spec`` also contains a way to specify constraints. See manual for more information.
