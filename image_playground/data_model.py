
import os
import numpy as np

from PIL import Image
from traits.api import HasTraits, Array, List, Directory, File, Instance, \
    Property, Range, Str, cached_property

from algorithm import Algorithm


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
    """
    """
    img = Image.open(filename)
    img.draft("L", (256, 256))
    return np.array(img)


class ImageCollection(HasTraits):
    """ This represents a collection of images stored in a directory.
    
    """

    # core input traits

    #directory = Directory()
    filename = File()

    algorithm = Instance(Algorithm, ())

    # A list of traits to be added to algorithm instances
    algorithm_inputs = List([])

    # derived traits

    files = Property(List(File), depends_on='filename')

    image_data = List(Array)

    display_images = List(Array)

    image_names = List()

    selected_image = Str

    # traits handlers

    def _image_data_default(self):
        return [np.zeros((255,255))]

    def _display_images_default(self):
        return self.image_data

    @cached_property
    def _get_files(self):
        full_paths = [os.path.abspath(self.filename),]
        return [filename for filename in full_paths if _is_data_file(filename)]

    def _filename_changed(self):
        self.load_data()
        self.run_algorithm()

    def _image_names_changed(self):
        if len(self.image_names) > 0:
            self.selected_image = self.image_names[0]

    def _selected_image_changed(self):
        self.run_algorithm()

    # utility methods

    def add_algorithm_input(self, name, low, high):
        """ Adds a new input trait for the algorithm
        """
        if len(name) == 0 or low >= high:
            return

        self.algorithm_inputs.append((name, Range(low, high)))
        value = (low+high)/2

        # Create the new instance and add the input traits to it
        algorithm = Algorithm()
        for input in self.algorithm_inputs:
            algorithm.add_trait(*input)
        # Set a default value for the new trait
        setattr(algorithm, name, value)

        # Copy values from the old instance
        old = self.algorithm
        traits = set(old.trait_names()) - {'trait_added', 'trait_modified'}
        for trait in traits:
            setattr(algorithm, trait, getattr(old, trait))

        self.algorithm = algorithm

    def load_data(self):
        images = [_load_image(filename) for filename in self.files]
        self.image_data = images
        self.display_images = images

    def run_algorithm(self):
        """ Run the algorithm on each of the files and create a list of events
        
        """
        if self.algorithm is None:
            return

        image_data = []
        for img in self.image_data:
            intermediates = self.algorithm.compute(img)

            self.image_names = intermediates.keys()
            if self.selected_image in intermediates:
                image_data.append(intermediates[self.selected_image])

        if len(image_data) == len(self.image_data):
            self.display_images = image_data

