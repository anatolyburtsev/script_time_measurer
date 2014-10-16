script_time_measurer
====================

script for measure the time of script and save result in graphite

write it before your script in crontab and it send the runtime of your script in graphite

for ex:

0 *  * * * root rm -rf /*

modify to 

0 *  * * * root python_bash_tm.py rm -rf /*
