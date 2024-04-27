# Teldyne FLIR Camera (Monitoring of gel extrsuion from needle)
### Example of broken Extrusion
![NZ196](https://github.com/Roy-Praveen/FLIR-camera-based-monitoring-of-Extrusion/assets/93182817/cf2b3e67-9b24-4a14-b421-458ca3d2aeb1)

### Example of non broken Extrusion
![N161](https://github.com/Roy-Praveen/FLIR-camera-based-monitoring-of-Extrusion/assets/93182817/c72d3cbb-d28b-47c2-8dc8-03c6fdc597fd)

This is a sample of my work carried out at Next Big Innovation Labs Pvt Ltd.
Segmentation of gel which is being extruded from a needle in 3D bioprinters is carried out using Yolov8.
The segmentation maps are classified into broken gels and unbroken gels using a CNN based feature extractor.
The user can experiment with various feature extractors to segment their objects.

### Graphical Example of Segmentation of Needle and Gel
![label](https://github.com/Roy-Praveen/FLIR-camera-based-monitoring-of-Extrusion/assets/93182817/010b3a21-9dcf-41e0-9341-d898bfb0a12d)

### Teledyne FLIR camera

The run.py is a hacked version of the acquire and display python script of the Spinnaker SDK.
Remember to direct to your model.pt file.

### Other scripts
The other scripts have been written in a OOP format as adviced by NBIL.

### High Level Function
The script basically measures your gel which is in red color relative to the size of the needle which is in green color.
The output will show the percentage of how small or big the gel is relative to the needle.
This output can be used to regulate pressure of 3D bioprinters to avoid under extrusion, over extrusion and even automate quality control.
