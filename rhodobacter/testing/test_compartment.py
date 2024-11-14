import pytest
from cobra import Model, Metabolite
import os
import sys

# Add the path to the folder containing change_metabolite_compartment.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the change_metabolite_compartment function
from change_metabolite_compartment import change_metabolite_compartment

def test_change_metabolite_compartment():
    # Create a model with tricky metabolite IDs
    model = Model('test_model')
    tricky_metabolites = [
        Metabolite('met1_c0', compartment='c0', name='Metabolite1_c0'),
        Metabolite('met2_e0', compartment='e0', name='Metabolite2_e0'),
        Metabolite('M_3__45__Hydroxy__45__5__45__methylhex__45__4__45__enoyl__45__CoA_c0', compartment='c0', name='M_3__45__Hydroxy__45__5__45__methylhex__45__4__45__enoyl__45__CoA_c0'),
        Metabolite('M_5__45__Methyl__45__3__45__oxo__45__4__45__hexenoyl__45__CoA_p0', compartment='p0', name='M_5__45__Methyl__45__3__45__oxo__45__4__45__hexenoyl__45__CoA_p0')
    ]
    model.add_metabolites(tricky_metabolites)

    target_compartments = {
        'c': 'cytosol',
        'e': 'extracellular',
        'p': 'periplasm'
    }
    compartment_id_change_dict = {
        'c0': 'c',
        'e0': 'e',
        'p0': 'p'
    }

    # Call the function
    updated_model = change_metabolite_compartment(model, target_compartments, compartment_id_change_dict)

    # Check the updated compartments
    assert updated_model.compartments == target_compartments

    # Check the updated metabolites
    expected_metabolites = {
        'met1_c': 'Metabolite1_c',
        'met2_e': 'Metabolite2_e',
        'M_3__45__Hydroxy__45__5__45__methylhex__45__4__45__enoyl__45__CoA_c': 'M_3__45__Hydroxy__45__5__45__methylhex__45__4__45__enoyl__45__CoA_c',
        'M_5__45__Methyl__45__3__45__oxo__45__4__45__hexenoyl__45__CoA_p': 'M_5__45__Methyl__45__3__45__oxo__45__4__45__hexenoyl__45__CoA_p'
    }

    for met in updated_model.metabolites:
        assert met.id in expected_metabolites
        assert met.name == expected_metabolites[met.id]
        if met.id.endswith('_c'):
            assert met.compartment == 'c'
        elif met.id.endswith('_e'):
            assert met.compartment == 'e'
        elif met.id.endswith('_p'):
            assert met.compartment == 'p'

if __name__ == '__main__':
    pytest.main()