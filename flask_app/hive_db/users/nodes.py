from beem.hive import Hive
from beem.nodelist import NodeList

nodelist = NodeList()
nodelist.update_nodes()
hive_instance = Hive(node=nodelist.get_hive_nodes())

