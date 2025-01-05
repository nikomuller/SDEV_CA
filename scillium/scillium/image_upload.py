from django.utils.deconstruct import deconstructible
from uuid import uuid4
import os


# 
# We want to split the uploaded file name
# into the name and the extension
# 
def split_into_segments(filename):
    # Split the filename into segments
    segments = filename.split('.')

    # Get the extension of the file
    extension = segments[-1]

    # Get the name of the file
    name = '.'.join(segments[:-1])

    return name, extension



# 
# This class generates a unique filename
# using the uuid4 function
# 
def generate_unique_filename(format):
    # Generate a unique filename
    filename = str(uuid4())

    # Return the filename
    return "{}.{}".format(filename, format)



# 
# This function combines the two functions above
# 
@deconstructible
class rename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # Split the filename into segments
        name, extension = split_into_segments(filename)

        # Generate a unique filename
        filename = generate_unique_filename(extension)

        # Return the path
        return os.path.join(self.path, filename)
