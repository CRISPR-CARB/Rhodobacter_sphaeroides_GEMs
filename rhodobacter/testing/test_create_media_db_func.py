import cobra
import os
import sys
import pandas as pd
from pandas.testing import assert_frame_equal

# Add the path to the folder containing change_metabolite_compartment.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the change_metabolite_compartment function
from rhodobacter.testing.func_for_test import create_media_db
from rhodobacter.testing.func_for_test import get_metabolite_from_exchange_rxn

def test_create_media_db():
        """Test the create_media_db function which creates a media database for the model to call
        during gapfill"""

        #define model, medium, and medium description
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../GEMS/model_compartment_cleaned.xml'))
        model = cobra.io.read_sbml_model(model_path)
        medium_name = "Base"
        medium_description = "Rhodobacter sphaeroides base medium"
        media_db = pd.DataFrame(columns=['medium', 'description', 'compound', 'name'])
    #id.rsplit('_', 1)[0] was included to remove compartment suffix.
        media_db['compound'] = pd.Series([get_metabolite_from_exchange_rxn(model, rxn).id.rsplit('_', 1)[0] for rxn in model.medium])
        media_db['name'] = pd.Series([get_metabolite_from_exchange_rxn(model, rxn).name for rxn in model.medium])
        media_db['medium'] = medium_name
        media_db['description'] = medium_description
        #input, actual, and expected dataframes. then compare and assert dataframes are same
        input_df = media_db
        expected_df = pd.read_csv("../data/media/default_media_db.tsv", sep="\t")
        actual_df = create_media_db(input_df, medium_name, medium_description)
        assert_frame_equal(actual_df, expected_df)
