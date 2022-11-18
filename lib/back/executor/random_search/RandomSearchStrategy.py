from executor.Strategy import Strategy
from executor.event_extractor.Action import Action
import time
import random


class RandomSearchStrategy(Strategy):

    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.time_limit = self.parameters['time_limit']

    def get_action(self, state, actions) -> Action:
        random_num = random.randint(0, len(actions) - 1)
        # print(actions[random_num].action_type)
        return actions[random_num]

    def get_termination(self) -> dict:
        termination = {'start_time': time.time()}
        return termination

    def terminate(self, **termination) -> bool:
        start_time = termination['start_time']
        current_t = time.time()
        return (current_t - start_time) >= self.time_limit
