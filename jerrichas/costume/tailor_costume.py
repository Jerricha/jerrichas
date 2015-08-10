# Jerrichas by Jerricha@chat.cohtitan.com, Summer 2015!
# module by ROBOKiTTY
# GPLv3

from . import BaseCostumeSave
from .. import utils


class TailorCostume(BaseCostumeSave):
    """
    Represents a .costume file saved from in-game tailor
    """
    def __init__(self, path):
        """
        :param path: /.costume file path
        :type path: str
        """
        super()
        self.costume_map = self.parse(path)

    def parse(self, path):
        """
        :returns: a list of maps of .costume elements
        """
        file = open(path, mode = 'r')
        costume_map = {}
        fileDepth = 0
        part_index = 0

        for raw_line in file.readlines():
            line = raw_line.strip()
            segments = [segment.strip() for segment in line.split(',')]
            segments[0] = segments[0].lower()
            key_name = segments[0]
            if line == '' or line == '\n' or line.startswith("CostumePart"):
                pass
            if fileDepth == 0:
                if line == '{':
                    fileDepth = 1
            elif fileDepth == 1:
                if line == '{':
                    fileDepth = 2
                elif line == '}':
                    fileDepth = 0
                else:
                    if key_name == 'costumefileprefix' or key_name == 'numparts': # unused values
                        pass
                    elif key_name == 'scale':
                        key_name = 'bodyscale'

                    # convert arrays of decimals into single integer per ParagonChat db schema
                    if key_name.endswith('scales'):
                        scales = [float(each) for each in segments[1:]]
                        costume_map[key_name] = utils.floats_to_int(scales)
                    # convert skincolor RGB values into single integer per ParagonChat db schema
                    elif key_name == 'skincolor':
                        colour_vals = [int(each) for each in segments[1:]]
                        costume_map[key_name] = utils.encode_colour(colour_vals)
                    else:
                        if segments[1:][0] == 'none':
                            costume_map[part_index][key_name] = ''
                        else:
                            costume_map[part_index][key_name] = segments[1:]
            elif fileDepth == 2:
                if line == '}':
                    if costume_map.get('fx') is None:
                        costume_map['fx'] = ""
                    elif costume_map.get('displayname') is None:
                        costume_map['displayname'] = ''
                    elif costume_map.get('region') is None:
                        costume_map['region'] = ''
                    elif costume_map.get('bodyset') is None:
                        costume_map['bodyset'] = ''
                    fileDepth = 1
                    part_index += 1
                else:
                    if part_index not in costume_map:
                        costume_map[part_index] = {'part': part_index}
                    if key_name == 'geometry':
                        key_name = 'geom'
                    elif key_name == 'texture1':
                        key_name = 'tex1'
                    elif key_name == 'texture2':
                        key_name = 'tex2'
                    elif key_name == 'regionname':
                        key_name = 'region'
                    elif key_name == 'bodysetname':
                        key_name = 'bodyset'

                    if key_name.startswith('color'):
                        colour_vals = [int(each) for each in segments[1:]]
                        costume_map[key_name] = utils.encode_colour(colour_vals)
                    else:
                        if segments[1:][0] == 'none':
                            costume_map[part_index][key_name] = ''
                        else:
                            costume_map[part_index][key_name] = segments[1:]

        # TODO: set other default values here?
        return costume_map

    def get_costumeparts(self):
        """
        :returns: a mapping of /.costume elements to ParagonChatDB 'costumepart' columns
        """
        super()
        return None

    def get_proportions(self):
        """
        :returns: a mapping of /.costume records to ParagonChatDB 'costume' columns.
        """
        super()
        return None
