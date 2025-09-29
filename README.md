Code to generate SOLWEIG model inputs and run simulations  
Two ways to generate DSM inputs, using LiDAR or datasets on GEE  
Use the below script to generate DSMs in GEE:  
https://code.earthengine.google.com/22efdf1049c9b0216b471aea9a8f5500

STEPS FOR INPUT DATA PROCESSING: 
1. Generate DSMs. Use GEE script or DM_creation_pdal.ipynb for LiDAR data. (note, need to add DEM only)
2. Generate Met Data. Download met data from ERA5 reanalysis, then run Met_Data_Prep.ipynb.

STEPS FOR CREATING SIMULATIONS:
1. Run on longleaf (faster, but need GPUs) - or run via QGIS (much slower)

STEPS FOR RUNNING SIMULATIONS 
1. 
