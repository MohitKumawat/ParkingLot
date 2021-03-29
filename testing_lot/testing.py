from parkinglot.service.parking_lot import ParkingLot


def test_parking_lot(input_file=None):
    if not input_file:
        input_file = 'testing_lot\input.txt'
    with open(input_file, 'r') as f:
        parking_lot = None
        parking_lot_id = None
        for line in f.readlines():
            line = line.strip()
            input_arr = line.split()
            if input_arr:
                if 'Create_parking_lot' == input_arr[0]:
                    try:
                        capacity = int(input_arr[1])
                    except:
                        print("Invalid command")
                    else:
                        parking_lot_res = ParkingLot.initialize(capacity)
                        if parking_lot_res['status'] == 1:
                            print (parking_lot_res['message'])
                            parking_lot = parking_lot_res['obj']
                            parking_lot_id = parking_lot_res['id']
                        else:
                            print(parking_lot_res['message'])
                else:
                    if parking_lot:
                        print(parking_lot.command_executor(input_arr, parking_lot_id))
                    else:
                        print("No Parking Lot Created")

            else:
                print("Invalid command")