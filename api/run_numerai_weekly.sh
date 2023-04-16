#!/bin/bash

#source /home/pica/anaconda3/bin/activate automl
echo "Running with poetry"
cd /home/pica/workspace/numebot || exit

LOG_PATH=/home/pica/nas_pica/Data/numerai/weekly_log/log_numerai_"$(date +"%Y-%m-%d_%H%M%S")".txt
poetry run python api/run_it.py |& tee "$LOG_PATH"
