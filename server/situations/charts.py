from openfisca_uk import graphs, IndividualSim
from server.utils.formatting import DARK_BLUE, format_fig
import json
import plotly.express as px
import pandas as pd
import numpy as np
from ubicenter.plotly import GRAY, BLUE

WHITE = "#FFF"


def budget_chart(baseline, reformed):
    df = pd.DataFrame(
        {
            "Employment income": baseline.calc("employment_income").sum(
                axis=0
            ),
            "Baseline": baseline.calc("net_income").sum(axis=0),
            "Reform": reformed.calc("net_income").sum(axis=0),
        }
    )
    graph = px.line(
        df,
        x="Employment income",
        y=["Baseline", "Reform"],
        labels={"variable": "Policy", "value": "Net income"},
        color_discrete_map={"Baseline": GRAY, "Reform": BLUE},
    )
    return json.loads(
        format_fig(graph, show=False)
        .update_layout(
            title="Net income by employment income",
            xaxis_title="Employment income",
            yaxis_title="Household net income",
            yaxis_tickprefix="£",
            xaxis_tickprefix="£",
            legend_title="Policy",
        )
        .to_json()
    )


def mtr_chart(baseline, reformed):
    earnings = baseline.calc("employment_income").sum(axis=0)
    baseline_net = baseline.calc("net_income").sum(axis=0)
    reform_net = reformed.calc("net_income").sum(axis=0)

    def get_mtr(x, y):
        return 1 - ((y[1:] - y[:-1]) / (x[1:] - x[:-1]))

    baseline_mtr = get_mtr(earnings, baseline_net)
    reform_mtr = get_mtr(earnings, reform_net)
    df = pd.DataFrame(
        {
            "Employment income": earnings[:-1],
            "Baseline": baseline_mtr,
            "Reform": reform_mtr,
        }
    )
    graph = px.line(
        df,
        x="Employment income",
        y=["Baseline", "Reform"],
        labels={"variable": "Policy", "value": "Effective MTR"},
        color_discrete_map={"Baseline": GRAY, "Reform": BLUE},
    )
    return json.loads(
        format_fig(graph, show=False)
        .update_layout(
            title="Effective marginal tax rate by employment income",
            xaxis_title="Employment income",
            xaxis_tickprefix="£",
            yaxis_tickformat="%",
            yaxis_title="Effective MTR",
            legend_title="Policy",
        )
        .to_json()
    )


COMPONENTS = (
    "employment_income",
    "self_employment_income",
    "pension_income",
    "savings_interest_income",
    "dividend_income",
    "income_tax",
    "national_insurance",
    "universal_credit",
    "child_benefit",
    "UBI",
    "net_income",
)

IS_POSITIVE = [True] * 5 + [False] * 2 + [True] * 4


def get_variables(sim, variables=COMPONENTS):
    amounts = []
    for variable in COMPONENTS:
        try:
            amounts += [sim.calc(variable).sum()]
        except:
            amounts += [0]
    df = pd.DataFrame(
        dict(
            variable=COMPONENTS,
            value=amounts,
            type=np.where(IS_POSITIVE, "Gain", "Loss"),
            is_value=True,
        )
    )
    df.value *= np.where(IS_POSITIVE, 1, -1)
    df = df[df.variable.isin(variables)].reset_index(drop=True)
    return df


key_to_label = dict(
    net_income="Net income",
    employment_income="Employment income",
    self_employment_income="Self-employment income",
    pension_income="Pension income",
    savings_interest_income="Savings income",
    dividend_income="Dividend income",
    universal_credit="Universal Credit",
    child_benefit="Child Benefit",
    UBI="UBI",
    income_tax="Income Tax",
    national_insurance="NI",
)


def variable_key_to_label(key):
    try:
        return key_to_label[key]
    except:
        return ""


def get_budget_waterfall_data(sim, label="Baseline", variables=COMPONENTS):
    df = get_variables(sim, variables=variables)
    net_income = df[df.variable == "net_income"].copy()
    net_income.type = ["Final"]
    df = df[df.variable != "net_income"].reset_index(drop=True)
    base = pd.Series([0] + list(df.value.cumsum()))
    for i in range(1, len(base)):
        if base[i] < base[i - 1]:
            base[i - 1] = base[i]
    df.value = df.value.abs()
    df = pd.concat(
        [
            pd.DataFrame(
                dict(variable=df.variable, value=base, type="", is_value=False)
            ),
            df,
        ]
    )
    df = pd.concat([df, net_income])
    df = df[~df.variable.isna()]
    df.variable = df.variable.apply(variable_key_to_label)
    df["Policy"] = label
    return df


def budget_waterfall_chart(baseline, reformed):
    baseline_variable_df = get_variables(baseline)
    baseline_variables = baseline_variable_df.variable[
        baseline_variable_df.value != 0
    ].unique()
    reform_variable_df = get_variables(reformed)
    reform_variables = reform_variable_df.variable[
        reform_variable_df.value != 0
    ].unique()
    variables = list(set(list(baseline_variables) + list(reform_variables)))
    df = pd.concat(
        [
            get_budget_waterfall_data(
                baseline, "Baseline", variables=variables
            ),
            get_budget_waterfall_data(reformed, "Reform", variables=variables),
        ]
    )
    fig = px.bar(
        df.rename(
            columns={
                "type": "Type",
                "value": "Amount",
                "variable": "Component",
            }
        ),
        x="Component",
        y="Amount",
        color="Type",
        animation_frame="Policy",
        color_discrete_map={
            "Gain": BLUE,
            "Loss": GRAY,
            "": WHITE,
            "Final": DARK_BLUE,
        },
    )
    variable_sums = df.groupby(["variable", "Policy"]).value.sum()
    fig.update_layout(
        title="Budget breakdown",
        xaxis_title="",
        yaxis_title="Yearly amount",
        yaxis_tickprefix="£",
        legend_title="",
        yaxis_range=(min(variable_sums.min(), 0), variable_sums.max()),
    )
    fig = format_fig(fig, show=False)
    fig.add_shape(
        type="line",
        xref="paper",
        yref="y",
        x0=0,
        y0=0,
        x1=1,
        y1=0,
        line=dict(color="grey", width=1, dash="dash"),
    )
    return json.loads(fig.to_json())
