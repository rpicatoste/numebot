#!/bin/bash
source /home/pica/anaconda3/bin/activate automl
cd /home/pica/workspace/numebot || exit

LOG_PATH=/home/pica/nas_pica/Data/numerai/weekly_log/log_numerai_"$(date +"%Y-%m-%d_%H%M%S")".txt
python api/run_it.py |& tee "$LOG_PATH"
