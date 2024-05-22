from melo.api import TTS
from pathlib import Path
import warnings


warnings.filterwarnings('ignore')


def load_meloTTS_model(speed):
    device='auto'
    model = TTS(language='ES', device=device)
    speakers_ids = model.hps.data.spk2id

    return model, speakers_ids, speed

