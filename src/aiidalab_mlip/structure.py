"""Structure selection wizard step."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets


class StructureWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard step for structure selection."""

    def __init__(self, model, **kwargs):
        """
        Initialize structure wizard step.

        Parameters
        ----------
        model : StructureModel
            The structure data model
        """
        self.model = model

        # Simple placeholder for now
        self.title = ipw.HTML("<h3>Step 1: Select or Upload Structure</h3>")
        
        self.upload_widget = ipw.FileUpload(
            accept='.cif,.xyz,.pdb',
            multiple=False,
            description='Upload Structure'
        )
        
        self.info = ipw.HTML(
            """
            <p>Upload a structure file (CIF, XYZ, or PDB format) or 
            select from the AiiDA database.</p>
            <p><i>Note: Full structure manager will be added once 
            dependency issues are resolved.</i></p>
            """
        )

        super().__init__(
            children=[self.title, self.info, self.upload_widget],
            **kwargs
        )
