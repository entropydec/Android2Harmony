from resource_management.ResourceManager import ResourceManager
from result_management.ResultManager import ResultManager
from Model.Task import Task
from executor.mcts.MCTSStrategy import MCTSStrategy
from executor.qlearning.QLearningStrategy import QLearningStrategy
from executor.random_search.RandomSearchStrategy import RandomSearchStrategy
from executor.appium_driver.AppiumScriptExecutor import AppiumScriptExecutor
from executor.dynamic_model.DynamicModelDriver import DynamicModelDriver
from executor.dynamic_model.ScriptSequenceDriver import ScriptSequenceDriver
from comparison.ActionsBasedStateComparison import ActionsBasedStateComparison
from comparison.XMLBasedStateComparison import XMLBasedStateComparison
from comparison.StringBasedStateComparison import StringBasedStateComparison
from container.Container import Container
from executor.Executor import Executor
from comparison.StateComparison import StateComparison
from executor.Executor import ExecutionStrategy
from comparison.StateComparison import StateComparisonStrategy


class AutomaticExploringFramework:
    def __init__(self):
        self.container = Container()
        self.result_manager = ResultManager()
        self.resource_manager = ResourceManager(self.container, self.result_manager)
        self.__registry()

    def __registry(self):
        self.container.put_execution_strategy(ExecutionStrategy.MCTS.value, MCTSStrategy)
        self.container.put_execution_strategy(ExecutionStrategy.Q_LEARNING.value, QLearningStrategy)
        self.container.put_execution_strategy(ExecutionStrategy.RANDOM.value, RandomSearchStrategy)
        self.container.put_execution_strategy(ExecutionStrategy.APPIUM.value, AppiumScriptExecutor)
        self.container.put_execution_strategy(ExecutionStrategy.SIMPLE_SCRIPT.value, RandomSearchStrategy)
        self.container.put_execution_strategy(ExecutionStrategy.DYNAMIC_MODEL.value, DynamicModelDriver)
        self.container.put_execution_strategy(ExecutionStrategy.SCRIPT_SEQUENCE.value, ScriptSequenceDriver)
        self.container.put_state_comparison(StateComparisonStrategy.XML.value, XMLBasedStateComparison)
        self.container.put_state_comparison(StateComparisonStrategy.ACTION.value, ActionsBasedStateComparison)
        self.container.put_state_comparison(StateComparisonStrategy.STRING.value, StringBasedStateComparison)

    def append_execution_strategy(self, strategy_name, strategy: Executor):
        self.container.put_execution_strategy(strategy_name, strategy)

    def append_state_comparison(self, comparison_name, comparison: StateComparison):
        self.container.put_state_comparison(comparison_name, comparison)

    def start(self):
        self.result_manager.start()
        self.resource_manager.start()

    def receive_task(self, task: Task):
        self.resource_manager.commit_task(task)

    def receive_tasks(self, tasks):
        for task in tasks:
            self.receive_task(task)
