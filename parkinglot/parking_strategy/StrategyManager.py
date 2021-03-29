from parkinglot.parking_strategy.nearest_from_entry import NearestFromEntry


class StrategyManager:
    @classmethod
    def get_strategy(cls, strategy, spots_details):
        if strategy == 'nearest_from_entry':
            return NearestFromEntry(spots_details)
        return None