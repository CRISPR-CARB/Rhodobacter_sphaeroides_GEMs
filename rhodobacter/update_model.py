#locally run this script after updating biolog/media updates
#and before running MEMOTE so it can update the model 
# with most current biolog information
#output file will overwite old generated model reports

#from memote.suite.cli.reports import diff
import cobra
import logging
from cobra.manipulation.modify import rename_genes
from cobra.io import read_sbml_model
import pandas as pd
import pathlib
import sys
import os
import re
sys.path.insert(0, "C:/Users/lint730/concerto") #this will have to be a local path
from concerto.utils import load_universal_model
from concerto.utils.biolog_help import add_biolog_exchanges

_log = logging.getLogger()

#adding additional metabolites
_path = pathlib.Path(__file__).parent
_f_path = _path.joinpath('C:/Users/lint730/GEM_repos/Rhodobacter_sphaeroides_GEMs/rhodobacter/data/growth/custom_plate.csv').__str__()

starting_model = read_sbml_model("GEMs/model_compartment_cleaned.xml")
output_model_name = 'model_gapfilled.xml'
output_model_path = os.path.join(_path, output_model_name)

def write_model(model):
    cobra.io.write_sbml_model(model, output_model_path)

#function to change the metabolite compartments in model from _c0 or _e0 to _c or _e
def change_metabolite_compartment(model, target_compartments, compartment_id_change_dict):
    model.compartments = target_compartments
    _log.info("Removing 0 from metabolites and exchange reactions")
    # Update metabolites
    for metabolite in model.metabolites:
        if metabolite.compartment in compartment_id_change_dict.keys():
            metabolite.compartment = compartment_id_change_dict[metabolite.compartment]
            metabolite_base = re.search(r'^(.*)_\w{2}$', metabolite.name).group(1)
            metabolite.name = metabolite_base + '_' + metabolite.compartment
            metabolite_base = re.search(r'^(.*)_\w{2}$', metabolite.id).group(1)
            metabolite.id = metabolite_base + '_' + metabolite.compartment

    # Update reactions
    for reaction in model.reactions:
        if reaction.id.endswith('c0') or reaction.id.endswith('e0') or reaction.id.endswith('p0'):
            reaction.id = reaction.id[:-1]

    return model

#define target_compartments and compartment_id_change_dict for change_metabolite_compartment function
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

#function to add biolog exchanges from concerto utils file
def update_1(model):
    # add missing biolog reactions to model
    _log.info("Adding BL to prefix")
    model = add_biolog_exchanges(model)
    return model

#function to add custom plate exchanges from concerto utils file
def add_custom_plate_exchanges(model):
    """ Add missing custom_plate exchanges to cobra model

    Adds missing custom_plate exchanges from the plate to a cobra model. It grabs the
    reactions for the universal model, which should pull all annotations as
    well as metabolite information.


    Parameters
    ----------
    model : cobra.Model

    Returns
    -------
    cobra.Model
    """
    new_model = model
    not_found = set()
    added = set()

    # load in material needed to add biolog exchanges
    universal_model = load_universal_model()
    custom_map = pd.read_csv(_f_path, index_col=False)
  
    for rxn in custom_map.exchange:
        if rxn not in new_model.reactions:
            if rxn in universal_model.reactions:
                added.add(rxn)
                current_rxn = universal_model.reactions.get_by_id(rxn)
                metabolite = current_rxn.reactants[0]
                new_model.add_boundary(
                    metabolite,
                    type="exchange"
                )
            else:
                not_found.add(rxn)
    for i in not_found:
        _log.warning(f'{i} not found in universal model')
        print(f'{i} not found in universal model')
    _log.info(f"Added {len(added)} custom exchange reactions")
    print(f"Added {len(added)} custom exchange reactions")
  
    return new_model

#function to execute all change to update the model
def update_model():
    # Fix compartments
    model = change_metabolite_compartment(starting_model, target_compartments, compartment_id_change_dict)  
    model = update_1(model)
    model = add_custom_plate_exchanges(model)
    write_model(model)


if __name__ == '__main__':
    update_model()
    '''model_paths = [s_model_path, output_model_path]
    diff(
        [
            *model_paths,
            '--filename', os.path.join(_file_path, 'model_differences.html'),
            '--experimental', os.path.join(_file_path, 'data', 'experiments.yml'),
            # '--custom-tests', os.path.join(_file_path, 'custom_tests'),
            '--exclusive', 'test_growth',
        ]
    )'''
