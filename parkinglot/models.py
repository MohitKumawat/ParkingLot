from django.db import models
from django.db.models import Model, CASCADE


class ParkingLotModel(Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    strategy = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)

class Spot(Model):
    token_no = models.PositiveIntegerField()
    row = models.PositiveIntegerField(default=0)
    col = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    parking_lot = models.ForeignKey(ParkingLotModel, on_delete=CASCADE, null=True)


    @classmethod
    def create_spots(cls, row_capacity, parking_lot_id, rows=1):
        spots = []
        token_no = 1
        for row in range(1, rows + 1):
            for col in range(1, row_capacity + 1):
                # distance can vary according to arrangement of parking spot
                distance = row * row_capacity + col
                spot = Spot.objects.create(row=row, col=col, token_no=token_no,
                                           parking_lot_id=parking_lot_id, distance=distance)
                spots.append((distance, spot.id, token_no))
                token_no += 1
        return spots

class Parking(Model):
    OCCUPIED = 1
    VACANT = 2

    status_choices = [
        (OCCUPIED, 'Occupied'),
        (VACANT, 'Vacant')
    ]
    spot = models.ForeignKey(Spot, on_delete=CASCADE)
    vehicle_number = models.CharField(max_length=13, db_index=True)
    age = models.PositiveIntegerField(db_index=True)
    park_in_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=status_choices, default=OCCUPIED)
    # Later on vehicle_number, age... could be moved to separate table to take care of different vehicle type and charges
