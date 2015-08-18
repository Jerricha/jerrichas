# Jerrichas by Jerricha@chat.cohtitan.com, Summer 2015!
# GPLv3

from .base import BaseCostumeSave
from . import utils
import xml.etree.ElementTree as ET


class SentinelPlusXML(BaseCostumeSave):
    """
    Represents a Titan Sentinel+ costume XML
    http://cit.cohtitan.com/sentinelplus/
    """
    def __init__(self, fp):
        """
        :param fp: /Sentinel+ file
        :type fp: file
        """
        super()
        self.costume_map_list = self.parse(fp)

    def parse(self, fp):
        """
        :param fp: /Sentinel+ file
        :type fp: file
        """
        costumes_tree = ET.parse(fp).find('costumes')
        assert isinstance(costumes_tree, ET.Element)
        costume_map_list = [] # a list of all costumes in a character save

        for costume in costumes_tree.findall('costume'):
            assert isinstance(costume, ET.Element)
            # one costume_map per costume
            costume_map = {}
            costume_map_list.append(costume_map)
            costume_map['bodytype'] = costume.find('bodytype').text
            costume_map['skincolor'] = costume.find('skincolor').text # already encoded for db schema
            scales = costume.find('scales').text.split()
            scales = [float(scale) for scale in scales]
            """:type: str"""

            assert(scales.__len__() == 30) # 7 atomic scales + 7 composite scales (each 3) + 2 padding

            # for documentation of the following, see https://github.com/jerricha-and-friends/jerrichas/issues/10
            costume_map['bodyscale'] = scales[0]
            costume_map['bonescale'] = scales[1]
            costume_map['shoulderscale'] = scales[3]
            costume_map['chestscale'] = scales[4]
            costume_map['waistscale'] = scales[5]
            costume_map['hipscale'] = scales[6]
            costume_map['legscale'] = scales[7]

            costume_map['headscales'] = utils.floats_to_int(scales[9:11+1])
            costume_map['browscales'] = utils.floats_to_int(scales[12:14+1])
            costume_map['cheekscales'] = utils.floats_to_int(scales[15:17+1])
            costume_map['chinscales'] = utils.floats_to_int(scales[18:20+1])
            costume_map['craniumscales'] = utils.floats_to_int(scales[21:23+1])
            costume_map['jawscales'] = utils.floats_to_int(scales[24:26+1])
            costume_map['nosecales'] = utils.floats_to_int(scales[27:29+1])

            # iterate through parts

            part_index = 0
            for part in costume.findall('part'):
                assert isinstance(part, ET.Element)
                part_contents = part.text.split()
                part_map = {}
                costume_map[part_index] = part_map
                part_map['part'] = part_index

                # for documentation of the following, see https://github.com/jerricha-and-friends/jerrichas/issues/10
                part_map['geom'] = part_contents[0] \
                    if part_contents[0] is not 'none' \
                    else ''
                part_map['tex1'] = part_contents[1] \
                    if part_contents[1] is not 'none' \
                    else ''
                part_map['tex2'] = part_contents[2] \
                    if part_contents[2] is not 'none' \
                    else ''
                part_map['color1'] = part_contents[3]
                part_map['color2'] = part_contents[4]
                if part_contents.__len__() > 5:
                    part_map['color3'] = part_contents[5]
                    part_map['color4'] = part_contents[6]
                    part_map['fx'] = part_contents[7]

                part_index += 1

        return costume_map_list

    def get_costumeparts(self, costume_id):
        """
        :param costume_id: int between 0 and 9
        :returns: a mapping of /Sentinel+ costume elements to ParagonChatDB 'costumepart' columns
        """
        super()
        assert(0 <= costume_id <= 9)
        if self.costume_map_list.__len__ < costume_id + 1:
            raise IndexError

        nth_map = self.costume_map_list[costume_id]
        result = []

        for key in nth_map:
            if key.isdigit():
                result.append(nth_map[key])
        return sorted(result, key = lambda k: k['part'])

    def get_scales(self, costume_id):
        """
        :param costume_id: int between 0 and 9
        :returns: a mapping of /Sentinel+ costume records to ParagonChatDB 'costume' columns.
        """
        super()
        assert(0 <= costume_id <= 9)
        if self.costume_map_list.__len__ < costume_id + 1:
            raise IndexError

        nth_map = self.costume_map_list[costume_id]
        result = {
            'bodytype' : nth_map['bodytype'],
            'skincolor' : nth_map['skincolor'],
            'bodyscale' : nth_map['bodyscale'],
            'bonescale' : nth_map['bonescale'],
            'shoulderscale' : nth_map['shoulderscale'],
            'chestscale' : nth_map['chestscale'],
            'waistscale' : nth_map['waistscale'],
            'hipscale' : nth_map['hipscale'],
            'legscale' : nth_map['legscale'],
            'headscales' : nth_map['headscales'],
            'browscales' : nth_map['browscales'],
            'cheekscales' : nth_map['cheekscales'],
            'chinscales' : nth_map['chinscales'],
            'craniumscales' : nth_map['craniumscales'],
            'jawscales' : nth_map['jawscales'],
            'nosescales' : nth_map['nosescales']
        }
        return result
