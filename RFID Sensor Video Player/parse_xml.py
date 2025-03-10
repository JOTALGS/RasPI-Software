import xml.etree.ElementTree as ET

# XML file path
xml_file = '/home/pi/Desktop/Scripts/RFIDSensorVideoPlayer/settings/videos.xml'

def parse_xml():
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    video_paths = {}
    all_cards_id = []
    for card in root.findall('card'):
        card_id = card.get('id')
        path = card.text.strip()
        video_paths[card_id] = path
        all_cards_id.append(card_id)
    
    screensaver_path = root.find('screensaver').text.strip()
    
    return video_paths, screensaver_path, all_cards_id
