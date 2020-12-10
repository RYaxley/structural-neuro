#!/usr/local/bin/tcsh -f
#!/bin/bash


set datapath = /Animal/rodent/Crews/NADIA/RPV9/Processing/CorticalThickness

foreach i ( $datapath/*segmentation*cortexsplit.nii.gz )

	set right = $datapath/$i:t:s/.nii.gz/_R.nii.gz/
	set left  = $datapath/$i:t:s/.nii.gz/_L.nii.gz/
	set temp  = $datapath/$i:t:s/.nii.gz/_temp.nii.gz/
	set brain = $i:s/.nii.gz/_brain.nii.gz/
	echo $i $right $left $brain
	'''
	# 14 = left cortex
	# 29 = right cortex with my latest test. i need to fix this
	# 16 = olfactory bulb
	#
	# RPV9 
	# 27=left
	# 19=right
	# 21=olf bulb

	# Merge non-neocortex regions into one label #1
	if ( -e $brain ) then
		echo $brain 'EXISTS'
	else
		/tools/bin_linux64/MergeLabels $i $brain -l 1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,25,26,28
	endif

	# Remove olfactory bulb
	set obulb = 21
   	ImageMath $brain -outfile ${datapath}/${obulb}.nii.gz -extractLabel $obulb
	ImageMath ${datapath}/${obulb}.nii.gz -outfile ${datapath}/${obulb}.nii.gz -constOper 2,${obulb}
	ImageMath $brain -outfile $brain -sub ${datapath}/${obulb}.nii.gz
	rm ${datapath}/${obulb}.nii.gz

	# Extract right and left cortices  and change labels. NEED TO FLIP THESE LABELS????
	ImageMath $i -outfile $right -extractLabel 19
	ImageMath $right -outfile $right -constOper 2,19
	ImageMath $i -outfile $left -extractLabel 27
	ImageMath $left -outfile $left -constOper 2,27

	cp $right $temp
	ImageMath $brain -outfile $right -sub $left
	ImageMath $brain -outfile $left -sub $temp
	rm $temp
	rm $brain
	
	###  cmd = 'SegPostProcess %s -Gauss -var 0.1,0.1,0.1 -o %s' % (file, ofid )

	# Reset values of cortex to 2. NEED TO FLIP THESE LABELS
	MergeLabels $right $right -l 2,19
	MergeLabels $left $left -l 2,27

	# Add 1 to all labels, so that background=1,subcortex=2,cortex=3
	ImageMath $right -outfile $right -constOper 0,1
	ImageMath $left  -outfile $left  -constOper 0,1

	MedianImageFilter $right $right:s/.nii.gz/_m.nii.gz/ --neighborhood 1,1,1
	MedianImageFilter $left  $left:s/.nii.gz/_m.nii.gz/  --neighborhood 1,1,1
	#SegPostProcess $right -Gauss -var 0.1,0.1,0.1 -o $right:t:s/.nnrd/_smooth.nrrd/
	#SegPostProcess $left  -Gauss -var 0.1,0.1,0.1 -o $left:t:s/.nnrd/_smooth.nrrd/
	
	'''

end
