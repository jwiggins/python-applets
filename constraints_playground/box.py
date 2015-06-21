
from random import choice

from enable.api import Component, color_table
from kiva.trait_defs.kiva_font_trait import KivaFont


class Box(Component):
    """ A simple box component that draws its id string.
    """
    # We want our border to show
    border_visible = True

    # A font for drawing with
    font = KivaFont("DEFAULT 16")

    def __init__(self, **traits):
        super(Box, self).__init__(**traits)

        # Pick a random background color
        self.bgcolor = choice(color_table.keys())

    def _draw_overlay(self, gc, view_bounds=None, mode="default"):
        """ Draw this object's id string, centered.
        """
        text = self.id
        with gc:
            gc.set_fill_color((0.0, 0.0, 0.0, 1.0))
            gc.set_font(self.font)
            twidth, theight = gc.get_text_extent(text)[2:]
            tx = self.x + (self.width - twidth) / 2.0
            ty = self.y + (self.height - theight) / 2.0
            gc.set_text_position(tx, ty)
            gc.show_text(text)

    __id_count = 0
    def _id_default(self):
        """ Provide a sensible default when an id isn't specified
        """
        self.__id_count += 1
        return 'Box {0}'.format(self.__id_count)
