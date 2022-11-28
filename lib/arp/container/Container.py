class Container:
    def __init__(self):
        self.execution_strategies = {}
        self.state_comparisons = {}

    def put_execution_strategy(self, strategy_name, strategy):
        if strategy_name in self.execution_strategies:
            raise Exception(f'the strategy named {strategy_name} already exists!')
        else:
            self.execution_strategies[strategy_name] = strategy

    def put_state_comparison(self, comparison_name, comparison):
        if comparison_name in self.state_comparisons:
            raise Exception(f'the state comparison named {comparison_name} already exists!')
        else:
            self.state_comparisons[comparison_name] = comparison

    def get_execution_strategy(self, strategy_name):
        if strategy_name in self.execution_strategies:
            return self.execution_strategies[strategy_name]
        else:
            return None

    def get_state_comparison(self, comparison_name):
        if comparison_name in self.state_comparisons:
            return self.state_comparisons[comparison_name]
        else:
            return None
