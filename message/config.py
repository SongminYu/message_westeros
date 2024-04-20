import os


class Config:

    def __init__(
            self,
            model_name: str,
            scenario_name: str,
            year_start: int,
            year_end: int,
            year_step: int,
            year_base: int
    ):
        self.model_name = model_name
        self.scenario_name = scenario_name
        self.year_start = year_start
        self.year_end = year_end
        self.year_step = year_step
        self.year_base = year_base
        self.dir_input = self.setup_folder("input")
        self.dir_output = self.setup_folder("output")
        self.dir_figure = self.setup_folder("figure")

    @staticmethod
    def setup_folder(path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        return path


