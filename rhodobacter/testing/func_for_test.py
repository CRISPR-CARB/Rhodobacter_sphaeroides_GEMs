import re
import pandas as pd

def change_metabolite_compartment(model, target_compartments, compartment_id_change_dict):
    model.compartments = target_compartments
    for metabolite in model.metabolites:
        # Change metabolite compartment
        if metabolite.compartment in compartment_id_change_dict.keys():
            metabolite.compartment = compartment_id_change_dict[metabolite.compartment]
            # Change metabolite name and id
            metabolite_base = re.search(r'^(.*)_\w{2}$', metabolite.name).group(1)
            metabolite.name = metabolite_base+'_'+metabolite.compartment
            metabolite_base = re.search(r'^(.*)_\w{2}$', metabolite.id).group(1)
            metabolite.id = metabolite_base+'_'+metabolite.compartment
    return model

def get_metabolite_from_exchange_rxn(model, exchange_rxn_id):
    met = list(model.reactions.get_by_id(exchange_rxn_id).metabolites)[0]
    return met

def create_media_db(model, medium_name, medium_description):
    """creates a media database for a model.
    The library must be a tab-separated file with four columns:
    medium: short id to be passed in command line (example: X)
    description: description of the medium (optional, example: Our magic X formula)
    compound: compound id (example: glc). Note: the id must be the BiGG id without the compartment suffix.
    id.rsplit('_', 1)[0] was included to remove compartment suffix.
    name: compound name (optional, example: Glucose)
Please note that, at this moment, CarveMe only supports metabolite ids from the BiGG database.
    Args: model (cobra.Model): a model
    medium_name (str): the name of the medium
    medium_description (str): the description of the medium
    Returns: a media database
    """
    media_db = pd.DataFrame(columns=['medium', 'description', 'compound', 'name'])
    #id.rsplit('_', 1)[0] was included to remove compartment suffix.
    media_db['compound'] = pd.Series([get_metabolite_from_exchange_rxn(model, rxn).id.rsplit('_', 1)[0] for rxn in model.medium])
    media_db['name'] = pd.Series([get_metabolite_from_exchange_rxn(model, rxn).name for rxn in model.medium])
    media_db['medium'] = medium_name
    media_db['description'] = medium_description
    

    return media_db