from numebot.round_manager import RoundManager

from numebot.env import NUMERAI_DATA_FOLDER
from numebot.secret import PUBLIC_ID, SECRET_KEY

print('\nRunning numebot public\n')

rm = RoundManager(
    NUMERAI_DATA_FOLDER, 
    public_id=PUBLIC_ID, 
    secret_key=SECRET_KEY,
#    nrows=10000, testing=True,
)

rm.models_info()
rm.generate_predictions_for_all_models()
rm.submit_predictions()
