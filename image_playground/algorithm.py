import os

import numpy as np

from traits.api import HasTraits, Any, File, Float, Int, Range, Str


class Algorithm(HasTraits):
    """ Wraps a user generated script that does some processing on an image.
    
    """

    # Loadable code bits
    code_file = File(editable=False)
    code_obj = Any(editable=False)
    code_source = Str(editable=False)

    def compute(self, image):
        """ Run the algorithm on the provided image.
        
            Returns a dictionary of intermediate images.
        
        """
        if self.code_obj is None:
            return {}, []

        # Create a context and add all the inputs to it
        context = {'image' : image}
        for name in self.editable_traits():
            context[name] = getattr(self, name)
        # Run the dynamic algorithm
        exec(self.code_obj, context)

        # Find all the 2D numpy arrays
        images = {}
        for k,v in context.iteritems():
            if isinstance(v, np.ndarray) and len(v.shape) == 2:
                images[k] = v
        # Remove 'image' (the input)
        del images['image']

        return images

    # private bits

    def _compile_script(self):
        """ Compile the script
        """
        try:
            return compile(self.code_source, '<user code>', 'exec')
        except:
            pass

    def _read_script(self):
        if os.path.exists(self.code_file):
            with open(self.code_file) as fp:
                return fp.read()
        return ""

    # trait handlers

    def _code_file_default(self):
        scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
        return os.path.join(scripts_dir, "default.py")

    def _code_obj_default(self):
        return self._compile_script()

    def _code_source_default(self):
        return self._read_script()

    def _code_file_changed(self):
        source = self._read_script()
        if len(source) > 0:
            self.code_source = source

    def _code_source_changed(self):
        code = self._compile_script()
        if code:
            self.code_obj = code

