""" The common utilization functions """
import os
import magic


# Utilization functions support for handling files

def create_media_path(custom_path=''):
    """ Generate the path to storing media data """
    def generate_path(instance, filename):
        if hasattr((instance), 'name'):
            return os.path.join(
                custom_path,
                instance.name,
                filename
            )

        return os.path.join(
            custom_path,
            filename
        )

    return generate_path


def get_file_mine(file, size_to_read=(5 * (1024 * 1024))):
    """ Return the mine of input file """
    return magic.from_buffer(file.read(size_to_read), mime=True)


def is_video(mine=None, file=None):
    """ Check a file is video """
    if file:
        mine = get_file_mine(file)
    print(mine)

    if mine:
        return mine.find('video') != -1

    return False


def is_image(mine=None, file=None):
    """ Check a file is video """
    if file:
        mine = get_file_mine(file)
    print(mine)
    if mine:
        return mine.find('image') != -1

    return False
