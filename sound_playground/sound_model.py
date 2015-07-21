import numpy as np
from PIL import Image

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
    img.draft("L", (256, 256))
    return np.array(img)


class SoundModel(HasStrictTraits):
    filename = File()

    image_view = Instance(ImageView)

    # traits handlers

    def _image_view_default(self):
        image = np.zeros((255, 255), dtype=np.uint8)
        return ImageView(image=image)

    def _filename_changed(self, new):
        if _is_data_file(new):
            self.image_view.image = _load_image(new)
            self.image_view.request_redraw()

    def play_sound(self):
        print "This is a sound"
