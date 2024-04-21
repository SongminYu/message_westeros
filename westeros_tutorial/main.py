import os

from message.config import Config
from message.reporter import Reporter
from message.scenario import Scenario
import pandas as pd

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
        scenario_name="baseline",
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


"""
renewable model
"""


def run_model_renewable():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="renewable",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_cumulative_bound_tax(scenario)
    scenario = add_renewable(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_renewable(scenario: "Scenario"):
    scenario.add_set(set_name="grade", file_name="Set_Grade")
    scenario.add_set(set_name="level_renewable", file_name="Set_LevelRenewable")
    scenario.add_category(set_name="technology", file_name="Category_Renewable_Technology")
    scenario.add_ts_par(par_name="input", file_name="Parameter_Renewable_TechnologyParent_Input")
    scenario.add_ts_par(par_name="renewable_potential", file_name="Parameter_Renewable_Potential", year_col="year", horizon="horizon")  # horizon = either "future" or "horizon" works, in the tutorial, model_horizon = scen.set("year") means [690, 700, 710, 720]
    scenario.add_ts_par(par_name="renewable_capacity_factor", file_name="Parameter_Renewable_CapacityFactor", year_col="year", horizon="horizon")  # same as above
    return scenario


"""
flexible_generation model

Infeasible
"""


def run_model_flexible_generation():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="flexible_generation",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_cumulative_bound_tax(scenario)
    scenario = add_flexible_generation(scenario)
    scenario = remove_coal_ppl_growth_activity_up(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_flexible_generation(scenario: "Scenario"):
    scenario.add_set(set_name="rating", file_name="Set_Rating")
    scenario.add_ts_par(par_name="rating_bin", file_name="Parameter_FlexibleGeneration_TechnologyParent_RatingBin", year_col="year_act", horizon="horizon")
    scenario.add_ts_par(par_name="flexibility_factor", file_name="Parameter_FlexibleGeneration_TechnologyParent_FlexibilityFactor")
    return scenario


def remove_coal_ppl_growth_activity_up(scenario: "Scenario"):
    df = scenario.scenario.par("growth_activity_up", filters={"technology": "coal_ppl", "year_act": 700})
    scenario.scenario.remove_par("growth_activity_up", df)
    return scenario


"""
firm_capacity model
"""


def run_model_firm_capacity():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="firm_capacity",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_bound_cumulative(scenario)
    scenario = add_firm_capacity(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_firm_capacity(scenario: "Scenario"):
    scenario.add_set(set_name="rating", file_name="Set_Rating")
    scenario.add_ts_par(par_name="rating_bin", file_name="Parameter_FlexibleGeneration_TechnologyParent_RatingBin", year_col="year_act", horizon="horizon")
    scenario.add_ts_par(par_name="peak_load_factor", file_name="Parameter_FirmCapacity_PeakLoadFactor", year_col="year", horizon="horizon")
    scenario.add_ts_par(par_name="reliability_factor", file_name="Parameter_FirmCapacity_ReliabilityFactor", year_col="year_act", horizon="horizon")
    return scenario


"""
seasonality model
"""


def run_model_seasonality():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="seasonality",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_seasonality(scenario)
    scenario = add_time_hierarchy(scenario)
    scenario = add_duration_time(scenario)
    scenario = modify_parameters_yearly_to_season(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_seasonality(scenario: "Scenario"):
    scenario.add_set(set_name="time", file_name="Set_Time")
    scenario.add_set(set_name="lvl_temporal", file_name="Set_LvlTemporal")
    return scenario


def add_time_hierarchy(scenario: "Scenario"):
    time_steps = ["winter", "summer"]
    time_level = "season"
    for t in time_steps:
        scenario.scenario.add_set("map_temporal_hierarchy", [time_level, t, "year"])
    return scenario


def add_duration_time(scenario: "Scenario"):
    time_steps = ["winter", "summer"]
    for t in time_steps:
        scenario.scenario.add_par("duration_time", [t], 0.5, "-")
    return scenario


def yearly_to_season(scen, parameter, data, filters=None):
    if filters:
        old = scen.par(parameter, filters)
    else:
        old = scen.par(parameter)
    scen.remove_par(parameter, old)

    # Finding time related indexes
    time_idx = [x for x in scen.idx_names(parameter) if "time" in x]
    for h in data.keys():
        new = old.copy()
        for time in time_idx:
            new[time] = h
        new["value"] = data[h] * old["value"]
        scen.add_par(parameter, new)


def modify_parameters_yearly_to_season(scenario: "Scenario"):
    # Modifying the demand for each season
    demand_data = {"winter": 0.60, "summer": 0.40}
    yearly_to_season(scenario.scenario, "demand", demand_data)

    # Modifying input and output parameters for each season
    fixed_data = {"winter": 1, "summer": 1}
    yearly_to_season(scenario.scenario, "output", fixed_data)
    yearly_to_season(scenario.scenario, "input", fixed_data)

    # Modifying growth rates for each season
    yearly_to_season(scenario.scenario, "growth_activity_up", fixed_data)

    # Modifying capacity factor
    # Let's get the yearly capacity factor of wind in the baseline scenario
    cf_wind = scenario.scenario.par("capacity_factor", {"technology": "wind_ppl"})["value"].mean()
    # Converting yearly capacity factor to seasonal
    cf_data = {"winter": 0.46 / cf_wind, "summer": 0.25 / cf_wind}
    cf_filters = {"technology": "wind_ppl"}
    yearly_to_season(scenario.scenario, "capacity_factor", cf_data, cf_filters)
    # Capacity factor of other technologies remains unchanged in each season
    cf_filters = {"technology": ["coal_ppl", "bulb", "grid"]}
    yearly_to_season(scenario.scenario, "capacity_factor", fixed_data, cf_filters)

    # Modifying historical activity
    hist_data = {"winter": 0.5, "summer": 0.5}
    yearly_to_season(scenario.scenario, "historical_activity", hist_data)

    # Modifying variable cost
    yearly_to_season(scenario.scenario, "var_cost", fixed_data)

    return scenario


"""
share_constraint model
"""


def run_model_share_constraint():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="share_constraint",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_share_constraint(scenario)
    scenario = add_map_shares_commodity_total(scenario)
    scenario = add_map_shares_commodity_share(scenario)
    scenario = add_share_commodity_lo(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_share_constraint(scenario: "Scenario"):
    scenario.add_set(set_name="shares", file_name="Set_Share")
    scenario.add_category(set_name="technology", file_name="Category_ShareConstraint_Technology")
    return scenario


def add_map_shares_commodity_total(scenario: "Scenario"):
    shares = "share_renewable_electricity"
    type_tec = "electricity_total"
    df = pd.DataFrame(
        {
            "shares": [shares],
            "node_share": "Westeros",
            "node": "Westeros",
            "type_tec": type_tec,
            "mode": "standard",
            "commodity": "electricity",
            "level": "secondary",
        }
    )
    scenario.scenario.add_set("map_shares_commodity_total", df)
    return scenario


def add_map_shares_commodity_share(scenario: "Scenario"):
    shares = "share_renewable_electricity"
    type_tec = "electricity_renewable"
    df = pd.DataFrame(
        {
            "shares": [shares],
            "node_share": "Westeros",
            "node": "Westeros",
            "type_tec": type_tec,
            "mode": "standard",
            "commodity": "electricity",
            "level": "secondary",
        }
    )
    scenario.scenario.add_set("map_shares_commodity_share", df)
    return scenario


def add_share_commodity_lo(scenario: "Scenario"):
    shares = "share_renewable_electricity"
    df = pd.DataFrame(
        {
            "shares": shares,
            "node_share": "Westeros",
            "year_act": [720],
            "time": "year",
            "value": [0.5],
            "unit": "-",
        }
    )
    scenario.scenario.add_par("share_commodity_lo", df)
    return scenario


"""
soft_constraint model
"""


def run_model_soft_constraint():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="soft_constraint",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_emission(scenario)
    scenario = add_emission_cumulative_bound_tax(scenario)
    scenario = add_soft_constraint_activity_up(scenario)
    scenario = add_soft_constraint_activity_up_level_cost(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_soft_constraint_activity_up(scenario: "Scenario"):
    df = pd.DataFrame(
        {
            "node_loc": "Westeros",
            "technology": "wind_ppl",
            "year_act": [690, 700, 710, 720],
            "time": "year",
            "value": [0.0, 0.0, 0.0, 0.01],
            "unit": "-",
        }
    )
    scenario.scenario.add_par("soft_activity_up", df)
    return scenario


def add_soft_constraint_activity_up_level_cost(scenario: "Scenario"):
    df = pd.DataFrame(
        {
            "node_loc": "Westeros",
            "technology": "wind_ppl",
            "year_act": [690, 700, 710, 720],
            "time": "year",
            "value": 0.01,
            "unit": "-",
        }
    )
    scenario.scenario.add_par("level_cost_activity_soft_up", df)
    return scenario


"""
add_on_technology model
"""


def run_model_add_on_technology():
    config = Config(
        project_path=os.path.dirname(__file__),
        model_name="westeros",
        scenario_name="add_on_technology",
        year_start=690,
        year_end=720,
        year_step=10,
        year_base=700
    )
    scenario = Scenario(config=config)
    scenario = setup_baseline(scenario)
    scenario = add_add_on_technology(scenario)
    scenario.solve()
    run_reporter(config=config)


def add_add_on_technology(scenario: "Scenario"):
    scenario.add_set(set_name="addon", file_name="Set_Addon")
    scenario.add_ts_par(par_name="demand", file_name="Parameter_Addon_Demand", year_col="year", horizon="future")
    scenario.add_ts_par(par_name="input", file_name="Parameter_Addon_TechnologyParent_Input")
    scenario.add_ts_par(par_name="output", file_name="Parameter_Addon_TechnologyParent_Output")
    scenario.add_ts_par(par_name="technical_lifetime", file_name="Parameter_Addon_TechnologyParent_TechnicalLifetime", year_col="year_vtg", horizon="future")
    scenario.add_ts_par(par_name="fix_cost", file_name="Parameter_Addon_TechnologyParent_Cost_Fix")
    scenario.add_ts_par(par_name="inv_cost", file_name="Parameter_Addon_TechnologyParent_Cost_Investment", year_col="year_vtg", horizon="future")
    scenario.add_category(set_name="addon", file_name="Category_Addon_Technology")
    scenario.add_map(map_name="map_tec_addon", file_name="Map_TechnologyAddon")
    scenario.add_ts_par(par_name="addon_conversion", file_name="Parameter_Addon_Conversion")
    scenario.add_ts_par(par_name="addon_up", file_name="Parameter_Addon_Up", year_col="year_act", horizon="year_act")
    return scenario


if __name__ == "__main__":

    # run_model_baseline()
    # run_model_emission_bound_cumulative()
    # run_model_emission_bound_year()
    # run_model_emission_bound_cumulative_tax()
    # run_model_fossil_resource()
    # run_model_renewable()
    # run_model_flexible_generation()  # infeasible
    # run_model_firm_capacity()
    # run_model_seasonality()
    # run_model_share_constraint()
    # run_model_soft_constraint()
    run_model_add_on_technology()

