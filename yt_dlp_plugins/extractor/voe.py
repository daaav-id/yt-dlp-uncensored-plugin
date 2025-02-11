from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    decode_packed_codes,
)

import base64
import json

class VoeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(voe.sx|sandratableother.com|robertordercharacter.com|maxfinishseveral.com)/e/(?P<id>[^/?#&]+)'
    _TESTS = []

    def _real_extract(self, url):
        video_id = self._match_id(url)

        #webpage = self._download_webpage(url, video_id)

        #url = self._html_search_regex(r'window.location.href = \'(?P<videoURL>[a-zA-Z0-9:/._\-]*)\'', webpage, 'videoURL')


        webpage = self._download_webpage(url, video_id)
        if webpage.startswith("<script>"):
            print("found redirect")
            new_url = self._html_search_regex(r'window.location.href = \'(?P<videoURL>[a-zA-Z0-9:/._\-]*)\'', webpage, 'videoURL')
            print(new_url)
            return {
                '_type': 'url_transparent',
                'id': video_id,
                'title': self._generic_title(url) or video_id,
                'url': new_url
            }

        sources = self._html_search_regex(r'var sources = (?P<sources>[\S\s]*);[\S\s]*const video', webpage, 'sources')
        print(sources)
        sources = json.loads(sources.replace("'", '"').replace(', }', '}'))
        for source in sources:
            try:
                sources[source] = base64.b64decode(sources[source]).decode('utf-8')
            except:
                sources[source] = sources[source]
        print(sources)

        formats = []
        dl_url = None
        for source in sources:
            if source == 'hls':
                dl_url = sources[source]
                formats.append({"url": sources[source], "format_id": source, "manifest_url": sources[source]})
            if source == 'mp4':
                formats.append({"url": sources[source], "format_id": source})

        print(formats)

        #hls = self._html_search_regex(r'\'hls\':[\s]*\'(?P<hls>[a-zA-Z0-9=]*)\',', webpage, 'hls')
        #hls = str(base64.b64decode(hls))
        #print(hls)
        #formats = [{"url": mp4, "format_id": "mp4"}]

        return {
            #'type': 'url_transparent',
            'id': video_id,
            'title': self._generic_title(url) or video_id,
            'url': dl_url,
            'ext': 'mp4'
        }
