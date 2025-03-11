import cobra
import pandas as pd


def test_gapfill_function():
        """Test the gapfill process and assert for three things: 
        1. assert original model grows
        2. assert that gapped doesn't grow (assert < threshold)
        3. assert that gapfilled does grow:
        growth = model.optimize().objective_value threshold = 0.2"
        "assert growth > threshold, f"Growth {growth} was not greater than threshold {threshold}"""

        #assert growth of original model by using threshold of greater than 0.02
        working_model = cobra.io.read_sbml_model('../../GEMs/f6p_reactions.xml')
        assert working_model.optimize().objective_value < 0.02, "Original model cannot grow"    

        #assert that gapped model does not grow by using threshold of less than 0.02
        gapped_model = cobra.io.read_sbml_model('../../GEMs/model_with_f6p_gap.xml')
        solutions = cobra.flux_analysis.gapfill(working_model, gapped_model, demand_reactions=False)
        gapped_model.add_reactions(solutions[0])
        assert gapped_model.optimize().objective_value < 0.02, "Gapped model does not grow"

        #assert that gapfilled model does grow by using threshold of greater than 0.02
        gapfilled_model = cobra.io.read_sbml_model('../../GEMs/f6p_gapfilled.xml')
        assert gapfilled_model.optimize().objective_value > 0.02, "Gapfilled model can grow"
