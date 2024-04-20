import os
from typing import List
from typing import Optional
from typing import Union

import ixmp
import message_ix
import pandas as pd

from message.config import Config

YearType = Union["year_act", "year_vtg", "year"]
HorizonType = Union["future", "history"]


class Scenario:

    def __init__(self, config: "Config"):
        self.config = config
        self.mp = ixmp.Platform()
        self.scenario = message_ix.Scenario(
            mp=self.mp,
            model=self.config.model_name,
            scenario=self.config.scenario_name,
            version="new"
        )
        self.horizon = list(range(self.config.year_start, self.config.year_end + 1, self.config.year_step))
        self.history = [year for year in self.horizon if year < self.config.year_base]
        self.future = [year for year in self.horizon if year >= self.config.year_base]
        self.scenario.add_horizon(year=self.horizon, firstmodelyear=self.config.year_base)
        self.year_df = self.scenario.vintage_and_active_years()

    def load_xlsx(self, file_name: str):
        return pd.read_excel(os.path.join(self.config.dir_input, f'{file_name}.xlsx'))

    def add_set(self, set_name: str, file_name: str):
        df = self.load_xlsx(file_name)
        self.scenario.add_set(set_name, list(df["name"]))

    def add_category(self, set_name: str, file_name: str):
        df = self.load_xlsx(file_name)
        for _, row in df.iterrows():
            self.scenario.add_cat(set_name, row["category"], row["name"])

    def add_par(
        self,
        par_name: str,
        file_name: str,
    ):
        df = self.load_xlsx(file_name=file_name)
        self.add_unit_from_df(df=df)
        for _, row in df.iterrows():
            key_or_data = [row[col] for col in df.columns if col not in ["value", "unit"]]
            self.scenario.add_par(
                name=par_name,
                key_or_data=key_or_data,
                value=row["value"],
                unit=row["unit"],
            )

    def add_ts_par(
        self,
        par_name: str,
        file_name: str,
        year_col: Optional[YearType] = None,
        horizon: Optional[HorizonType] = None
    ):
        df = self.load_xlsx(file_name=file_name)
        self.add_unit_from_df(df=df)
        for _, row in df.iterrows():
            self.scenario.add_par(
                name=par_name,
                key_or_data=pd.DataFrame(
                    self.gen_ts_par_dict(
                        par_row=row,
                        index_cols=[col for col in df.columns if col not in self.horizon and col != "value"],
                        year_col=year_col,
                        horizon=horizon
                    )
                )
            )

    def add_unit_from_df(self, df: pd.DataFrame):
        if "unit" in df.columns:
            for unit in df["unit"].unique():
                self.add_unit(unit)

    def add_unit(self, unit: str):
        self.mp.add_unit(unit)

    def gen_ts_par_dict(
            self,
            par_row: pd.Series,
            index_cols: List[str],
            year_col: Optional[YearType] = None,
            horizon: Optional[HorizonType] = None
    ):
        par_dict = {}
        for col in index_cols:
            par_dict[col] = par_row[col]
        if year_col is None and horizon is None:
            par_dict["year_vtg"] = self.year_df["year_vtg"].to_list()
            par_dict["year_act"] = self.year_df["year_act"].to_list()
            par_dict["value"] = par_row["value"]
        else:
            par_dict[year_col] = self.__dict__[horizon]
            par_dict["value"] = [par_row[str(year)] for year in par_dict[year_col]]
        return par_dict

    def solve(self):
        self.scenario.commit(comment=self.config.scenario_name)
        self.scenario.set_as_default()
        self.scenario.solve()
        self.mp.close_db()



