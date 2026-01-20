"""Defines the main AiiDAlab MLIP application page."""

from datetime import datetime

import aiidalab_widgets_base as awb
import ipywidgets as ipw
from IPython.display import display

from aiidalab_mlip.structure import StructureWizardStep
from aiidalab_mlip.training import TrainingWizardStep
from aiidalab_mlip.prediction import PredictionWizardStep
from aiidalab_mlip.results import ResultsWizardStep
from aiidalab_mlip.process import MainAppModel


class MainApp:
    """The main AiiDAlab MLIP application class."""

    def __init__(self):
        """MainApp constructor."""
        self.model = MainAppModel()
        self.view = MainAppView(self.model)
        display(self.view)


class MainAppView(ipw.VBox):
    """The main app view."""

    def __init__(self, model: MainAppModel, **kwargs):
        """MainAppView constructor."""
        logo = ipw.HTML(
            """
            <div class="app-container logo" style="text-align: center;">
                <h1> Machine Learning Interatomic Potentials</h1>
            </div>
            """,
            layout={"margin": "auto"},
        )

        subtitle = ipw.HTML(
            """
            <h2 style="text-align: center;">
                Train and deploy ML potentials for molecular simulations
            </h2>
            """
        )

        header = ipw.VBox(
            children=[
                logo,
                subtitle,
            ],
            layout={"margin": "auto"},
        )

        footer = ipw.HTML(
            f"""
            <footer style="text-align: center; margin-top: 20px;">
                Copyright (c) {datetime.now().year} MLIP Development Team
            </footer>
            """,
        )

        self.main = WizardWidget(model)

        super().__init__(
            layout={}, children=[header, self.main, footer], **kwargs
        )


class WizardWidget(ipw.VBox):
    """Widget to hold the main MLIP application wizard."""

    def __init__(self, model: MainAppModel, **kwargs):
        """
        WizardWidget constructor.

        Parameters
        ----------
        model : MainAppModel
            The application data model
        **kwargs :
            Keyword arguments passed to ipywidgets.VBox.__init__()
        """
        self.structure_step = StructureWizardStep(model.structure_model)
        self.training_step = TrainingWizardStep(model.training_model)
        self.prediction_step = PredictionWizardStep(model.prediction_model)
        self.results_step = ResultsWizardStep(model.results_model)

        # Link structure to prediction step
        def update_prediction_structure(change):
            self.prediction_step._parent_structure = change['new']
        
        model.structure_model.observe(update_prediction_structure, names='structure')

        self._wizard_app_widget = awb.WizardAppWidget(
            steps=[
                ("Select Structure", self.structure_step),
                ("Train MLIP", self.training_step),
                ("Run Predictions", self.prediction_step),
                ("View Results", self.results_step),
            ]
        )

        super().__init__(
            children=[self._wizard_app_widget],
            **kwargs,
        )
