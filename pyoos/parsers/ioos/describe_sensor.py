from pyoos.utils.etree import etree
from owslib.namespaces import Namespaces

ns = Namespaces()
SML_NS = ns.get_versioned_namespace('sml', '1.0.1')
SWE_NS = [ns.get_versioned_namespace('swe', '1.0.1')]

class IoosDescribeSensor(object):

    def __new__(cls, element):
        if isinstance(element, str):
            root = etree.fromstring(element)
        else:
            root = element

        sml_str = ".//{{{0}}}identifier/{{{0}}}Term[@definition='http://mmisw.org/ont/ioos/definition/%s']".format(SML_NS)

        if hasattr(root, 'getroot'):
            root = root.getroot()

        # circular dependencies are bad. consider a reorganization
        # find the the proper type for the DescribeSensor
        from pyoos.parsers.ioos.one.describe_sensor import (NetworkDS,
                                                            StationDS, SensorDS)
        for ds_type, constructor in [('networkID', NetworkDS), ('stationID', StationDS), ('sensorID', SensorDS)]:
            if root.find(sml_str % ds_type) is not None:
                return super(IoosDescribeSensor, cls).__new__(constructor)
        # if we don't find the proper request from the IOOS definitions,
        # try to adapt a generic DescribeSensor request to the dataset
        from pyoos.parsers.ioos.one.describe_sensor import GenericSensor
        return super(IoosDescribeSensor, cls).__new__(GenericSensor)
