
from enable.api import ConstraintsContainer
from enable.layout.api import (align, grid, horizontal, hbox, vbox, spacer,
    vertical)
from traits.api import List, Str

from box import Box


LAYOUT_HELPERS_NS = {
    'align': align,
    'grid': grid,
    'hbox': hbox,
    'vbox': vbox,
    'spacer': spacer,
    'horizontal': horizontal,
    'vertical': vertical,
}


class LayoutCanvas(ConstraintsContainer):
    """ A ConstraintsContainer with a dynamic constraints definition.
    """

    # A list of child boxes
    box_list = List

    # Just the names of the boxes
    box_names = List

    # Source code for the contraints of this container. Will be eval'd.
    constraints_def = Str

    def add_box(self, name, size_hint, **hugs_and_resists):
        """ Add a box component to the mix.
        """
        if len(name) == 0:
            return

        box = Box(id=name, layout_size_hint=size_hint, **hugs_and_resists)
        if name not in self.box_names:
            self.box_names.append(name)
            self.box_list.append(box)
            self.add(box)
            self._constraints_def_changed()

    def _constraints_def_changed(self):
        locals = {'container': self}
        for child in self._components:
            locals[child.id] = child

        try:
            new_cns = eval(self.constraints_def, LAYOUT_HELPERS_NS, locals)
        except Exception, ex:
            return

        self.layout_constraints = new_cns
        self.request_redraw()

    def _constraints_def_default(self):
        return """[
    vbox(*container.box_list),
    align('layout_height', *container.box_list),
    align('layout_width', *container.box_list),
]"""
