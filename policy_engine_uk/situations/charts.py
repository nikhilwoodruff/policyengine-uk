from openfisca_uk import IndividualSim
from policy_engine_uk.utils import charts
import plotly.express as px
import pandas as pd

COLOR_MAP = {
    "Baseline": charts.GRAY,
    "Reform": charts.BLUE,
}

LABELS = dict(
    variable="Policy",
    employment_income="Employment income",
)


def budget_chart(baseline: IndividualSim, reformed: IndividualSim) -> str:
    """Produces line chart with employment income on the x axis and net income
    on the y axis, for baseline and reform simulations.
    :param baseline: Baseline simulation.
    :type baseline: IndividualSim
    :param reformed: Reform simulation.
    :type reformed: IndividualSim
    :return: Representation of the budget plotly chart as a JSON string.
    :rtype: str
    """
    df = pd.DataFrame(
        {
            "employment_income": baseline.calc("employment_income").sum(
                axis=0
            ),
            "Baseline": baseline.calc("net_income").sum(axis=0),
            "Reform": reformed.calc("net_income").sum(axis=0),
        }
    )
    fig = px.line(
        df.round(0),
        x="employment_income",
        y=["Baseline", "Reform"],
        labels=dict(LABELS, value="Net income"),
        color_discrete_map=COLOR_MAP,
    )
    fig.update_traces(hovertemplate="%{y}")
    fig.update_layout(
        title="Net income by employment income",
        xaxis_title="Employment income",
        yaxis_title="Household net income",
        yaxis_tickprefix="£",
        xaxis_tickprefix="£",
        legend_title=None,
        hovermode="x unified",
    )
    return charts.formatted_fig_json(fig)


def mtr_chart(baseline: IndividualSim, reformed: IndividualSim) -> str:
    """Produces line chart with employment income on the x axis and marginal
    tax rate on the y axis, for baseline and reform simulations.
    :param baseline: Baseline simulation.
    :type baseline: IndividualSim
    :param reformed: Reform simulation.
    :type reformed: IndividualSim
    :return: Representation of the marginal tax rate plotly chart as a JSON
        string.
    :rtype: str
    """
    earnings = baseline.calc("employment_income").sum(axis=0)
    baseline_net = baseline.calc("net_income").sum(axis=0)
    reform_net = reformed.calc("net_income").sum(axis=0)

    def get_mtr(x, y):
        return 1 - ((y[1:] - y[:-1]) / (x[1:] - x[:-1]))

    baseline_mtr = get_mtr(earnings, baseline_net)
    reform_mtr = get_mtr(earnings, reform_net)
    df = pd.DataFrame(
        {
            "employment_income": earnings[:-1].round(0),
            "Baseline": baseline_mtr,
            "Reform": reform_mtr,
        }
    )
    fig = px.line(
        df,
        x="employment_income",
        y=["Baseline", "Reform"],
        labels=dict(LABELS, value="Effective MTR"),
        color_discrete_map=COLOR_MAP,
        line_shape="hv",
    )
    fig.update_traces(hovertemplate="%{y}")
    fig.update_layout(
        title="Effective marginal tax rate by employment income",
        xaxis_title="Employment income",
        xaxis_tickprefix="£",
        yaxis_tickformat="%",
        yaxis_title="Effective MTR",
        legend_title=None,
        hovermode="x unified",
    )
    return charts.formatted_fig_json(fig)


def household_waterfall_chart(
    baseline: IndividualSim, reformed: IndividualSim
) -> dict:
    return charts.waterfall_chart(baseline, reformed)
