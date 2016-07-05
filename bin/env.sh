source env/bin/activate
export PYTHONPATH=`pwd`/src
alias run="python `pwd`/src/test.py"
alias api_count="cat `pwd`/src/tests/*.py|grep 'global_params.post'|awk -F \"'\" '{print \$2}' | sort |uniq -c |wc -l"

