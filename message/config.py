import os


class Config:

    def __init__(
            self,
            project_path: str,
            model_name: str,
            scenario_name: str,
            year_start: int,
            year_end: int,
            year_step: int,
            year_base: int
    ):
        self.project_path = project_path
        self.model_name = model_name
        self.scenario_name = scenario_name
        self.year_start = year_start
        self.year_end = year_end
        self.year_step = year_step
        self.year_base = year_base
        self.dir_input = self.create_folder("input")
        self.create_folder("output")
        self.dir_output = self.create_folder(f"output/{scenario_name}")
        self.dir_figure = self.create_folder("figure")

    def create_folder(self, folder_name: str):
        folder_path = os.path.join(self.project_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path


