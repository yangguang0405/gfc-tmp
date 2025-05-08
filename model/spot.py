
class Spot(dict):
    def __init__(self, id, name, creator, city, type, instruction=None, instruction_detail=None, address=None,navigation=None, 
                 browse_count=None, nearby_completed=False, spots=None, time_created=None):
        dict.__init__(self, id=id, name=name, creator=creator, instruction=instruction, instruction_detail=instruction_detail,
                       address=address, navigation=navigation,
                        browse_count=browse_count, nearby_completed=nearby_completed,
                        spots=spots, city=city, type=type, time_created=time_created)
