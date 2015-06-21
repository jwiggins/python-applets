import numpy as np

from enable.api import Component
from enable.kiva_graphics_context import GraphicsContext
from traits.api import (Bool, DelegatesTo, Float, HasStrictTraits, Instance,
                        Trait, on_trait_change)

COLORS = ((1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0))


def _draw_circles(gc, colors, x, y, r, t, n, dont_fill):
    segment_width = r/float(n)
    for i in range(n, 0, -1):
        gc.arc(x, y, i*segment_width, 0.0, 2*np.pi)
        gc.set_fill_color(colors[i % 2])
        if dont_fill:
            gc.stroke_path()
        else:
            gc.fill_path()


def _draw_squares(gc, colors, x, y, r, t, n, dont_fill):
    segment_width = r/float(n)
    with gc:
        gc.translate_ctm(x, y)
        gc.rotate_ctm(t)
        for i in range(n, 0, -1):
            half_width = i*segment_width
            gc.rect(-half_width, -half_width, half_width*2.0, half_width*2.0)
            gc.set_fill_color(colors[i % 2])
            if dont_fill:
                gc.stroke_path()
            else:
                gc.fill_path()


def _draw_triangles(gc, colors, x, y, r, t, n, dont_fill):
    segment_width = r/float(n)
    with gc:
        gc.translate_ctm(x, y)
        gc.rotate_ctm(t)
        for i in range(n, 0, -1):
            scale = 2.0*i*segment_width
            with gc:
                gc.scale_ctm(scale, scale)
                gc.move_to(0.0, 0.7113248654051871 * 0.85)
                gc.line_to(-0.5, -0.28867513459481287)
                gc.line_to(0.5, -0.28867513459481287)
                gc.line_to(0.0, 0.7113248654051871 * 0.85)
                gc.close_path()
                gc.set_fill_color(colors[i % 2])
                if dont_fill:
                    gc.stroke_path()
                else:
                    gc.fill_path()

shape_dict = dict(Circle=_draw_circles,
                  Square=_draw_squares,
                  Triangle=_draw_triangles)


class SpiralComponent(Component):
    """ A Component that draws a spiral based on several parameters.

    """
    num_shapes = Float(150.0)
    num_cycles = Float(8.0)
    max_radius = Float(7.1)
    min_count = Float(2.0)
    max_count = Float(10.0)
    start_scale = Float(2.25)
    end_scale = Float(1.5)
    inverted = Bool(False)
    no_fill = Bool(False)

    shape_choices = shape_dict.keys()
    shape = Trait(shape_dict.keys()[0], shape_dict)

    def draw(self, gc, **kwargs):
        colors = COLORS if not self.inverted else tuple(reversed(COLORS))
        gc.clear(colors[0])

        center = (gc.width()/2, gc.height()/2)
        NUM = int(self.num_shapes)
        thetas = np.linspace(0., self.num_cycles*2.*np.pi, NUM)
        radii = np.linspace(0.0, self.max_radius, NUM)
        scales = np.linspace(self.start_scale, self.end_scale, NUM)
        counts = np.linspace(self.min_count, self.max_count, NUM)

        for r, t, s, n in zip(radii, thetas, scales, counts):
            r = np.exp(r)*s
            x = center[0]+r*np.cos(t)*s
            y = center[1]+r*np.sin(t)*s

            self.shape_(gc, colors, x, y, r, t, int(n)*2, self.no_fill)


class SpiralModel(HasStrictTraits):
    component = Instance(Component)

    #: Delegates.
    padding = DelegatesTo('component')
    num_shapes = DelegatesTo('component')
    num_cycles = DelegatesTo('component')
    max_radius = DelegatesTo('component')
    min_count = DelegatesTo('component')
    max_count = DelegatesTo('component')
    start_scale = DelegatesTo('component')
    end_scale = DelegatesTo('component')
    inverted = DelegatesTo('component')
    no_fill = DelegatesTo('component')
    shape = DelegatesTo('component')

    def _component_default(self):
        return SpiralComponent()

    @on_trait_change('num_shapes,num_cycles,max_radius,min_count,max_count'
                     ',start_scale,end_scale,inverted,no_fill,shape')
    def _redraw(self):
        self.component.request_redraw()

    def save(self, path):
        """ Save the contents of the component to a file.
        """
        # 100 DPI dimensions of the Macbook Pro 15"
        size = (1435, 982)
        gc = GraphicsContext(size)
        self.component.draw(gc)
        gc.save(path)
