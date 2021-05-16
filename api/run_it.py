from numebot.round_manager import RoundManager

from numebot.env import NUMERAI_DATA_FOLDER, MODEL_CONFIGS_PATH
from numebot.secret import PUBLIC_ID, SECRET_KEY

print('\nRunning numebot public\n')

rm = RoundManager(
    numerai_folder=NUMERAI_DATA_FOLDER, 
    model_configs_path=MODEL_CONFIGS_PATH,
    public_id=PUBLIC_ID, 
    secret_key=SECRET_KEY,
#    nrows=10000, testing=True,
)

rm.models_info()
rm.generate_predictions_for_all_models()
rm.submit_predictions()
_ = rm.mm.download_round_details()
