# Test cases

"""Generate image encondings"""
from models import EncondingImages
number_of_images = 30
enconding_images = EncondingImages(number_of_images)
encoding_values = enconding_images.get()
