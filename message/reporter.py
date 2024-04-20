import os.path

import ixmp
import message_ix

from message.config import Config


class Reporter:

    def __init__(self, config: "Config"):
        self.config = config
        self.mp = ixmp.Platform()
        self.scenario = message_ix.Scenario(
            mp=self.mp,
            model=self.config.model_name,
            scenario=self.config.scenario_name
        ).clone()
        self.scenario.to_excel(os.path.join(self.config.dir_output, f'{self.config.scenario_name}.xlsx'))
        self.reporter = message_ix.Reporter.from_scenario(self.scenario)
        ixmp.report.configure(units={"replace": {"-": ""}})

    def main(self):
        self.test()
        self.test_save_data()
        self.mp.close_db()

    def test(self):
        print(self.scenario.var("PRICE_EMISSION", {"node": "Westeros"}))

    def test_save_data(self):
        DATA_NAMES = [
            "ACT",
            "CAP",

            "out",
            "output",
            "out_hist",
            "ref_activity",

            "in",
            "input",
            "in_hist",

            "emi",
            "emission_factor",
            "emi_hist",

            "inv",
            "inv_cost",
            "CAP_NEW",
            "inv_hist",
            "ref_new_capacity",

            "fom",
            "fix_cost",
            "fom_hist",
            "ref_capacity",

            "vom",
            "var_cost",
            "vom_hist",
            "ref_activity",

            "tom",

            "C", 'COST_NODAL', 'COST_NODAL_NET', 'DEMAND', 'EMISS', 'EXT', 'GDP', 'I', 'LAND', 'OBJ', 'PRICE_COMMODITY',
            'PRICE_EMISSION', 'REL', 'STOCK', 'STORAGE', 'STORAGE_CHARGE'
        ]
        for data_name in DATA_NAMES:
            try:
                self.save_data(data_name=data_name)
            except:
                print(f'missing --> {data_name}')

    def save_data(self, data_name: str):
        self.reporter.write(self.reporter.get(data_name), os.path.join(self.config.dir_output, f'{data_name}.csv'))
