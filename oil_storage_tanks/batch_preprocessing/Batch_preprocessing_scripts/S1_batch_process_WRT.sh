#!/bin/bash

#Path variables must be defined here

path_input=/media/rose/Samsung_T51/Togodo/data/
path_output_VH=/media/rose/Samsung_T51/Togodo/Process_data/VH/
path_output_VV=/media/rose/Samsung_T51/Togodo/Process_data/VV/

#Definition of local variables

extension=.zip
VH_data=_VH
VV_data=_VV

#Extraction of data and execution of GPT command. The corresponding preprocessing graph (xml file) should be set as parameter

"""We browse through the folder and read all the elements that fulfill the requirement.
 For all files in path_input that start with 'S1' and finish with '.zip' do
	Extract the sensing time of image in variable m
	Call gpt command
	gpt <xml_graph_file.xml> ...
 End"""

c=1
date
for j in $(ls $path_input$S1*.zip)
	do
		# 
		echo Traitement : $c
		m=${j%.*}
		m=${j%T*}
		m=${m#"${m%_*}_"}
		date
		gpt /home/rose/acquisition_traitement_auto/SNAP_process/gpt_batch_processTogodo.xml -Pinput_data=$j -Poutput_data1="$path_output_VH$m$VH_data" -Poutput_data2="$path_output_VV$m$VV_data"
		#c=$((c+1))
		
		date
	done

date	

