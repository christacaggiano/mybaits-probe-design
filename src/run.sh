#!/bin/bash                         

#$ -S /bin/bash                     
#$ -cwd                            
#$ -r y                            
#$ -j y                           
#$ -l mem_free=30G                 
#$ -l arch=linux-x64               
#$ -l netapp=10G,scratch=15G         
# #$ -l h_rt=24:00:00   

conda activate py36 
python run.py 
echo "finished"

