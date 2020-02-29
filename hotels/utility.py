def hotel_directory_path(instance, filename):
    return 'hotels/hotel_{0}/{1}'.format(instance.id, filename)


def room_directory_path(instance, filename):
    return 'rooms/room_{0}/{1}'.format(instance.id, filename)
