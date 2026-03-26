Interactive Roots
=================

This page demonstrates how to embed interactive 3D figures using the
``.. pyvista-plot::`` directive. Each figure automatically gets a
**Static Scene** tab (a screenshot) and an **Interactive Scene** tab
(fully rotatable/zoomable in the browser — no Python server needed).

Write your figures as plain ``.py`` scripts in Spyder, then paste the
code into a ``.. pyvista-plot::`` block. That's it.

Test of my data
---------------

.. pyvista-plot::
   :caption: A sphere coloured by distance from an offset point.
   :include-source: True
   import pyvista as pv
   import numpy as np
   import yaml

   # Load data
   elvGrid = pv.read("elvGrid.vtk")
   pts1 = pv.read("xyzPoints.vtk")
   pts2 = pv.read("xyzPoints2.vtk")
   validate = pv.read("validate_points.vtk")

   npz = np.load("plot_data.npz")
   avgAmp = npz["avgAmp"]
   avgAmp2 = npz["avgAmp2"]
   vMin = npz["vMin"]
   vMax = npz["vMax"]
   VE   = npz["VE"]

   with open("plot_config.yml") as f:
       cfg = yaml.safe_load(f)

   pts1["avgAmp"] = avgAmp
   pts2["avgAmp"] = avgAmp2

   # Plot
   p = pv.Plotter()
   p.set_background("white")

   p.add_mesh(elvGrid,
           opacity=cfg["opacity_elv"],
           cmap="gray",
           clim=[0, 2],
           show_scalar_bar=False)

   p.add_points(pts1,
             scalars="avgAmp",
             style="points_gaussian",
             point_size=cfg["point_size"],
             cmap=cfg["cmap_points"],
             clim=[vMin, vMax],
             opacity="sigmoid",
             lighting=False)

   p.add_points(pts2,
             scalars="avgAmp",
             style="points_gaussian",
             point_size=cfg["point_size"],
             cmap=cfg["cmap_points"],
             clim=[vMin, vMax],
             opacity="sigmoid",
             lighting=False)

   p.add_points(validate,
             color="red",
             point_size=10,
             render_points_as_spheres=True)

   p.camera_position = cfg["camera_position"]
   p.set_scale(zscale=VE)

   p.show()


