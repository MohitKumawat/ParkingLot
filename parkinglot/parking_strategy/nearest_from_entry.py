from parkinglot.models import Parking
from parkinglot.parking_strategy.strategy_interface import Strategy

import heapq

# Sample implementation, could be implemented using db directly as well. For now using heap to retrieve minimum
# distance spots faster
class NearestFromEntry(Strategy):
    def get_slot(self):
        try:
            res =  heapq.heappop(self.heap)
            return {
                'data': res,
                'status': 1
            }
        except IndexError:
            return {
                'message': "No Vacant SPOT",
                'status': 0
            }

    def vacant_slot(self, spot):
        distance = spot.distance
        token_no = spot.token_no
        slot_details = (distance, spot.id, token_no)
        heapq.heappush(self.heap, slot_details)

    def __init__(self, spots_details):
        self.heap = spots_details
        heapq.heapify(spots_details)
