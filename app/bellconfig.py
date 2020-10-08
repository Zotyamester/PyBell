from xml.dom import minidom

WEEK = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
TIME = ['h', 'm', 's']

class BellConfig:

    class Ring:
        def __init__(self, soundfile, days, times):
            self.soundfile = soundfile
            self.days = days
            self.times = times

    def __init__(self):
        self.rings = None

    def load(self, filename):
        doc = minidom.parse(filename)
        dRings = doc.getElementsByTagName('ring')
        self.rings = []
        for dRing in dRings:
            soundfile_node = dRing.getElementsByTagName('media')[0]
            soundfile = soundfile_node.firstChild.nodeValue
            days_node = dRing.getElementsByTagName('days')[0]
            days = {x: (days_node.attributes[x].firstChild.nodeValue == '1') for x in WEEK}
            time_nodes = dRing.getElementsByTagName('time')
            times = [{x: int(time_node.attributes[x].firstChild.nodeValue) for x in TIME} for time_node in time_nodes]

            ring = BellConfig.Ring(soundfile, days, times)
            self.rings.append(ring)

    def save(self, filename):
        doc = minidom.Document()
        bell_node = doc.createElement('bell')
        for ring in self.rings:
            ring_node = doc.createElement('ring')

            soundfile_node = doc.createElement('media')
            soundfile_node.appendChild(doc.createTextNode(ring.soundfile))
            ring_node.appendChild(soundfile_node)

            days_node = doc.createElement('days')
            for dayOfWeek, value in ring.days.items():
                days_node.setAttribute(dayOfWeek, str(int(value)))
            ring_node.appendChild(days_node)

            for time in ring.times:
                time_node = doc.createElement('time')
                for unit, value in time.items():
                    time_node.setAttribute(unit, str(value))
                ring_node.appendChild(time_node)

            bell_node.appendChild(ring_node)
        doc.appendChild(bell_node)
        with open(filename, 'w') as file:
            file.write(doc.toprettyxml())
