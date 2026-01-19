"""MLIP training wizard step."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets


class TrainingWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard step for MLIP training."""

    def __init__(self, model, **kwargs):
        """
        Initialize training wizard step.

        Parameters
        ----------
        model : TrainingModel
            The training data model
        """
        self.model = model

        self.title = ipw.HTML("<h3>Step 2: Train MLIP Model</h3>")
        
        self.model_selector = ipw.Dropdown(
            options=['MACE', 'M3GNET', 'CHGNET'],
            value='MACE',
            description='Model Type:',
        )
        
        self.info = ipw.HTML(
            """
            <p>Select the machine learning potential model to train.</p>
            <p>Supported models:</p>
            <ul>
                <li><b>MACE</b>: Multi-Atomic Cluster Expansion</li>
                <li><b>M3GNET</b>: Materials 3-body Graph Network</li>
                <li><b>CHGNET</b>: Crystal Hamiltonian Graph Neural Network</li>
            </ul>
            """
        )
        
        self.train_button = ipw.Button(
            description='Start Training',
            button_style='primary',
            disabled=True
        )
        
        self.output = ipw.Output()

        super().__init__(
            children=[
                self.title,
                self.info,
                self.model_selector,
                self.train_button,
                self.output
            ],
            **kwargs
        )
