# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR
#. ./tasks/environment.sh
. tasks/environment.sh



# activate the virtual environment for python
#. env/bin/activate
. env/bin/activate


python manage.py report 
