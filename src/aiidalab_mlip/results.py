"""Results viewing wizard step."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets


class ResultsWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard step for viewing results."""

    def __init__(self, model, **kwargs):
        """
        Initialize results wizard step.

        Parameters
        ----------
        model : ResultsModel
            The results data model
        """
        self.model = model

        self.title = ipw.HTML("<h3>Step 4: View Results</h3>")
        
        self.info = ipw.HTML(
            """
            <p>View and analyze calculation results.</p>
            <p>This section will display:</p>
            <ul>
                <li>Optimized structures</li>
                <li>Energy plots and trajectories</li>
                <li>MD simulation results</li>
                <li>Export options</li>
            </ul>
            """
        )
        
        self.results_area = ipw.Output()

        super().__init__(
            children=[
                self.title,
                self.info,
                self.results_area
            ],
            **kwargs
        )
