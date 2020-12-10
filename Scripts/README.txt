March 7, 2014

Dataset: RPV9

Scans acquired by Al Johnson at DUMC Center for InVivo Microscopy

* * *

# DATA DOWNLOAD INSTRUCTIONS

DUMC Center for InVivo Microscopy
Bryan Research Building, Rm. 129
311 Research Drive, Box 3302
Durham, North Carolina  27710
http://www.civm.duhs.duke.edu

* * *

# NOTES ON DATA

Correct, it is not in DICOM format. You can choose to download the 3D-Tiff
or the gzipped-tarfile with is the raw data with no header.

a) dimensions/number of voxels in each dimension

X=800
Y=400
Z=320


b) voxelsize in each dimension (I think 50micrometer isotropic, but I am
not sure)

Voxel Dimensions: .05 x .05 x .05mm


c) datatype (unsigned short integer, big-endian byte order)
16-bit = unsigned


Are there 4 images per scan, or this only one image which constitutes the
sum of the 4 original images?

No, there are 320 images per run number. For example: S64938_m0 is a run
number. Within that run there are 320 images. So for the first specimen
listed: 140303-9:1, there are 4 run numbers each with 320 images.

--

We acquired a multi gradient recalled echo @ 50 um isotropic resolution. There are thus 4 3D data sets in each run with the expected T2* decay. We have had good luck in the past in adding the data. I'm playing with options at the moment and hope to play around a little more tonight. It's a bit trickey to make fair comparisons of SNR and CNR unless one is very specific about which 2 tissues one wants to delineate. I'm sure you know the problems.
	My suggestion is that you pull a couple of data sets over and see what you think. The run nos have extensions m0,m1,m2,m3 indicating the successive echoes. 
	
* * *


Duke is providing an atlas of Wister @ P80 with ~30 structures, multicontrast, oriented in Paxinos-Watson space. 2 types of images (graident recalled echo) @ 25 microns. Also, 6 b-value DTI set @ 50 microns.

