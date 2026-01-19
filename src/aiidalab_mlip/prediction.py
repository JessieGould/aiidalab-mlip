"""MLIP prediction wizard step."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets


class PredictionWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard step for running predictions with trained MLIP."""

    def __init__(self, model, **kwargs):
        """
        Initialize prediction wizard step.

        Parameters
        ----------
        model : PredictionModel
            The prediction data model
        """
        self.model = model

        self.title = ipw.HTML("<h3>Step 3: Run Predictions</h3>")
        
        self.calc_type = ipw.Dropdown(
            options=[
                ('Geometry Optimization', 'geometry_opt'),
                ('Molecular Dynamics', 'md'),
                ('Single Point', 'single_point'),
            ],
            value='geometry_opt',
            description='Calculation:',
        )
        
        self.info = ipw.HTML(
            """
            <p>Run calculations using the trained MLIP model.</p>
            <p>Available calculation types:</p>
            <ul>
                <li><b>Geometry Optimization</b>: Find minimum energy structure</li>
                <li><b>Molecular Dynamics</b>: NVE, NVT, or NPT simulations</li>
                <li><b>Single Point</b>: Energy and forces calculation</li>
            </ul>
            """
        )
        
        self.run_button = ipw.Button(
            description='Run Calculation',
            button_style='success',
            disabled=True
        )
        
        self.output = ipw.Output()

        super().__init__(
            children=[
                self.title,
                self.info,
                self.calc_type,
                self.run_button,
                self.output
            ],
            **kwargs
        )
