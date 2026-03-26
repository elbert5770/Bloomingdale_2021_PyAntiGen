"""
Example model builder. Outputs go to antimony_models/Example/ and generated/Example/.
"""
import os
import sys

# Use location: import Model_* from the same folder as this script (model folder)
_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)
MODEL_NAME = os.path.basename(_project_dir)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from framework.pyantigen import PyAntiGen
from modules.Tissue_Rxns.Tissue_rxns_bloomingdale_1a import Tissue_RxnsModule
from modules.Tissue_Flows.Tissue_flows_bloomingdale_1a import Tissue_FlowsModule
from modules.Tissue_Flows.FCRn_flows_bloomingdale_1a import FcRn_FlowsModule
from modules.Tissue_Flows.cns_flows_bloomingdale_1a import CNS_FlowsModule


if __name__ == "__main__":
    Isotopes = ['']
    SpeciesList = ['Antibody']
    model = PyAntiGen(name=MODEL_NAME, isotopes=Isotopes)
    for Species in SpeciesList:
        Tissue_RxnsModule(model, Species=Species)
        Tissue_FlowsModule(model, Species=Species)
        FcRn_FlowsModule(model, Species=Species)
        CNS_FlowsModule(model, Species=Species)

    print(f"Reactions generated: {model.counter}")
    print(f"Rules generated: {len(model.rules)}")
    model.generate(__file__)
    print("\nModel generated successfully.")
    print("Next steps:")
    print(f"  1. Optionally edit parameters in antimony_models/{MODEL_NAME}/{MODEL_NAME}_parameters.csv")
    print(f"  2. From scripts/{MODEL_NAME}/, run: python {MODEL_NAME}_run.py")
