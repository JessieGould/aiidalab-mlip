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
        self.model_selector.observe(self._on_model_change, names='value')
        
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
        self.train_button.on_click(self._on_train_click)
        
        self.status = ipw.HTML()
        self.output = ipw.Output()

        super().__init__(
            children=[
                self.title,
                self.info,
                self.model_selector,
                self.train_button,
                self.status,
                self.output
            ],
            **kwargs
        )
    
    def _on_model_change(self, change):
        """Handle model type selection."""
        self.model.model_type = change['new']
        self.status.value = f"<p>Selected {change['new']} architecture</p>"
        self.train_button.disabled = False
    
    def _on_train_click(self, button):
        """Handle train button click."""
        with self.output:
            self.output.clear_output()
            print(f"Training {self.model.model_type} model...")
            print()
            print("To implement training, you need:")
            print("1. Install aiida-mlip in the container")
            print("2. Prepare training data (train/valid/test XYZ files)")
            print("3. Create JanusConfigfile with training parameters")
            print("4. Submit aiida_mlip.calculations.train.Train CalcJob")
            print()
            print("Example code:")
            print("```python")
            print("from aiida import orm, engine")
            print("from aiida_mlip.calculations.train import Train")
            print("from aiida_mlip.data.config import JanusConfigfile")
            print("from aiida_mlip.data.model import ModelData")
            print()
            print("# Create config with training parameters")
            print("config = JanusConfigfile({")
            print("    'name': 'my_model',")
            print("    'train_file': '/path/to/train.xyz',")
            print("    'valid_file': '/path/to/valid.xyz',")
            print("    'test_file': '/path/to/test.xyz',")
            print("    'arch': 'mace',  # or 'm3gnet', 'chgnet'")
            print("})")
            print()
            print("# Submit training")
            print("builder = Train.get_builder()")
            print("builder.mlip_config = config")
            print("builder.fine_tune = orm.Bool(False)")
            print("builder.metadata.options.resources = {'num_machines': 1}")
            print("node = engine.submit(builder)")
            print("```")
            
            self.status.value = "<p style='color: orange;'>⚠ Training requires aiida-mlip installation and training data</p>"
