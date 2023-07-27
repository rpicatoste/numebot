#!/bin/bash

echo "Running with anaconda"
cd /home/pica/workspace/numebot || exit
source /home/pica/anaconda3/bin/activate automl

LOG_PATH=/home/pica/nas_pica/Data/numerai/weekly_log/log_numerai_"$(date +"%Y-%m-%d_%H%M%S")"_anaconda.txt
python api/run_it.py |& tee "$LOG_PATH"
