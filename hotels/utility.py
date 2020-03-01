def hotel_directory_path(instance, filename):
    return 'hotels/hotel_{0}/{1}'.format(instance.id, filename)


def room_directory_path(instance, filename):
    return 'rooms/room_{0}/{1}'.format(instance.id, filename)


def calculate_nights(object):
    start_date = object.start_date
    end_date = object.end_date
    delta = abs(end_date - start_date)  # need to improve it by adding validation on end_date
    return delta.days
