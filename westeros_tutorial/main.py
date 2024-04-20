from message.scenario import Scenario
from message.reporter import Reporter
from message.config import Config


"""
baseline model
"""


def run_model_baseline(config: "Config"):
    config.scenario_name = "baseline"
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario.solve()


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


def run_model_emission_bound_cumulative(config: "Config"):
    config.scenario_name = "emission_bound_cumulative"
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_bound_cumulative(scenario)
    scenario.solve()


def add_emission(scenario: "Scenario"):
    scenario.add_set(set_name="emission", file_name="Set_Emission")
    scenario.add_category(set_name="emission", file_name="Category_Emission")
    scenario.add_ts_par(par_name="emission_factor", file_name="Parameter_TechnologyParent_EmissionFactor")
    return scenario


def add_emission_bound_cumulative(scenario: "Scenario"):
    scenario.add_category(set_name="year", file_name="Category_Year")
    scenario.add_par(par_name="bound_emission", file_name="Parameter_BoundEmission_Cumulative")
    return scenario


"""
run reporter
"""


def run_reporter(config: "Config", scenario_name: str):
    config.scenario_name = scenario_name
    reporter = Reporter(config)
    reporter.main()


if __name__ == "__main__":
    cfg = Config(
        model_name="westeros",
        scenario_name="",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    # run_model_baseline(config=cfg)
    run_model_emission_bound_cumulative(config=cfg)
    # run_reporter(config=cfg, scenario_name="emission_bound_cumulative")