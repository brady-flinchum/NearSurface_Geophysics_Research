---
title: Mapping Coarse Tree Roots Using Ground-Penetrating Radar with an Angular Grid Acquisition
authors: Brady A. Flinchum, Donald L. Hagan, Martin A. Hamilton, Paul Mullins
journal: Journal of Applied Geophysics
year: 2026
doi: https://doi.org/10.1016/j.jappgeo.2026.106226
---

   
# Mapping Coarse Tree Roots Using GPR with an Angular Grid Acquisition

**Brady A. Flinchum¹, Donald L. Hagan², Martin A. Hamilton³, Paul Mullins⁴**

¹ University of Newcastle, School of Environmental and Life Sciences, Callaghan NSW 2308, Australia 
² Clemson University, Forestry and Environmental Conservation 
³ South Carolina Botanical Garden, Clemson University 
⁴ Bartlett Tree Experts

*Journal of Applied Geophysics*, 2026

Link: [https://doi.org/10.1016/j.jappgeo.2026.106226](https://doi.org/10.1016/j.jappgeo.2026.106226)

---

# Abstract

Roots are critical to tree health and structural stability, yet their complex geometry covered by the soil makes them difficult to characterize. Ground-penetrating radar (GPR) is a nondestructive geophysical method capable of imaging coarse woody roots, but transforming raw GPR data into spatially coherent root maps remains challenging. This study presents 3.6 km of GPR data collected around a mature swamp oak (*Quercus palustris*) with a diameter at breast height of 1.1 m, located in the South Carolina Botanical Gardens, USA. A total of 1170 profiles were acquired at 15 cm spacing using a 500 MHz antenna and a novel angular grid geometry that maintained perpendicular orientation to radially extending roots. A multi-stage processing workflow that consisted of velocity analysis, migration, and site-specific depth-normalization was used to characterize the root system architecture. The resulting dendritic network exhibited visible asymmetry, with higher root density on the upslope side of the trunk. Roots initiated near the trunk at depths of 30--60 cm and became shallower (10--20 cm) near the canopy edge, over 10 m away. The GPR data were used to guide an airspade excavation, which confirmed the location of coarse roots predicted by the survey. These results demonstrate that high-density GPR data, when paired with optimized acquisition and processing, can resolve spatially continuous root networks and support non-invasive root system characterization.


# Introduction

A tree's root system connects it to the soil, enabling the uptake of water and nutrients {cite}`Brantley2017`. Roots are typically divided into coarse and fine roots. Fine roots facilitate resource acquisition, while coarse roots provide structural support {cite}`Reubens2007,Wu2014,Yang2017,Dumroese2019`. The formation and decay of coarse roots influence erosion rates {cite}`Gabet2010,Roering2010,Pawlik2016`, drive chemical and physical weathering processes that convert rock to soil {cite}`Brantley2011,Brantley2017`, and serve as long-term carbon reservoirs in forest ecosystems {cite}`Misra1998,Miller2006`. Despite their ecological significance, the spatial distribution of roots remains difficult to quantify because their complex geometry is hidden below the soil.

Excavation-based studies have provided foundational insights into root architecture {cite}`Danjon2008,Danjon1999,Addo-Danso2016`, but these methods are labor-intensive, cannot be replicated, and can be fatal to the tree [@Guo2013]. GPR surveys conducted around trees have demonstrated that, with advanced signal processing techniques, estimates of root biomass can be made [@Wu2014; @Cui2011; @Addo-Danso2016]. Non-invasive alternatives such as radioactive tracers, sapflow measurements, and soil moisture profiling have been used to estimate rooting depth, but lack the resolution needed to resolve individual roots [@Cermak1980; @Abbott1991; @Hruska1999]. Emerging tools, including sonic root imaging [@Proto2020] and electrical resistivity tomography [@Robinson2010; @Robinson2012; @Onaral2022; @Fath2024], are useful tools but fail to capture detailed root network geometry.

Although GPR has been applied to image tree roots since the early 2000s [@Danjon1999; @Hruska1999; @Butnor2001], transforming GPR data into detailed root maps remains challenging. These challenges fall into three categories: (1) acquisition parameters such as line spacing, orientation, and antenna frequency; (2) post-processing workflows that convert raw profiles into depth sections; and (3) visualization strategies capable of representing small-diameter roots embedded within large soil volumes. Recent studies have used low-cost GPS to improve GPR surveys that have facilitated improved 3D root mapping, characterized roots beneath pavements, and applied algorithms to connect diffraction hyperbolae that trace out individual roots [@Zou20205; @Bassuk2011; @Nichols2017; @Alani2018].

This study addresses the three challenges by implementing a tailored acquisition strategy using a 500 MHz antenna, a novel angular grid geometry, and a depth-sensitive processing workflow. The resulting dataset enabled the visualization of coarse root architecture across a 450 m^2^ area. The alignment of high-amplitude anomalies created by collapsed diffraction hyperbolae across more than 1170 individual profiles created a 3D, spatially continuous, dendritic root network. These results demonstrated that GPR, when paired with optimized acquisition and processing, could be used to characterize the coarse root network hidden beneath the soil.

# Site Description

Ground-penetrating radar (GPR) data were collected around a mature swamp oak (*Quercus palustris*) located in the South Carolina Botanical Gardens (SCBG) in Clemson, SC (*34.67390, -82.82453*). The tree, situated on the side slope of a small hill approximately 25 m wide, had a diameter at breast height (DBH) of 101 cm (Figure {numref}`fig-map`). The hill separates Perimeter Road, a well-traveled two-lane road, from the SCBG parking lot. Elevation increased by approximately 4 m when moving upslope from the parking lot toward Perimeter Road.

The study area was divided diagonally into upslope and downslope zones. The upslope side was adjacent to the road, and the downslope side was adjacent to the parking lot (Figure {numref}`fig-map`a). The upslope side was more exposed to wind due to the absence of shelter along Perimeter Road, whereas the downslope side was shaded and protected by other trees. Four additional trees were present within the survey area (Figure {numref}`fig-map`a), each smaller than the oak. The area was actively managed but not irrigated.

To characterize site topography and trunk geometry, structure-from-motion (SfM) data were acquired using a Nikon D750 equipped with a 20 mm lens [@Westoby2012; @Micheletti2015]. A local coordinate system was established using a total station and ground control points placed prior to image acquisition. Images and control point coordinates were processed in Agisoft Metashape (Agisoft 2024), yielding a high-resolution (2 cm) digital elevation model (DEM). Trunk geometry for surrounding trees was also captured (Figure {numref}`fig-map`). Both Cartesian (Figure {numref}`fig-map`a) and polar coordinate systems (Figure {numref}`fig-map`b) were used in this study.

Excavations of mature blue oak (*Quercus douglasii*) indicate that most coarse-root biomass is concentrated above $\sim$0.5 m, with a general rooting depth of $\sim$0.5--1.5 m. Additionally, two sites in Tennessee, USA, excavated to a depth of 50 cm revealed that 77.4% and 67.1% of total oak root biomass occurred in the upper 30 cm of soil [@Kelly1989]. Our method does not image fine roots; however, these are generally most abundant in the upper 10--30 cm and decrease in abundance with depth [@Millikin1999]. In semi-arid Californian oak savannas, coarse roots occupy the full soil profile and often accumulate near the soil--bedrock interface. Coarse-root abundance declines rapidly with increasing distance from the trunk, with $<$20% of coarse-root biomass beyond $\sim$2--3 m [@RazYaseef2013]. Classical trench studies in maple--oak forests likewise report a strong concentration of roots at shallow depths [@Scully1942].

```{figure} figures/Fig01_updatedMap.png
:name: fig-map

(a) Map of the study area showing GPR data collection, tree geometry, and surrounding vegetation. The base layer is a 2 cm-resolution relative elevation model generated via structure-from-motion. The relative elevation is set to the elevation at the base of the trunk. Thin black lines represent individual GPR profiles; thick black lines delineate angular grid boundaries extending approximately 12 m from the trunk. Data were collected over four days: sections 1--4 (day one), 5--8 (day two), 9--12 (day three), and 13--15 (day four). (b) Same as panel a, shown in polar coordinates. Colored points indicate the start of profiles referenced in Figure {numref}`fig-MigratedSections`.
```

# Methods

GPR is a geophysical technique widely used in urban, archaeological, and geological investigations [@Knight2001; @Neal2004; @Zajicova2019; @Jol2009; @Annan2009]. GPR operates by transmitting electromagnetic (EM) waves into the subsurface, where reflections occur at boundaries defined by contrasts in dielectric permittivity. The frequency of the transmitting antenna governs both resolution and penetration depth: higher frequencies yield finer resolution but shallower penetration due to increased signal attenuation per cycle [@Ozdemir2014; @Rehman2016]. In addition to antenna frequency, soils with high electrical conductivity reduce the depth of penetration of the signal [@Jol2009; @Annan2009].

This study employed a 500 MHz Sensors and Software antenna in a common-offset configuration. The transmitter (Tx) and receiver (Rx) were separated by 23 cm and mounted in a small sled that was dragged along the ground. The Tx was triggered every 1 cm using an odometer wheel. Data were collected at a sampling rate of 6.6 GHz with a time window of 70 ns. We used the 500 MHz antenna because it was within the 400--1000 MHz range that had been reported by others when using GPR to image tree roots [@Barton2004; @Cui2011; @Yamase2018].

## Acquisition

Tree roots are small subsurface targets that typically produce diffraction hyperbolae when intersected perpendicularly by the GPR antenna [@Butnor2001; @Molon2017]. Because coarse roots radiate outward from the trunk, circular survey profiles have been used [@Onaral2022; @Zhang2021; @Wu2014; @Lantini2020], but they introduce logistical complexity. To balance imaging quality with easy field data acquisition, we divided the survey area into 15 angular grid sections (Figure {numref}`fig-map`a). Each section was bounded by two tape measures extending from the trunk to the canopy edge ( 12 m). The tape measure endpoints were located using a total station.

GPR profiles were acquired at 15 cm intervals using a PVC guide placed at equal radial distances along each tape, creating straight-line transects between the tape measures (Figure {numref}`fig-acquisition`). Grids without obstructions contained 79 profiles. If another tree was within the angular grid (see Figure {numref}`fig-acquisition`), we did not attempt to circumvent it; those profiles were skipped or the section was truncated early. The angular-grid approach meant that the angles were not set beforehand; instead, they were laid out based on field observations. This allowed flexible deployment without prior site knowledge but also meant that sections were not exactly the same size. However, each grid shared an edge with the previous one to maintain spatial continuity (Figure {numref}`fig-acquisition`).

Grids were collected counterclockwise around the tree, beginning on the upslope side of section 1 (Figure {numref}`fig-map`a). In post-processing, profiles were concatenated (e.g., laid end-to-end) to approximate circular transects. Profile locations were also transformed into polar coordinates, with the tree center set as the origin. Angles follow mathematical convention, increasing counterclockwise from zero degrees starting on the right (Figure {numref}`fig-map`b).

Data collection spanned four days (12--16 August 2024), yielding 1170 profiles totaling 3.6 km of GPR data. Profile lengths ranged from 29 cm to 623 cm. Each section took approximately 45 minutes for a three-person team to complete. Sections 1--4 were collected on 12 August, 5--8 on 13 August, 9--11 on 14 August, and 12--15 on 15 August. A precipitation event occurred between 13 and 14 August, with 304.8 mm of rainfall recorded at the Clemson-Oconee County Airport (NWS Site KCEU),  5.2 km west of the site. The ground was dry during sections 1--4 and wet during sections 5--8; no further rainfall occurred during the remaining survey period.

```{figure} figures/Fig02_Field_Setup_and_Aquisition.png
:name: fig-acquisition

Photographs of the data acquisition setup using tape measures and PVC as guides. (a) View looking toward the oak from section 7, illustrating how the tapes were used to lay out a flexible angular grid; it highlights the shared edge and the zigzag pattern used to acquire the data. We skipped data where objects obstructed a straight path between the tapes, as illustrated by tree 3. (b) View of the tapes that trace the edges of the angular grid; the photo was taken looking away from the trunk along sections 7 and 8. (c) PVC was used as a guide for the GPR. Profiles were started and ended based on the midpoint between the two antennas.
```

## Processing

GPR data were processed using GPRPy [@Plattner2020], with additional routines implemented in NumPy [@Harris2020] and SciPy [@Virtanen2020]. The processing workflow consisted of three main stages (Figure {numref}`fig-ProcessingFlow`, Table {numref}`tab-gpr_params_short`): (1) estimating the root-mean-square velocity ($V_{RMS}$) using diffraction hyperbola analysis (light gray), (2) migrating the data using the estimated $V_{RMS}$ to collapse hyperbolae (light blue), and (3) applying depth-dependent gain to enhance root visibility prior to visualization.

Velocity estimation was essential for both migration and the time-to-depth conversion. The initial processing flow included standard steps: dewow filtering, mean trace subtraction, amplitude power gain, and band-pass filtering (Table {numref}`tab-gpr_params_short`). We did not apply a static correction prior to picking hyperbolae because the picks were made before construction of the high-resolution DEM and many profiles were short (the longest profile was approximately 6 m), so the elevation change across them was negligible.

Each GPR profile was trace-normalized to emphasize diffraction hyperbolae prior to picking them. Hyperbola geometry was analyzed in these processed common-offset profiles [@StClair2017; @Dou2017; @Dossi2024], where the shape and apex location are governed by $V_{RMS}$ and object depth [@Jol2009; @Neal2004]. A Python-based GUI was used to rapidly pick and fit hyperbolae across the dataset. The large number of picks enabled robust estimation of an average $V_{RMS}$, which was then used for migration. Details about the velocity-picking tool are provided in the Supplemental Material.

The visualization workflow was based on two assumptions. First, roots would appear as high-amplitude anomalies created by the collapse of diffraction hyperbolae during migration. This is consistent with prior studies showing roots as hyperbolic features in unmigrated profiles due to their small diameter and curved geometry [@Butnor2001; @Barton2004; @Zhu2014]. Second, the roots would appear as high‑amplitude anomalies because the migration re‑focused the scattered energy back to the source, creating small but bright high‑amplitude anomalies relative to the surrounding material.

```{figure} figures/Fig03_Methods_flow.png
:name: fig-ProcessingFlow

Diagram of the GPR processing workflow, divided into two main steps (light blue and light gray). Step one involved estimating the average EM velocity across the study area. Each profile was passed through standard preprocessing routines and then analyzed using a Python-based tool for rapid diffraction hyperbola picking based on semblance. Step two applied the estimated $V_{RMS}$ to migrate the data using FK migration. Migrated profiles were then geolocated and visualized.
```

```md
```{list-table} GPR processing parameters described in Figure {numref}`fig-ProcessingFlow`.
:name: tab-gpr_params_short
:header-rows: 1

* - Parameter
  - Value
* - Dewow
  - 1
* - Remove Mean Trace (traces)
  - 150
* - Exponent for Power Gain
  - 2
* - Hyperbola Width (m)
  - 2.5
* - Time Window (ns)
  - 20
* - Velocity Range (m/ns)
  - 0.05–0.15
* - Migration Velocity (m/ns)
  - 0.105



# Results

## Velocity Results

A total of 998 diffraction hyperbolae were identified across the 1170 GPR profiles (Figure {numref}`fig-VelocityResults`). The velocity distribution of all picked hyperbolae had a Gaussian shape (Figure {numref}`fig-VelocityResults`b). The mean and standard deviation of this distribution were 0.105 ± 0.017 m/ns (standard error = 0.001 m/ns). The range was quite large; however, 87.2% of the picked velocities fell between 0.08 and 0.13 m/ns. The depth distribution of the velocities from the hyperbolae showed that 75.9% were located above 60 cm, and 96% were within the top metre (Figure {numref}`fig-VelocityResults`c). No significant depth‑dependent velocity trends were observed. The maximum depth at which we observed a pickable hyperbola was 1.5 m. Although difficult to determine with certainty, 1.5 m likely represents the maximum depth of investigation. All profiles were migrated using FK migration with the mean velocity of 0.105 m/ns. Using a more complex migration algorithm that incorporated the spatial velocity information would likely improve the data; however, it extends beyond the scope of this paper.

In addition to these general observations, the velocity picks were mapped spatially (Figure {numref}`fig-VelocityResults`a). A higher density of hyperbolae was observed on the upslope side of the tree, where velocities were slightly lower than the mean (blue in Figure {numref}`fig-VelocityResults`). On the downslope side, the density of observations was lower, and the velocities were generally higher than the mean (red in Figure {numref}`fig-VelocityResults`).

When plotted as a function of azimuth, the velocities show a subtle decreasing trend following the precipitation event that occurred after the collection of data on day 1 (Figure {numref}`fig-VelocityAzimuth`). The decrease in velocity is observed in the means of windowed sections. A decrease in EM velocity is consistent with an increase in water content [@Topp1980; @Jol2009]. Rotating the azimuth so that the edge of the first section is set to zero, that is, visualizing the data in the order it was collected, makes this decreasing trend more obvious (Figure {numref}`fig-VelocityAzimuth`b). The mean velocities derived from all picked hyperbolae windowed by each day were 0.110 ± 0.017 m/ns (day 1), 0.108 ± 0.015 m/ns (day 2), 0.102 ± 0.016 m/ns (day 3), and 0.101 ± 0.017 m/ns (day 4). Although this trend is decreasing, determining its statistical significance would require more detailed analysis; given that a simple FK (single‑velocity) migration was used, such an investigation is beyond the scope of this paper.

The spatial distribution of picked hyperbolae also indicated signs of structural continuity. In Figure {numref}`fig-VelocityResults`a, symbol size corresponded to depth, with larger circles indicating that the picked hyperbola originated from greater depths. In several locations, coherent radial structures appeared to form by connecting the picks. These features emerged naturally, despite picks being made rapidly and independently on individual profiles. This suggested that the diffraction hyperbolae were not randomly distributed, but instead were generated by roots.

```{figure} figures/Fig04_velocity_combined.png
:name: fig-VelocityResults

Results from the detailed diffraction hyperbola velocity analysis. (a) Spatial distribution of selected diffraction hyperbolae. The velocity is colored by the percent difference from the mean (0.105 m/ns), where cooler colors indicate slower velocities and warmer colors indicate faster velocities. The symbol size corresponds to the depth of the picked hyperbola, where larger circles are from greater depths and smaller circles are shallower. (b) A plot of the velocity and depth from the hyperbola analysis. The depth was calculated using the picked $V_{RMS}$. The colors and sizes of the symbols are consistent with those shown in panel a. (c) Normalized histogram showing the velocity distribution of the picked hyperbolae. The distribution was Gaussian, with a mean and standard error of 0.0105 ± 0.001 m/ns. (d) A normalized distribution showing the depths of the picked hyperbolae.
```

```{figure} figures/Fig05_vel_with_azimuth.png
:name: fig-VelocityAzimuth

$V_{RMS}$ from picked diffraction hyperbolae plotted as a function of azimuth. Picks are coloured by acquisition day, with the black symbols and error bars showing the mean and standard deviation in 40° bins. The vertical blue line marks the precipitation event. (a) Velocities plotted as a function of azimuth shown in Figure {numref}`fig-map`b. (b) The same data plotted after shifting the azimuth so that the start of Section 1 (Figure {numref}`fig-map`a) is set to 0°, which places the observations in the order they were collected, moving counter‑clockwise around the tree.
```

## Root Visualization

A 27 m circular profile was constructed by laying the GPR profiles from all 15 angular grids end to end, which is traced out by the light blue line in Figure {numref}`fig-map`. This profile was also used to demonstrate the processing workflow (Figure {numref}`fig-ProcessingFlow`). For these data we calculated four amplitude curves by taking the mean amplitude from the Hilbert transform as a function of depth of dewowed and mean‑trace‑removed profiles (Figure {numref}`fig-AmplitudeGain`a). We used four profiles, as opposed to a single profile, to account for the precipitation event that occurred between days one and two, which altered shallow signal amplitudes. The near‑surface amplitudes of data collected on days 2 and 3 (sections 5--12) had higher amplitudes near the surface. These four curves were used for the amplitude normalization applied throughout the paper.

To illustrate the gain and processing flow we showed the unmigrated profile (Figure {numref}`fig-AmplitudeGain`b) expressed as ratios relative to the depth-specific mean. This means a value of five indicated an amplitude five times greater than the mean at that depth. The colors on top of the profile show which curve from Figure {numref}`fig-AmplitudeGain`a was used. This type of normalization, as opposed to the power gain used to identify hyperbolae, enhanced diffraction hyperbolae. In the unmigrated profile most of the diffractions appeared between 25 and 100 cm depth. The concatenated section maintained continuity across 15 individual profiles due to consistent field acquisition and alignment, because it is actually comprised of 15 profiles collected across four days.

Migration was performed using the estimated $V_{RMS} = 0.105~\text{m/ns}$, which collapsed diffraction hyperbolae into localized high‑amplitude anomalies (Figure {numref}`fig-AmplitudeGain`d). To illustrate the effects of subsequent processing we extracted three traces from the migrated section (Figure {numref}`fig-AmplitudeGain`c). The gray trace intersected an anomaly at approximately 110 cm, the cyan trace intersected one at approximately 50 cm, and the black trace intersected no anomaly. Multiple peaks were observed in the gray and cyan traces, suggesting possible anomalies or boundaries. The oscillatory nature of the GPR signal complicated direct interpretation and depth‑section construction.

To suppress oscillations and isolate amplitude anomalies, the envelope of the migrated section was calculated (Figure {numref}`fig-AmplitudeGain`e,f). These amplitudes were also normalized to the depth-specific curves shown in Figure {numref}`fig-AmplitudeGain`a. The envelope profile shows the areas where collapsed hyperbolae were bright anomalies. The extracted traces are more simplified because they are now single-peaked, corresponding to the collapsed hyperbolae (Figure {numref}`fig-AmplitudeGain`e).

To enhance contrast, the envelope was squared (Figure {numref}`fig-AmplitudeGain`g,h). This operation sharpened peaks and increased the visibility of high-amplitude anomalies. All subsequent figures used these squared, normalized envelope sections. In this space, a value of 8 corresponded to a signal 2.8× greater than the mean ($\sqrt{8}$). These anomalies formed the basis for all depth sections and spatial interpretations.

The continuity observed in depth sections and spatial slices was not produced by interpolation. Instead, it emerged from the alignment of discrete high‑amplitude anomalies across adjacent profiles (Figure {numref}`fig-AmplitudeGain`h). Looking at the profile in Figure {numref}`fig-AmplitudeGain`f,h, it would be impossible to determine if or which of those anomalies are roots. One of the key arguments is that these small, high‑amplitude anomalies will reveal dendritic structures with radial continuity from the trunk to the canopy edge. The data are now presented as squared amplitude data.

```{figure} figures/Fig06_GPR_Roots_Results_proifle21.png
:name: fig-AmplitudeGain

(a) Mean amplitude envelopes from all profiles collected on each survey day. Colors correspond to sections shown in Figure {numref}`fig-map`: blue (1--4), orange (5--8), purple (9--12), and red (13--15). (b) Unmigrated, gain-adjusted circular profile constructed by concatenating profiles from all sections. Amplitudes are normalized by the depth-dependent mean from panel a; color scale indicates relative amplitude. The profile is shown with 3× vertical exaggeration. (c) Three normalized amplitude traces extracted from the migrated section, corresponding to colored lines in panel d. (d) Migrated version of panel b, showing collapsed diffraction hyperbolae as bright anomalies. This represents the second step in the processing workflow (Figure {numref}`fig-ProcessingFlow`). (e) Three normalized envelope traces from the migrated section, corresponding to colored lines in panel f. (f) Envelope of panel d, with colormap scaled to highlight deviations from the depth-dependent mean in panel a. Blue indicates below-average amplitudes; red indicates above-average. (g) Three squared, normalized envelope traces from the migrated section, corresponding to colored lines in panel f. Squaring sharpens and emphasizes positive anomalies. (h) Squared, normalized envelope from panel f. Color scale reflects amplitude relative to the depth-specific mean; e.g., a value of 9 indicates an anomaly 3× greater than the mean ($\sqrt{9} = 3$). This scale is used throughout the remainder of the paper.
```

## Cross-Sections

Due to the high volume of data (1170 profiles), three circular and radial profiles were used to describe general observations (Figure {numref}`fig-MigratedSections`). Circular profiles were constructed by concatenating lines from the 15 angular grids collected at different distances from the tree and are shown in Figure {numref}`fig-map`. The continuity was maintained along these circular profiles because of the careful field acquisition and day-specific amplitude normalization. The profiles we show have also been shifted to account for topography from the high‑resolution DEM (Figure {numref}`fig-MigratedSections`).

Radial profiles exhibited greater continuity than circular profiles. Three radial sections extracted along angles of 97°, 238°, and 303° showed laterally continuous high-amplitude structures (Figure {numref}`fig-MigratedSections`a--c). These profiles originated near the trunk and extended toward the canopy edge and are marked in Figure {numref}`fig-map`b. The high-amplitude structures extended up to 10 m from the trunk and were formed by the alignment of features across more than 70 individual profiles. A zip folder containing profiles of all radial cross-sections at 1° intervals is provided in the supplemental material.

Circular profiles (Figure {numref}`fig-MigratedSections`d--f) showed limited continuity. These three profiles were extracted at radial distances of 4.5, 6.5, and 9.5 m, beginning at 0° and increasing counterclockwise around the tree (Figure {numref}`fig-map`). The circular sections were dominated by speckled anomalies and lacked laterally continuous high-amplitude structures. One exception was a structure located at approximately --0.5 m elevation between 22 and 25 m along the 4.5 m radius profile (Figure {numref}`fig-MigratedSections`d). This anomaly also appeared in intersecting radial profiles. In general, the high-amplitude density and amplitude decreased with increasing radial distance. The circular profiles shown in Figure {numref}`fig-MigratedSections`d--f are plotted as a function of distance and can also be plotted as a function of azimuth. Two zip files containing images from circular profiles extracted every 15 cm, plotted as azimuth and distance, are provided in the supplemental material.

```{figure} figures/Fig07_Amplitude_Profiles.png
:name: fig-MigratedSections

Processed GPR sections shown with 5× vertical exaggeration. Panels a--c are radial cross-sections at 97°, 238°, and 303°, respectively; panels d--f are circular cross-sections at radial distances of 4.5, 6.5, and 9.5 m. Circular profiles are plotted as a function of distance, with vertical dashed lines indicating intersections with corresponding radial profiles. In panels a--c, distance increases outward from the tree center (0 m). All profiles correspond to locations shown in Figure {numref}`fig-map`. Zip files containing images of radial sections in 1° increments and circular sections in 15 cm increments, plotted both as azimuth and distance, are provided in the supplemental material.
```

## Depth Sections

To visualize root distribution by depth, four depth slices were extracted: 0--25 cm, 25--45 cm, 45--65 cm, and 65--85 cm (Figure {numref}`fig-DepthSections`). Data were plotted in polar coordinates, with radial cross-sections from Figure {numref}`fig-MigratedSections`a--c shown as dashed lines. Each trace was treated as a discrete data point. For each depth range, amplitudes exceeding 2.5 times the mean were plotted as a scatter plot, sorted so that data points with stronger amplitudes were rendered on top. No interpolation was applied. Color scales matched those used in Figures {numref}`fig-AmplitudeGain` and {numref}`fig-MigratedSections`. Spatial continuity was generated by the alignment of high-amplitude anomalies across 1170 profiles.

The depth sections revealed complex, dendritic structures that varied with depth and radial position. At 0--25 cm, anomalies were concentrated near the canopy edge ($> 8~m$ radial distance; Figure {numref}`fig-DepthSections`a). Several features aligned with other trees visible in the DEM and appeared more frequently on the upslope side. At these shallow depths, the anomalies do not appear to connect back to the trunk.

Between 25--45 cm, the dendritic structures shifted inward. Several features extended from the trunk to distances of 8--10 m (Figure {numref}`fig-DepthSections`b). Complexity remained high, with branching patterns visible across multiple radial directions. At 45--65 cm, structural density decreased. Anomalies clustered closer to the trunk and appeared more frequently on the upslope side (60°--260°). A distinct feature extended radially to 10 m at 300°, with intersecting anomalies near 9 m and 30°. Below 60 cm, structures stabilized and became less intricate. The 65--85 cm section showed reduced amplitude and anomaly density, though the 300° feature remained visible. At these depths, the features appear to radiate from the trunk.

Static images did not fully capture the connectivity of these features. Supplemental images of depth sections showed that anomalies near the canopy edge at shallow depths connected to deeper structures toward the trunk. For example, features in the 0--25 cm section aligned with those in the 25--45 cm section. In the images, these anomalies appeared to shift inward with increasing depth, suggesting that roots were shallower near the canopy edge and deepened toward the trunk. All images showing depth sections from 0 to 1.5 m in 1 cm increments were provided as a .zip folder in the supplemental material.

```{figure} figures/DepthSections.png
:name: fig-DepthSections

Depth sections created by extracting the squared envelope (see Figure {numref}`fig-AmplitudeGain`c,d) from individual profiles. Data are plotted in polar coordinates and overlaid on a hillshade to show tree locations and topography. Radial grid lines indicate 1 m increments. A transparency mask was applied to suppress amplitudes below 30. Panels show depth slices at: (a) 5--25 cm, (b) 25--45 cm, (c) 45--65 cm, and (d) 65--85 cm. All images showing depth sections from 0 to 1.5 m in 1 cm increments were provided as a .zip folder in the supplemental material.
```

## Exploring the Data Volume

Cross-sections (Figure {numref}`fig-MigratedSections`) and depth sections (Figure {numref}`fig-DepthSections`) revealed complex spatial patterns. To examine the sensitivity of these structures to small (cm-scale) shifts in path lengths we look in detail at the root centered near 238°. This profile was chosen because the reflector was less prominent than those in the 97° and 303° profiles (Figure {numref}`fig-MigratedSections`b compared to Figures {numref}`fig-MigratedSections`a,c).

A depth section spanning 0--45 cm was constructed by combining data from Figure {numref}`fig-DepthSections`a and b. Using an interactive Python interface, we picked a path that traced along a visible root extending from the trunk toward another tree in the survey area. The path measured approximately 9 m and is shown in Figure {numref}`fig-PerspectiveView_gray`b. The path is more complex than the radial section, characterized by some cm deviations, but generally follows the same radial direction.

The cross-section extracted along this path revealed a continuous high‑amplitude structure extending from the trunk to the end of the profile. No interpolation was applied; each point was selected from the nearest trace within 1 cm, so the pixel width in Figure {numref}`fig-MigratedSections`a is approximately 15 cm (i.e., the angular grid line spacing). The profile extracted along the more complex path shown in Figure {numref}`fig-PerspectiveView_gray`b exhibited improved continuity. In other words, the reader should compare Figure {numref}`fig-MigratedSections`b to Figure {numref}`fig-PerspectiveView_gray`a. This path was drawn using the depth sections (Figure {numref}`fig-DepthSections`) to demonstrate that the high‑amplitude anomalies are sensitive to centimetre‑scale shifts in the extraction path, rather than to the spatial positioning of the antenna. Near the trunk, a shallow anomaly appeared to connect with a deeper, continuous structure at approximately 1 m elevation, suggesting a complex root origin. Toward the end of the profile, anomaly density increased near a second tree, consistent with patterns observed in the depth sections (Figure {numref}`fig-DepthSections`); the anomalies at this location appeared shallower. While the transition between root systems was not clearly defined, the continuous structure likely includes contributions from both trees.

```{figure} figures/Fig09_labeled.png
:name: fig-PerspectiveView_gray

Combined views illustrating how high-amplitude anomalies form complex dendritic structures. (a) 2D cross-section along a curved path near the 238° radial profile. Deviating from a straight radial path improves structural continuity (cf. Figure {numref}`fig-MigratedSections`b). (b) Depth section showing anomalies from 0--50 cm, combining data from Figure {numref}`fig-DepthSections`a and b. The path was selected based on the depth section and remains close to the radial profile; color indicates distance along path.
```

# Discussion

This study aimed to address the challenges associated with transforming GPR data into spatially coherent maps of root architecture. These challenges were addressed by collecting data using a unique angular grid and a processing workflow designed to emphasize the visibility and continuity of root anomalies.

We presented results from 1170 individual GPR profiles collected across 15 angular grid sections. This acquisition strategy simplified field deployment while maintaining a perpendicular orientation to roots radiating from the tree (Figure {numref}`fig-map`). The angular grid geometry enabled consistent alignment across profiles, which was critical for producing the observed spatial continuity of the root network.

The processing workflow optimized the visualization of high-amplitude anomalies created by the collapse of diffraction hyperbolae (Figure {numref}`fig-ProcessingFlow`). A detailed velocity analysis, based on 997 picked hyperbolae, revealed a mean electromagnetic velocity of 0.105 m/ns, with over 90% of picks occurring at depths shallower than 1 m (Figure {numref}`fig-VelocityResults`). These results suggested that the hyperbolae were not randomly distributed, but instead formed a spatially complex structure consistent with coarse root architecture.

Migrated radial cross-sections revealed continuous structures formed by the alignment of high-amplitude anomalies (Figure {numref}`fig-MigratedSections`a--c). In contrast, circular cross-sections appeared speckled, with high-amplitude anomalies resembling small bullseyes and lacking coherent patterns in individual slices (Figure {numref}`fig-MigratedSections`d--f). Depth sections showed that these bullseye anomalies formed dendritic structures that varied both spatially and with depth (Figure {numref}`fig-DepthSections`). At depths less than 25 cm, most structures appeared near the canopy edge at radial distances greater than 8 m (Figure {numref}`fig-DepthSections`a). Between 25--45 cm, the structures became more complex and connected to the trunk (Figure {numref}`fig-DepthSections`b). Below 50 cm, the structures stabilized and became less intricate, remaining close to the trunk (Figure {numref}`fig-DepthSections`c,d). The continuity observed in radial cross-sections was further enhanced by slight adjustments to the survey path (Figure {numref}`fig-PerspectiveView_gray`). These paths, selected using depth sections, demonstrated that anomaly visibility was sensitive to centimeter-scale shifts, underscoring the importance of acquisition geometry in resolving root structure.

From a geophysical perspective, it is remarkable that such a complex and spatially continuous structure emerged from short (no longer than 6 m) profiles. None of the images presented were interpolated. The alignment of high‑amplitude anomalies across independently collected profiles is the primary reason these features were interpreted as roots. Uncertainties remain, particularly because estimates of root depth and diameter depend on the velocity structure. Although we conducted a detailed velocity analysis, which indicated a slight decrease in velocities after a precipitation event, we still applied a single velocity for migration and depth conversion. Incorporating our observed lateral and vertical velocity variations could further improve image quality and reduce uncertainty in depth and dip estimates, but building the velocity model and using non-standard processing software to migrate was beyond the scope of the work here. Here, the diffractions collapsed and produced high-enough quality root maps.

The angular grid was designed so that GPR profiles crossed approximately perpendicular to radially oriented roots. The small line spacing (15 cm) likely reduced orientation bias, consistent with prior work showing that quarter‑wavelength (or finer) spacing minimises aliasing and that a single high‑density, unidirectional survey can outperform two orthogonal but sparser surveys [@Pierpaolo2015; @Grasmueck2005]. The strong spatial coherence of the anomalies therefore supports our choice of single‑velocity migration and dense spacing: the resulting volume images anomalies consistent with a continuous root system rather than isolated natural diffractions (e.g., corestones or other sharp interfaces). The only exception was a feature that appeared man‑made: a pair of linear structures intersecting at right angles between 46 and 65 cm depth, approximately 9 m from the tree at 30° (Figure {numref}`fig-DepthSections`c). Although the trees are not currently irrigated, this may represent a remnant irrigation pipe or buried infrastructure.

## Validation

To validate the root network observed in the GPR depth sections (Figure {numref}`fig-DepthSections`), we used the depth section maps to define a path to guide an airspade excavation. A perspective view and 2D cross-section of this selected path are shown in Figure {numref}`fig-airspade_gpr_validate`. The airspade effort was led by the South Carolina Botanical Gardens with in-kind support from [Bartlett Tree Experts](https://www.bartlett.com/). Prior to excavation, a total station was used to flag locations in the defined local coordinate system where the largest-diameter roots were expected. The path was chosen to begin near the trunk and extend toward the upslope side of the tree, where the majority of roots were concentrated.

This was a focused excavation effort, guided by flags laid out based on the geophysical data (Figure {numref}`fig-airspadeImages`a). Once the root was exposed, its diameter was measured at three locations: A (32 mm; Figure {numref}`fig-airspade_gpr_validate`b), B (8 mm; Figure {numref}`fig-airspade_gpr_validate`c), and C (14 mm; Figure {numref}`fig-airspade_gpr_validate`d). After measurements were taken, the soil was replaced to prevent disturbance to the South Carolina Botanical Garden operations. Unfortunately, root depths were not recorded because the total station was unavailable during excavation, and the airspade created shallow trenches with soil buildup around their edges, making it difficult to measure depth from the surface elevation. Excavation beyond point C was not possible due to consolidated soil that resisted removal by the airspade.

More extensive validation is needed, such as scanning a tree and then removing it to characterize the full root network. However, this study focused on an established tree, and further excavation was avoided to prevent harm or stress. Furthermore, the excavation took only half a day in a busy area with minimal disturbance. We acknowledge that additional ground-truthing measurements might be used to calibrate GPR data for estimating root diameter, as demonstrated in previous studies [@Zhu2014; @Fan2022; @Cui2011].

The airspade results align with previous studies demonstrating that GPR can resolve coarse root architecture under favorable conditions, particularly when acquisition geometry and processing workflows are tailored to root morphology. Similar to prior work, the data showed that diffraction hyperbolae collapsed into high-amplitude anomalies that, when spatially aligned, revealed dendritic root structures [@Barton2004; @Hruska1999]. This study detected roots, and velocity variations from the in-depth analysis suggested that results may be sensitive to soil moisture, root orientation, and survey design [@Butnor2001; @Zenone2008].

```{figure} figures/Fig10_Airspade_validation_2of2.png
:name: fig-airspadeImages

Images from the airspade excavation guided by the GPR data shown in Figure {numref}`fig-airspade_gpr_validate`. (a) View looking toward the oak tree, with points A, B, and C marked as dots. (b) Root exposed at point A, measuring 32 mm in diameter. (c) Root exposed at point B, measuring 8 mm in diameter. (d) Root exposed at point C, measuring 14 mm in diameter.
```

```{figure} figures/Airspade_validation_1of2.png
:name: fig-airspade_gpr_validate

Multiple perspectives from the GPR data volume used to guide airspade excavation. Locations A, B, and C correspond to those shown in Figure {numref}`fig-airspadeImages`a. (a) A 3D perspective view illustrating the complexity of the root network beneath the airspade transect. (b) An alternate perspective view, similar to Figure {numref}`fig-airspade_gpr_validate`a. (c) A 2D cross-section beneath the airspade transect, with locations A, B, and C plotted. The thickened segments of the dashed line represent estimated root diameters. Depths were not recorded and are manually placed on strong reflectors. (d) A depth section from 0 to 45 cm, with points A, B, and C plotted on the map.
```

## Root Distribution and Probability Maps

The unique volume of data and structural insights from the non-invasive dataset were used to estimate the probability of encountering a root. For this analysis, a root was assumed to be indicated by an amplitude threshold of 6, corresponding to anomalies approximately 2.5 times greater than the average amplitude at any given depth. These anomalies appeared as light purples, browns, and blacks in the colormaps used to display the data (see Figure {numref}`fig-MigratedSections`). Because only one root was validated through excavation, this section is presented as a potential application of the methodology, with the understanding that further ground-truthing is required.

Using the full dataset, the probability of encountering a root---defined as an amplitude exceeding the threshold---was calculated. From a top-down perspective, the study area was divided into bins with radial widths of 35 cm and angular widths of 2 degrees (Figure {numref}`fig-probabilityMaps`a). Squared amplitude values from all data points in a bin were used to construct a probability density function using Gaussian kernels implemented in SciPy [@Virtanen2020]. The probability density function was integrated to estimate the likelihood of encountering an amplitude above 6 in each bin (Figure {numref}`fig-probabilityMaps`a). A similar approach was used to estimate probability along the radial direction, using the same radial bin width and a depth bin width of 6 cm (Figure {numref}`fig-probabilityMaps`b). In this space, a perfectly oriented radial root would appear as a bullseye. Probability was also estimated around the tree using 2-degree azimuth bins and 6 cm depth bins (Figure {numref}`fig-probabilityMaps`c).

These probability maps, while specific to the tree studied, provided a way to visualize root distribution. From the map view, a high probability of encountering a root was observed between 90° and 270° (Figure {numref}`fig-probabilityMaps`a). Between 100° and 225°, the probability was notably lower. This pattern was reinforced in the azimuth-depth view (Figure {numref}`fig-probabilityMaps`c), which also showed that most roots occurred between 0.25 and 0.75 m depth. From a radial perspective, the majority of roots were located between 3 and 6 m from the tree at a depth of approximately 50 cm (Figure {numref}`fig-probabilityMaps`b). A secondary cluster of deeper roots was observed between 9 and 13 m from the tree, likely reflecting elevation changes that caused roots to grow deeper into the hillslope.

In these data, the highest probability of encountering a root occurred on the upslope side of the tree, which was also exposed to wind (Figure {numref}`fig-probabilityMaps`). Trees are known to preferentially grow roots where additional mechanical support is needed [@Chiatante2002]. Different species exhibit varying mechanical properties, with some roots stronger in tension and others in compression [@Potocka2018]. Roots may also structurally adapt, forming I-beams and T-beams to enhance anchorage [@Nicoll1996; @Coutts1983; @Iorio2005; @Tamasi2005]. Although these data cannot resolve root shape, they clearly revealed where the largest and coarsest roots were located.

The compiled probability results may be used to inform models that constrain root orientation and location. They also offer a promising tool for comparative studies of tree species and root distribution patterns. While scanning this tree required four days, the process was exploratory and included refinement of the angular grid configuration. With automation---such as track-mounted systems or unmanned ground vehicles---similar scans could be completed in a single day or less. This would enable broader surveys across species, ages, and environments, including protected trees, with minimal disturbance and limited ground-truthing.

```{figure} figures/Probability_roots.png
:name: fig-probabilityMaps

The probability of encountering a root, defined as a high-amplitude anomaly with a value greater than six. (a) Map view in radial coordinates, which includes all data contained in bins with radial widths of 35 cm and angular widths of 2 degrees. (b) The probability of encountering a root computed by binning all the data in 35 cm radial bins and 6 cm depth bins. (c) The probability of encountering a root computed by binning all the data in 2-degree bins and 6 cm depth bins.
```

## Implications and Future Development

This study demonstrated that high-density GPR data, when paired with a tailored acquisition strategy and depth-sensitive processing workflow, revealed spatially continuous root structures without interpolation. The ability to visualize dendritic networks and trace individual roots across dozens of profiles indicated that GPR is not only a mapping tool but also a means of exploring root architecture in situ. These insights have implications for studies of slope stability, carbon storage, and subsurface hydrology, where root geometry plays a critical role.

However, several challenges remain. Depth estimation depended on accurate velocity modeling, and root diameter could not be reliably inferred from signal amplitude alone. The sensitivity of anomaly continuity to centimeter-scale shifts in survey geometry highlighted the need for adaptive acquisition strategies and automated path optimization. Future work should explore integration with other geophysical methods (e.g., ERT), machine learning-based anomaly classification, and 3D reconstruction techniques capable of resolving overlapping root systems. Ultimately, the development of standardized workflows and validation protocols will be essential for translating GPR-derived root maps into ecological and engineering applications.

# Conclusion

This study addressed the challenge of transforming GPR data into spatially coherent maps of root architecture by developing a tailored acquisition and processing strategy. The angular grid geometry maintained a perpendicular orientation to radially extending roots, improving anomaly clarity and mitigating limitations in survey design. A multi-stage processing workflow, including velocity analysis, migration, and depth-normalized amplitude enhancement, enabled the visualization of dendritic root structures without interpolation.

The results demonstrated that high-amplitude anomalies, when spatially aligned across profiles, revealed a continuous root network consistent with coarse root architecture. The sensitivity of anomaly continuity to centimeter-scale shifts highlighted the importance of acquisition geometry and suggested the potential for adaptive path selection. While small-diameter roots remained difficult to resolve, the combined innovations in acquisition and processing represent meaningful progress toward overcoming long-standing barriers in GPR-based root system mapping.

# Acknowledgments

This research was supported by startup funding from Clemson University. We gratefully acknowledge Bartlett Tree Experts for their logistical support and interest in advancing tree root imaging technologies. We thank William Cummings, Annalee Chiaviello, and Rachel Uecker for their invaluable assistance with data acquisition and fieldwork. This study builds upon the foundational work of Megan Lapkoff, whose M.S. thesis Ground-Penetrating Radar Imaging of Tree Root Architecture laid the groundwork for our angular grid acquisition approach. Although her work could not be published due to limitations in full-tree scanning and ground-truthing, it was instrumental in shaping the design and methodology of this project. We also acknowledge Dr. Nadarajah Ravichandran and Clemson University for early conversations---initiated over five years ago---that inspired the use of ground-penetrating radar to image tree roots. His insights helped catalyze the conceptual development of this research. During the preparation of this work Brady A. Flinchum used Microsoft Co-Pilot (Enterprise Protected) to help smooth langauge. After using this tool/service, the authors have reviewed and edited the content as needed and take full responsibility for the content of the published article.


## References

```{bibliography}
:filter: docname in docnames
:style: unsrt
```
