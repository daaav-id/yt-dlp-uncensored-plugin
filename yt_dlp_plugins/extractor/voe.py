from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    decode_packed_codes,
)

import base64
import json
import re

class VoeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(voe.sx|sandratableother.com|robertordercharacter.com|maxfinishseveral.com|alejandrocenturyoil.com|heatherwholeinvolve.com|hentaisword.com|kristiesoundsimply.com|jonathansociallike.com|mariatheserepublican.com|jilliandescribecompany.com)/e/(?P<id>[^/?#&]+)'
    _TESTS = []

    def _real_extract(self, url):
        video_id = self._match_id(url)

        #webpage = self._download_webpage(url, video_id)

        #url = self._html_search_regex(r'window.location.href = \'(?P<videoURL>[a-zA-Z0-9:/._\-]*)\'', webpage, 'videoURL')


        webpage = self._download_webpage(url, video_id)
        if "<title>Redirecting...</title>" in webpage:
            new_url = self._html_search_regex(r'window.location.href = \'(?P<videoURL>[a-zA-Z0-9:/._\-]*)\'', webpage, 'videoURL')
            print(new_url)
            return {
                '_type': 'url_transparent',
                'id': video_id,
                'title': self._generic_title(url) or video_id,
                'url': new_url
            }

        #get encoded value
        encoded_json = self._html_search_regex(r'<script type=\"application/json\">(?P<encodedjson>\[.*\])</script>', webpage, 'encodedjson')

        def rot13(text):
            """Apply ROT13 cipher to the text (only affects letters)."""
            result = ""
            for char in text:
                code = ord(char)
                if 65 <= code <= 90:  # A-Z
                    code = ((code - 65 + 13) % 26) + 65
                elif 97 <= code <= 122:  # a-z
                    code = ((code - 97 + 13) % 26) + 97
                result += chr(code)
            return result

        def replace_patterns(text):
            """Replace specific patterns with underscores."""
            patterns = ['@$', '^^', '~@', '%?', '*~', '!!', '#&']
            for pattern in patterns:
                text = text.replace(pattern, '')
            return text

        def decode_base64(text):
            """Decode base64 encoded string."""
            return base64.b64decode(text).decode('utf-8', errors='replace')

        def shift_chars(text, shift):
            """Shift character codes by specified amount."""
            return ''.join([chr(ord(char) - shift) for char in text])

        def reverse_string(text):
            """Reverse the string."""
            return text[::-1]

        def deobfuscate(obfuscated_json):
            # Parse the JSON to get the first element
            try:
                data = json.loads(obfuscated_json)
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
                    obfuscated_string = data[0]
                else:
                    return "Input doesn't match expected format."
            except json.JSONDecodeError:
                return "Invalid JSON input."
    
            # Apply transformations in sequence
            try:
                step1 = rot13(obfuscated_string)
                step2 = replace_patterns(step1)
                step4 = decode_base64(step2)
                step5 = shift_chars(step4, 3)
                step6 = reverse_string(step5)
                step7 = decode_base64(step6)
        
                # Parse the final result as JSON
                result = json.loads(step7)
                return result
            except Exception as e:
                return f"Error during deobfuscation: {str(e)}"

        source_json = deobfuscate(encoded_json)

        print(source_json)
        formats = []
        dl_url = None
        for source in source_json:
            #print(source)
            if source == 'hls':
                formats = self._extract_m3u8_formats(source_json[source], video_id, ext="mp4", entry_protocol='m3u8_native', m3u8_id="hls")
                break
            if source == 'mp4':
                formats.append({"url": source_json[source], "format_id": source})

        formats.append({"url": source_json['direct_access_url'], "format_id": 'mp4'})

        return {
            'id': video_id,
            'title': self._generic_title(url) or video_id,
            'formats': formats,
        }