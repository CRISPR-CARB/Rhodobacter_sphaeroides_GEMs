import re

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
