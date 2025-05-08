
class NearbySpot(dict):
    def __init__(self, spot_id, other_spot_id, distance):
        dict.__init__(self, spot_id=spot_id, other_spot_id=other_spot_id, distance=distance)
