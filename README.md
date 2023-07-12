# WoodSKE
**An algorithm to extract skeletons from discrete point clouds of tree branches collected by terrestrial laser scanners.**<br>
     We developed the WoodSKE method to extract `skeletons` from discrete point clouds of tree branches collected by `terrestrial laser scanners (TLSs).` A TLS point cloud of tree branches is firstly contracted according to the pointwise local point distribution pattern to extract its `coarse skeleton.` Then, the coarse skeleton is thinned and optimized by a noise-filtering method.<br>
--
**DOI**:
https://linkinghub.elsevier.com/retrieve/pii/S0303243421002968<br>
**Reference:** Wu B, Zheng G, Chen Y, et al. Assessing inclination angles of tree branches from terrestrial laser scan data using a skeleton extraction method[J]. International Journal of Applied Earth Observation and Geoinformation, 2021, 104: 102589.<br>
**Graphical Abstract:**<br> 
![Graphical Abstract](PNG/GraphicAbstract.png)
**Highlights:**<br> 
The WoodSKE method is suitable for extracting skeletons from woody point clouds with variable point density and outliers at `the single-tree and plot scales.` Setting seed points or converting the format of discrete point clouds is `not required` when using the WoodSKE method. Besides, the WoodSKE-extracted skeletons maintained the structure of twigs, which provided a base for extracting their inclination angles and other geometrical features. Before running the WoodSKE method, users `do not need to segment individual trees or single branches` from tree point clouds.<br> 
We share the Python script of WoodSKE and the test datasets (TLS point clouds at single-tree and plot scales) in .csv format.
**Test Datasets:**<br> 
![Test datasets](PNG/Models-ALL.jpg)
**Results show:**<br> 
![Skeleton extraction](PNG/FSD.jpg)
The key steps of WoodSKE are `Coarse skeleton contraction` and `Skeleton thinning`.<be> The detailed description of these two steps is provided in the related paper. The thinning step of the post-filling coarse skeleton analyzed during the coarse skeleton contraction is shown in the following figure:<br>
--
![Skeleton extraction](PNG/Thin.jpg)
The points in the blue spherical area formed the nearby point set (SCO) of a coarse skeleton point PCS (green dot). ESO means the nearest Euclidean distance between PCS and the input point cloud (the distance between PCS and Pnear). PL is the farthest point to Pnear (blue dot) in the SCO. The ESO of PL (orange dot) is ESO ′. In the inset (C), the skeleton point PSKE (red dot) was located by the mean coordinate of points with larger ESO than that of PCS in the dash-shaded area. The red lines present the thinned skeleton.





