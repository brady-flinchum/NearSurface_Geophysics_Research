PyVista Demo
============

This page demonstrates how to embed interactive 3D figures using the
``.. pyvista-plot::`` directive. Each figure automatically gets a
**Static Scene** tab (a screenshot) and an **Interactive Scene** tab
(fully rotatable/zoomable in the browser — no Python server needed).

Write your figures as plain ``.py`` scripts in Spyder, then paste the
code into a ``.. pyvista-plot::`` block. That's it.

Basic mesh with scalar field
-----------------------------

.. pyvista-plot::
   :caption: A sphere coloured by distance from an offset point.
   :include-source: True

   import pyvista as pv
   import numpy as np

   mesh = pv.Sphere(radius=1.0, theta_resolution=60, phi_resolution=60)

   center = np.array([0.5, 0.5, 0.5])
   distances = np.linalg.norm(mesh.points - center, axis=1)
   mesh['distance'] = distances

   pl = pv.Plotter()
   pl.add_mesh(mesh, scalars='distance', cmap='viridis',
               show_scalar_bar=True, scalar_bar_args={'title': 'Distance'})
   pl.add_axes()
   pl.show()


Loading your own data
---------------------

In Spyder, develop your script normally with ``pl.show()`` to preview it.
When you're happy, paste the code into a ``.. pyvista-plot::`` block here.

.. pyvista-plot::
   :caption: Reading a VTK file — replace the filename with your own data.
   :include-source: True

   import pyvista as pv

   # Replace with your own file:
   #   mesh = pv.read('path/to/your/file.vtk')
   # For this demo we use a built-in example:
   mesh = pv.examples.load_globe()

   pl = pv.Plotter()
   pl.add_mesh(mesh, smooth_shading=True)
   pl.add_axes()
   pl.show()


Tips
----

- Develop in Spyder with ``pl.show()`` as normal — that gives you the
  live trame window locally.
- When ready to publish, paste the same code into a
  ``.. pyvista-plot::`` block. No changes needed.
- The directive runs the code at build time, so your figures are always
  up to date when you push.
- You can have as many ``.. pyvista-plot::`` blocks as you want on one page.
