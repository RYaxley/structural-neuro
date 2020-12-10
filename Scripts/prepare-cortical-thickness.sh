#!/usr/local/bin/tcsh -f
#!/bin/bash

set datapath = /Animal/rodent/Crews/NADIA/RPV9/Processing/CorticalThickness
# RPV9 
# 27=left
# 19=right
# 21=olf bulb

foreach i ( $datapath/002*segmentation*cortexsplit.nii.gz )

	set right = $datapath/$i:t:s/.nii.gz/_R.nii.gz/
	set left  = $datapath/$i:t:s/.nii.gz/_L.nii.gz/
	set brain = $i:s/.nii.gz/_brain.nii.gz/
	set rightsmooth = $right:s/.nii.gz/_spp.nii.gz/
	set leftsmooth  = $left:s/.nii.gz/_spp.nii.gz/
	set brainsmooth = $brain:s/.nii.gz/_spp.nii.gz/
	
	# Merge non-neocortex regions into one label #1
	if ( -e $brain ) then
		echo $brain 'already exists. Not regenerating.'
	else
		/tools/bin_linux64/MergeLabels $i $brain -l 1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,25,26,28
	endif
	
	# Extract regions and and change labels
	ImageMath $brain -outfile $brain -extractLabel 1
	ImageMath $i -outfile $right -extractLabel 19
	ImageMath $i -outfile $left  -extractLabel 27
	ImageMath $right -outfile $right -constOper 2,2
	ImageMath $left  -outfile $left  -constOper 2,2

	# Smooth
	SegPostProcess $right -Gauss -var 0.15 -o $rightsmooth
	SegPostProcess $left  -Gauss -var 0.15 -o $leftsmooth
	SegPostProcess $brain -Gauss -var 0.15 -o $brainsmooth

	# Combine brain to cortex labelmaps
	ImageMath $rightsmooth -outfile $rightsmooth -add $brainsmooth
	ImageMath $leftsmooth  -outfile $leftsmooth  -add $brainsmooth
	
	# I could mask the brain region by the cortical label maps and then add.
	

	# # Add 1 to all labels, so that background=1, subcortex=2, cortex=3
	# ImageMath $rightsmooth -outfile $rightsmooth -constOper 0,1
	# ImageMath $leftsmooth  -outfile $leftsmooth  -constOper 0,1
	
	# rm $brain

	
end
