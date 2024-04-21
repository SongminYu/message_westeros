import os

from message.config import Config
from message.reporter import Reporter
from message.scenario import Scenario


"""
run reporter
"""


def run_reporter(config: "Config"):
    reporter = Reporter(config)
    reporter.main()


"""
baseline model
"""


def run_model_baseline():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="baseline_2",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario.solve()
    run_reporter(config=config)


def setup_baseline(scenario: "Scenario"):
    scenario.add_set(set_name="node", file_name="Set_Node")
    scenario.add_set(set_name="commodity", file_name="Set_Commodity")
    scenario.add_set(set_name="level", file_name="Set_Level")
    scenario.add_set(set_name="technology", file_name="Set_TechnologyParent")
    scenario.add_set(set_name="mode", file_name="Set_Mode")
    scenario.add_ts_par(par_name="input", file_name="Parameter_TechnologyParent_Input")
    scenario.add_ts_par(par_name="output", file_name="Parameter_TechnologyParent_Output")
    scenario.add_ts_par(par_name="capacity_factor", file_name="Parameter_TechnologyParent_CapacityFactor")
    scenario.add_ts_par(par_name="fix_cost", file_name="Parameter_TechnologyParent_Cost_Fix")
    scenario.add_ts_par(par_name="var_cost", file_name="Parameter_TechnologyParent_Cost_Variable")
    scenario.add_ts_par(par_name="demand", file_name="Parameter_Demand", year_col="year", horizon="future")
    scenario.add_ts_par(par_name="interestrate", file_name="Parameter_InterestRate", year_col="year", horizon="future")
    scenario.add_ts_par(par_name="growth_activity_up", file_name="Parameter_TechnologyParent_GrowthActivityUp", year_col="year_act", horizon="future")
    scenario.add_ts_par(par_name="historical_activity", file_name="Parameter_TechnologyParent_HistoricalActivity", year_col="year_act", horizon="history")
    scenario.add_ts_par(par_name="historical_new_capacity", file_name="Parameter_TechnologyParent_HistoricalNewCapacity", year_col="year_vtg", horizon="history")
    scenario.add_ts_par(par_name="inv_cost", file_name="Parameter_TechnologyParent_Cost_Investment", year_col="year_vtg", horizon="future")
    scenario.add_ts_par(par_name="technical_lifetime", file_name="Parameter_TechnologyParent_TechnicalLifetime", year_col="year_vtg", horizon="future")
    return scenario


"""
emission_bound_cumulative model
"""


def run_model_emission_bound_cumulative():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="emission_bound_cumulative",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_bound_cumulative(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_emission(scenario: "Scenario"):
    scenario.add_set(set_name="emission", file_name="Set_Emission")
    scenario.add_category(set_name="emission", file_name="Category_Emission")
    scenario.add_ts_par(par_name="emission_factor", file_name="Parameter_TechnologyParent_EmissionFactor")
    return scenario


def add_emission_bound_cumulative(scenario: "Scenario"):
    scenario.add_category(set_name="year", file_name="Category_Year_EmissionBoundCumulative")
    scenario.add_par(par_name="bound_emission", file_name="Parameter_BoundEmission_Cumulative")
    return scenario


"""
emission_bound_year model
"""


def run_model_emission_bound_year():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="emission_bound_year",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_bound_year(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_emission_bound_year(scenario: "Scenario"):
    scenario.add_category(set_name="year", file_name="Category_Year_EmissionBoundYear")
    scenario.add_set(set_name="type_year", file_name="Set_TypeYear")
    scenario.add_ts_par(par_name="bound_emission", file_name="Parameter_BoundEmission_Year", year_col="type_year", horizon="future")
    return scenario


"""
emission_bound_cumulative_tax model
"""


def run_model_emission_bound_cumulative_tax():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="emission_bound_cumulative_tax",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_cumulative_bound_tax(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_emission_cumulative_bound_tax(scenario: "Scenario"):
    scenario.add_set(set_name="type_year", file_name="Set_TypeYear")
    scenario.add_category(set_name="year", file_name="Category_Year_EmissionBoundCumulative")
    scenario.add_par(par_name="bound_emission", file_name="Parameter_BoundEmission_Cumulative")
    scenario.add_ts_par(par_name="tax_emission", file_name="Parameter_BoundEmission_Tax", year_col="type_year", horizon="future")
    return scenario


"""
fossil resource model
"""


def run_model_fossil_resource():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="fossil_resource",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_fossil_resource(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_fossil_resource(scenario: "Scenario"):
    scenario.add_set(set_name="level_resource", file_name="Set_LevelResource")
    scenario.add_set(set_name="grade", file_name="Set_Grade")
    scenario.add_par(par_name="resource_volume", file_name="Parameter_Resource_Volume")
    scenario.add_ts_par(par_name="resource_cost", file_name="Parameter_Resource_Cost", year_col="year", horizon="future")
    scenario.add_ts_par(par_name="historical_extraction", file_name="Parameter_Resource_HistoricalExtraction", year_col="year", horizon="history")
    scenario.add_ts_par(par_name="input", file_name="Parameter_Resource_TechnologyParent_Input")
    return scenario


if __name__ == "__main__":

    # run_model_baseline()
    # run_model_emission_bound_cumulative()
    # run_model_emission_bound_year()
    # run_model_emission_bound_cumulative_tax()
    run_model_fossil_resource()
