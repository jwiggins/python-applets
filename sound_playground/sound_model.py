import librosa as lr
import numpy as np
from PIL import Image
from pyaudio import PyAudio
from skimage import img_as_float
from skimage.color import rgb2gray

from traits.api import (HasStrictTraits, Array, Bool, File, Instance, Int,
                        on_trait_change)

from image_view import ImageView

IMAGE_SIZE = (512, 512)


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
    img.draft('L', IMAGE_SIZE)
    arr = np.array(img)
    if arr.ndim == 3:
        return rgb2gray(arr)
    return arr


def _spec(image):
    real_image = img_as_float(image)
    imag_image = 1.0 - real_image
    comp_image = real_image + 1j * imag_image
    return lr.istft(comp_image)


class SoundModel(HasStrictTraits):
    filename = File()

    image_view = Instance(ImageView)

    created_sound = Array()

    _audio_lib = Instance(PyAudio, args=())

    transpose_image = Bool(False)

    sample_rate = Int(22050)

    def _image_view_default(self):
        image = np.zeros(IMAGE_SIZE, dtype=np.uint8)
        return ImageView(image=image)

    def _filename_changed(self, new):
        if _is_data_file(new):
            self.image_view.image = _load_image(new)
            self.image_view.request_redraw()
            self._clear_sound()

    @on_trait_change('transpose_image,sample_rate')
    def _clear_sound(self):
        self.created_sound = np.ndarray(shape=(0,))

    def play_sound(self):
        if len(self.created_sound) == 0:
            img = self.image_view.image
            sound = _spec(img.T if self.transpose_image else img)
            self.created_sound = lr.util.normalize(sound)

        stream = self._audio_lib.open(
            format=1, channels=1, rate=self.sample_rate, output=True
        )
        stream.write(self.created_sound)
        stream.stop_stream()
        stream.close()
