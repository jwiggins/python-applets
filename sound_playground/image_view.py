
from chaco.api import Plot, ArrayPlotData
from chaco.default_colormaps import gray
from traits.api import Array


class ImageView(Plot):
    default_origin = 'top left'

    image = Array

    # traits handlers

    def __init__(self, **kw):
        super(ImageView, self).__init__(**kw)

        if self.data is None:
            self.data = ArrayPlotData()
        self.data.set_data('image', self.image)

        self.img_plot('image', colormap=gray)
        self.x_axis = None
        self.y_axis = None
        self.padding = [0, 0, 0, 0]

    def _image_changed(self):
        if not self.traits_inited():
            return
        self.data.set_data('image', self.image)
