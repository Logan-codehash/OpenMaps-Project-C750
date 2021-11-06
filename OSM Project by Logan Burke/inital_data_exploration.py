#exploring inital data

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import unicodedata
from collections import defaultdict

#path to osm file
osm_path = "Longview_Home_Full.osm"

#creates the csv files
nodes_path = "nodes_inital.csv"
node_tags_path = "nodes_tags_inital.csv"
ways_path = "ways_inital.csv"
way_nodes_path = "ways_nodes_inital.csv"
way_tags_path = "ways_tags_inital.csv"

#checking for chars that cause issues
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#structure the csv fields
node_fields = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
node_tags_fields = ['id', 'key', 'value', 'type']
way_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
way_tags_fields = ['id', 'key', 'value', 'type']
way_nodes_fields = ['id', 'node_id', 'position']

#structures and processes the data
def shaper(element, node_attr_fields = node_fields, way_attr_fields = way_fields, problemchars = problem_chars, default_tag_type = 'regular'):
	node_attribs = {}
	way_attribs = {}
	way_nodes = []
	tags = []
	if element.tag == 'node':
		for fields in node_attr_fields:
			node_attribs[fields] = element.attrib[fields]
		for t in element.iter('tag'):
			t_dict = {}
			t_dict['id'] = element.attrib['id']
			#if there are any proboblem chars, that part will be skipped
			if problemchars.match(t.attrib['k']):
				continue;
			if not(':' in t.attrib['k']):
				t_dict['key'] = t.attrib['k']
				t_dict['type'] = 'regular';
			else:
				key_str = t.attrib['k']
				val = key_str.split(':')
				value = ''
				for items in val[1:]:
					value +=items
				t_dict['key'] = value
				t_dict['type'] = val[0]
			#structuring the data for tags
			if t.attrib['k'] == 'addr:street':
				t_dict['value'] = t.attrib['v']
			elif t.attrib['k'] == 'addr:city':
				t_dict['value'] = t.attrib['v']
			elif t.attrib['k'] == 'addr:postcode':
				t_dict['value'] =  t.attrib['v']
			elif t.attrib['k'] == 'phone':
				t_dict['value'] =  t.attrib['v']
			else:
				t_dict['value'] = t.attrib['v']
			tags.append(t_dict)
	elif element.tag == 'way':
		for fields in way_attr_fields:
			way_attribs[fields] = element.attrib[fields]
		for t in element.iter('tag'):
			t_dict = {}
			t_dict['id'] = element.attrib['id']
			if problemchars.match(t.attrib['k']):
				continue;
			if not(':' in t.attrib['k']):
				t_dict['key'] = t.attrib['k']
				t_dict['type'] = 'regular';
			else:
				key_str = t.attrib['k']
				val = key_str.split(':',1)
				t_dict['key'] = val[1]
				t_dict['type'] = val[0]
			#structuring the data for tags
			if t.attrib['k'] == 'addr:street':
				t_dict['value'] =  t.attrib['v']
			elif t.attrib['k'] == 'addr:city':
				t_dict['value'] =  t.attrib['v']
			elif t.attrib['k'] == 'addr:postcode':
				t_dict['value'] =  t.attrib['v']
			elif t.attrib['k'] == 'phone':
				t_dict['value'] =  t.attrib['v']
			else:
				t_dict['value'] = t.attrib['v']
			tags.append(t_dict)
		p = 0
		for w in element.iter('nd'):
			wd = {}
			wd['id'] = element.attrib['id']
			wd['node_id'] = w.attrib['ref']
			wd['position'] = p
			way_nodes.append(wd)
			p += 1
	if element.tag == 'node':
		return {'node': node_attribs, 'node_tags': tags}
	elif element.tag == 'way':
		return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

#handles the osm file
def get_element(osm_file, tags=('node', 'way', 'relation')):
	context = ET.iterparse(osm_file, events = ('start', 'end'))
	_, root = next(context)
	for event, elem in context:
		if event == 'end' and elem.tag in tags:
			yield elem
			root.clear()

#so it can handle unicode in python 2.7
class UnicodeDictWriter(csv.DictWriter, object):
	def write_row(self, row):
		super(UnicodeDictWriter, self).writerow({
			k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
		})

	def write_rows(self, rows):
		for row in rows:
			self.write_row(row)

#main function
def process_map(file_in):
	with codecs.open(nodes_path, 'w') as nodes_file, \
		 codecs.open(node_tags_path, 'w') as nodes_tags_file, \
		 codecs.open(ways_path, 'w') as ways_file, \
		 codecs.open(way_nodes_path, 'w') as way_nodes_file, \
		 codecs.open(way_tags_path, 'w') as way_tags_file:

		nodes_writer = UnicodeDictWriter(nodes_file, node_fields)
		node_tags_writer = UnicodeDictWriter(nodes_tags_file, node_tags_fields)
		ways_writer = UnicodeDictWriter(ways_file, way_fields)
		way_nodes_writer = UnicodeDictWriter(way_nodes_file, way_nodes_fields)
		way_tags_writer = UnicodeDictWriter(way_tags_file, way_tags_fields)

		nodes_writer.writeheader()
		node_tags_writer.writeheader()
		ways_writer.writeheader()
		way_nodes_writer.writeheader()
		way_tags_writer.writeheader()

                #goes through the file and writes the data
		for element in get_element(file_in, tags = ('node', 'way')):
			elem = shaper(element)
			if elem:
				if element.tag == 'node':
					nodes_writer.write_row(elem['node'])
					node_tags_writer.write_rows(elem['node_tags'])
				elif element.tag == 'way':
					ways_writer.write_row(elem['way'])
					way_nodes_writer.write_rows(elem['way_nodes'])
					way_tags_writer.write_rows(elem['way_tags'])


if __name__ == '__main__':
	process_map(osm_path)
	#print a visual notice that process is completed. Makes it easier for me.
	print('finished')
