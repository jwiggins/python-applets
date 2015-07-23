import librosa as lr
import numpy as np
from PIL import Image
from pyaudio import PyAudio
from skimage import img_as_float

from traits.api import HasStrictTraits, File, Instance

from image_view import ImageView


def _is_data_file(filename):
    """ Determine if filename points to a file that we care about.
    """
    try:
        img = Image.open(filename)
        img.verify()
    except:
        return False
    return True


def _load_image(filename):
    img = Image.open(filename)
    img.draft("L", (512, 512))
    return np.array(img)


def _spec(image):
    real_image = img_as_float(image)
    imag_image = 1.0 - real_image
    comp_image = real_image + 1j * imag_image
    return lr.istft(comp_image)


class SoundModel(HasStrictTraits):
    filename = File()

    image_view = Instance(ImageView)

    audio_lib = Instance(PyAudio, args=())

    # traits handlers

    def _image_view_default(self):
        image = np.zeros((255, 255), dtype=np.uint8)
        return ImageView(image=image)

    def _filename_changed(self, new):
        if _is_data_file(new):
            self.image_view.image = _load_image(new)
            self.image_view.request_redraw()

    def play_sound(self):
        sound = _spec(self.image_view.image)
        sound =  lr.util.normalize(sound)
        stream = self.audio_lib.open(format=1, channels=1, rate=11025,
                                     output=True)
        stream.write(sound)
        stream.stop_stream()
        stream.close()
