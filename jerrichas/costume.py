# Jerrichas by Jerricha@chat.cohtitan.com, Summer 2015!
# GPLv3

import csv

class CostumeCSV(object):
    """
    Represents a file produced with the /costumesave command in Icon.exe
    """
    def __init__(self, path):
        """
        :param path: /costumesave file path
        :type path: str
        """
        self.path = path

    def get_costumeparts(self):
        """
        :returns: a mapping of /costumesave elements to ParagonChatDB 'costumepart' columns
        """
        costume_csv = csv.reader(open(self.path, 'r'))
        costume = map(
            lambda row: dict(
                part=row[0],
                geom=row[1],
                tex1=row[2],
                tex2=row[3],
                bodytype=row[7],
                bonescale=row[10],
                shoulderscale=row[12],
                chestscale=row[13],
                waistscale=row[14],
                hipscale=row[15],
                legscale=row[16],
                # TODO: headscales ~ nosescales
                fx=row[39] if not row[39]=="0" else "",
                displayname=row[4],
                region=row[42],
                bodyset=row[43],
                # name=row[],
                color1=row[5],
                color2=row[6],
                # color3=row[],
                # color4=row[],
            ),
            costume_csv
        )
        return list(costume)

    def get_proportions(self):
        """
        :returns: a mapping of /costumesave records to ParagonChatDB 'costume' columns.
        """
        return None

class TailorSaved(object):
    """
    Represents a .costume file produced at the tailor / character creation screen.
    """
    pass
