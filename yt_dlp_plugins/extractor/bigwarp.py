from yt_dlp.extractor.common import InfoExtractor

import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


class BigwarpIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(bigwarp.io)/embed-(?P<id>[^/?#&]+).html'


    def _real_extract(self, url):
        video_id = self._match_id(url)
        #print(video_id)
        headers = {
            'User-Agent': randomword(16),
            'Accept': 'text/html',
            #'Referer': url,
            'Sec-Fetch-Dest': 'iframe',
        }
        new_url = url.replace('io/embed-', 'art/')
        #print(new_url)
        webpage, urlh = self._download_webpage_handle(new_url, video_id, headers=headers)
        #print(webpage)

        jwpdata = self._find_jwplayer_data(webpage)
        #print(jwpdata)
        formats = self._parse_jwplayer_formats(jwpdata['sources'])
        #print(formats)

        title = self._html_extract_title(webpage)

        return {
            #'_type': 'url_transparent',
            '_type': 'video',
            'id': video_id,
            'formats': formats,
            'title': title,
        }
        