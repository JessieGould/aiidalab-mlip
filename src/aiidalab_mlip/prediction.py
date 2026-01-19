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
        self.calc_type.observe(self._on_calc_change, names='value')
        
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
        self.run_button.on_click(self._on_run_click)
        
        self.status = ipw.HTML()
        self.output = ipw.Output()

        super().__init__(
            children=[
                self.title,
                self.info,
                self.calc_type,
                self.run_button,
                self.status,
                self.output
            ],
            **kwargs
        )
    
    def _on_calc_change(self, change):
        """Handle calculation type selection."""
        self.model.calculation_type = change['new']
        calc_names = {
            'geometry_opt': 'Geometry Optimization',
            'md': 'Molecular Dynamics', 
            'single_point': 'Single Point'
        }
        self.status.value = f"<p>Selected: {calc_names[change['new']]}</p>"
        self.run_button.disabled = False
    
    def _on_run_click(self, button):
        """Handle run button click."""
        with self.output:
            self.output.clear_output()
            calc_type = self.model.calculation_type
            print(f"Submitting {calc_type}...")
            print("TODO: Submit aiida-mlip calculation")
            # TODO: Import and submit appropriate calculation:
            # - aiida_mlip.calculations.geomopt.Geomopt
            # - aiida_mlip.calculations.md.MD  
            # - aiida_mlip.calculations.singlepoint.Singlepoint
            self.status.value = "<p style='color: orange;'>Calculation submission not yet implemented</p>"
