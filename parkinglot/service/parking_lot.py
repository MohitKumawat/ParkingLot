from parkinglot.models import Spot, Parking, ParkingLotModel
from parkinglot.parking_strategy.StrategyManager import StrategyManager


class ParkingLot:
    def __init__(self, capacity, strategy_obj):
        self.capacity = capacity
        self.strategy_obj = strategy_obj

    def command_executor(self, command_arr, parking_lot_id):
        # '''Park KA-01-HH-1234 driver_age 21'''
        if command_arr[0] == 'Park':
            if len(command_arr) != 4 or command_arr[2] != 'driver_age':
                return "Invalid Command"
            vehicle_no = command_arr[1]
            try:
                age = int(command_arr[3])
            except ValueError:
                return "Invalid User Age"
            get_slot_res = self.strategy_obj.get_slot()
            if get_slot_res['status'] == 1:
                dist, spot_id, token_no = get_slot_res['data']
                Parking.objects.create(spot_id=spot_id, vehicle_number=vehicle_no, age=age)
                return f'Car with vehicle registration number "{vehicle_no}" has been parked at slot number {token_no}'
            else:
                return get_slot_res['message']
        # Slot_numbers_for_driver_of_age 21
        # Vehicle_registration_number_for_driver_of_age 18
        if command_arr[0] == 'Slot_numbers_for_driver_of_age' or command_arr[0] == \
                'Vehicle_registration_number_for_driver_of_age':
            if len(command_arr) == 2:
                try:
                    age = int(command_arr[1])
                    req_result = 'spot__token_no' if command_arr[0] == 'Slot_numbers_for_driver_of_age' else \
                        'vehicle_number'
                    spots = list(Parking.objects.filter(status=Parking.OCCUPIED, age=age,
                                                        spot__parking_lot_id=parking_lot_id).
                                 values_list(req_result,flat=True))
                    return ', '.join(map(str, spots))
                except ValueError:
                    return "Invalid User Age"
            else:
                return "Invalid Command"
        # Slot_number_for_car_with_number PB-01-HH-1234
        if command_arr[0] == 'Slot_number_for_car_with_number':
            if len(command_arr) == 2:
                vehicle_no = command_arr[1]
                spot = Parking.objects.filter(status=Parking.OCCUPIED, vehicle_number=vehicle_no,
                                              spot__parking_lot_id=parking_lot_id).\
                    values('spot__token_no').last()
                if spot:
                    return spot["spot__token_no"]
                else:
                    return ""
            else:
                return "Invalid Command"
        # Leave 2
        if command_arr[0] == 'Leave':
            if len(command_arr) == 2:
                try:
                    token_no = int(command_arr[1])
                    parking_detail = Parking.objects.filter(spot__token_no=token_no, status=Parking.OCCUPIED,
                                                            spot__parking_lot_id=parking_lot_id).last()
                    if parking_detail:
                        spot = parking_detail.spot
                        self.strategy_obj.vacant_slot(spot)

                        parking_detail.status = Parking.VACANT
                        parking_detail.save()
                        return f'Slot number {token_no} vacated, the car with vehicle registration number ' \
                               f'"{parking_detail.vehicle_number}" left the space, the driver of the car was of age ' \
                               f'{parking_detail.age}'
                    else:
                        return "Invalid Token"
                except ValueError:
                    return "Invalid Command"
            else:
                return "Invalid Command"

        return "Invalid Command"

    @classmethod
    def initialize(cls, row_capacity, strategy="nearest_from_entry", rows=1):
        parking_lot_model_obj = ParkingLotModel.objects.create(strategy=strategy, capacity=row_capacity * rows)
        spots_details = Spot.create_spots(row_capacity, parking_lot_model_obj.id, rows)
        strategy_obj = StrategyManager.get_strategy(strategy, spots_details)
        if strategy_obj:
            return {
                'status': 1,
                'message': f"Created parking of {row_capacity} slots",
                'obj': ParkingLot(row_capacity, strategy_obj),
                'id': parking_lot_model_obj.id
            }
        else:
            return {
                'status': 0,
                'message': f"Invalid Strategy"
            }

