from numebot.round_manager import RoundManager

from numebot.secret import PUBLIC_ID, SECRET_KEY


data_folder = '/home/pica/nas_pica/Data/numerai/'

rm = RoundManager(
    data_folder, 
    public_id=PUBLIC_ID, 
    secret_key=SECRET_KEY,
#    nrows=10000, testing=True,
)

rm.models_info()
rm.generate_predictions_for_all_models()
rm.submit_predictions()
