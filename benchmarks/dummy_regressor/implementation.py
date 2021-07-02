from typing import Tuple
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor as dreg
from sklearn.metrics import mean_absolute_error
from ..common.benchmark_wrapper import BenchmarkWrapper
from time import sleep
import json

class DummyRegressor(BenchmarkWrapper):
    def __init__(self):
        self.benchmarkName = "DummyRegressor"
        super().__init__(self.benchmarkName)
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        self.preset_loc = self.home_dir.joinpath(
            "benchmarks", "dummy_regressor", "presets"
        )
        self.settings_loc = self.home_dir.joinpath(
            "benchmarks", "dummy_regressor", "settings"
        )

    def setSettings(self):
        with open(f"{self.settings_loc}/settings1.json") as f:
            _file = json.load(f)
            self.burnin:int = _file["burnin"]
            self.repetitions:int = _file["repetitions"]
            return self.burnin,self.repetitions

    def getPresets(self):
        pass

    def startBenchmark(self):
        print(self.dummyReg())

    def benchmarkStatus():
        # TODO : Communication with celery workers to see if the task is completed.
        pass

    def stopBenchmark():
        # TODO : Figure out stopping the benchmark
        pass

    def extractDataset(self):
        data, target = load_boston(return_X_y=True)
        sleep(0.05)                                    ##Used to debug the logs
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            data,
            target,
            test_size=0.2,
            shuffle=True,
            random_state=42,
        )

    def dummyReg(self) -> Tuple[dict,float]:
        with BenchmarkWrapper.Timer() as t:
            dummy_reg = dreg(strategy="mean")
            self.extractDataset()
            dummy_reg.fit(self.X_train, self.y_train)
            y_pred = dummy_reg.predict(self.X_test)
        results_dict = {
            "score": dummy_reg.score(self.y_test, y_pred),
            "Mean absolute error": mean_absolute_error(self.y_test, y_pred),
        }
        return results_dict,"{:.4f}".format(t.elapsed)
