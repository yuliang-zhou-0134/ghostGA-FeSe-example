import warnings
warnings.filterwarnings("ignore") #ignore some matplotlib warnings

# numpy
import numpy as np

# import plovasp converter
import triqs_dft_tools.converters.plovasp.converter as plo_converter

# Generate and store PLOs
plo_converter.generate_and_output_as_text('plo.cfg', vasp_dir='./')

# import VASPconverter
from triqs_ghostGA.vasp import *


# create Converter
Converter = VaspConverter('FeSe', proj_or_hk='proj')
# run the converter
Converter.convert_dft_input()

# SumK
from triqs_dft_tools.sumk_dft_tools import SumkDFTTools

SK = SumkDFTTools(hdf_file='FeSe.h5', use_dft_blocks = False)
