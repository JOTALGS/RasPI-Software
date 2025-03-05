import xml.etree.ElementTree as ET

# XML file path
xml_file = '/home/pi/Desktop/Scripts/Touch Sensor Video Player/settings/videos.xml'

def parse_xml():
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    video_paths = {}
    sensor_pins = []
    for sensor in root.findall('sensor'):
        pin = int(sensor.get('pin'))
        path = sensor.text.strip()
        video_paths[pin] = path
        sensor_pins.append(pin)
    
    screensaver_path = root.find('screensaver').text.strip()
    
    return video_paths, screensaver_path, sensor_pins
