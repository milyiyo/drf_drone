def validate_fleet_size(drone_class, exception):
    """Check the max amount af drones that can be in the fleet."""
    fleet_size = drone_class.objects.count()
    if fleet_size >= 10:
        raise exception('The maximum amount of drones in the fleet is 10.')
