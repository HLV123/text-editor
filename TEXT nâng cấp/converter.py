import urllib.parse
import base64
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import yaml
import csv
import io
import re

class Converter:
    def __init__(self):
        pass
    
    def url_encode(self, text):
        return urllib.parse.quote(text, safe='')
    
    def url_decode(self, text):
        try:
            return urllib.parse.unquote(text)
        except:
            return text
    
    def base64_encode(self, text):
        try:
            return base64.b64encode(text.encode('utf-8')).decode('ascii')
        except:
            return text
    
    def base64_decode(self, text):
        try:
            return base64.b64decode(text.encode('ascii')).decode('utf-8')
        except:
            return text
    
    def to_uppercase(self, text):
        return text.upper()
    
    def to_lowercase(self, text):
        return text.lower()
    
    def to_title_case(self, text):
        return text.title()
    
    def to_camel_case(self, text):
        words = re.split(r'[_\s-]+', text.strip())
        if not words:
            return text
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def to_snake_case(self, text):
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        text = re.sub(r'[_\s-]+', '_', text)
        return text.lower()
    
    def convert_encoding(self, text, from_encoding, to_encoding):
        try:
            if from_encoding == to_encoding:
                return text
            
            if from_encoding == 'auto':
                encodings = ['utf-8', 'utf-16', 'ascii', 'latin-1', 'windows-1252', 'iso-8859-1']
                for enc in encodings:
                    try:
                        text.encode(enc)
                        from_encoding = enc
                        break
                    except:
                        continue
                else:
                    from_encoding = 'utf-8'
            
            bytes_data = text.encode(from_encoding)
            return bytes_data.decode(to_encoding)
        except:
            return text
    
    def csv_to_json(self, csv_text):
        try:
            reader = csv.DictReader(io.StringIO(csv_text))
            data = list(reader)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def csv_to_xml(self, csv_text):
        try:
            reader = csv.DictReader(io.StringIO(csv_text))
            root = ET.Element('data')
            
            for row in reader:
                item = ET.SubElement(root, 'item')
                for key, value in row.items():
                    elem = ET.SubElement(item, key.replace(' ', '_'))
                    elem.text = str(value) if value else ''
            
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = xml.dom.minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        except Exception as e:
            return f"Error: {str(e)}"
    
    def json_to_xml(self, json_text):
        try:
            data = json.loads(json_text)
            
            def dict_to_xml(tag, d):
                elem = ET.Element(tag)
                if isinstance(d, dict):
                    for key, val in d.items():
                        child = dict_to_xml(key, val)
                        elem.append(child)
                elif isinstance(d, list):
                    for item in d:
                        child = dict_to_xml('item', item)
                        elem.append(child)
                else:
                    elem.text = str(d)
                return elem
            
            root = dict_to_xml('root', data)
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = xml.dom.minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        except Exception as e:
            return f"Error: {str(e)}"
    
    def xml_to_json(self, xml_text):
        try:
            def xml_to_dict(element):
                result = {}
                
                if element.attrib:
                    result.update(element.attrib)
                
                if element.text and element.text.strip():
                    if len(element) == 0:
                        return element.text.strip()
                    result['text'] = element.text.strip()
                
                for child in element:
                    child_data = xml_to_dict(child)
                    if child.tag in result:
                        if not isinstance(result[child.tag], list):
                            result[child.tag] = [result[child.tag]]
                        result[child.tag].append(child_data)
                    else:
                        result[child.tag] = child_data
                
                return result
            
            root = ET.fromstring(xml_text)
            data = {root.tag: xml_to_dict(root)}
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def json_to_yaml(self, json_text):
        try:
            data = json.loads(json_text)
            return yaml.dump(data, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def yaml_to_json(self, yaml_text):
        try:
            data = yaml.safe_load(yaml_text)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Error: {str(e)}"