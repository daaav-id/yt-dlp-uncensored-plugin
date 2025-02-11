from yt_dlp.extractor.common import InfoExtractor

import random
import string
import time


class DoodStreamIE(InfoExtractor):
    _VALID_URL = r'(?P<domain>https?://(?:www\.)?(d((o*)|(0*))?d?(s)?(ter)?(2play)?)\.(?:com|to|watch|so|pm|wf|re|pro|la|li|work))/(?P<type>[ed])/(?P<id>[a-z0-9]+)'
    _TESTS = [{
        'url': 'http://dood.to/e/5s1wmbdacezb',
        'md5': '4568b83b31e13242b3f1ff96c55f0595',
        'info_dict': {
            'id': '5s1wmbdacezb',
            'ext': 'mp4',
            'title': 'Kat Wonders - Monthly May 2020',
            'description': 'Kat Wonders - Monthly May 2020 | DoodStream.com',
            'thumbnail': 'https://img.doodcdn.com/snaps/flyus84qgl2fsk4g.jpg',
        }
    }, {
        'url': 'http://dood.watch/d/5s1wmbdacezb',
        'md5': '4568b83b31e13242b3f1ff96c55f0595',
        'info_dict': {
            'id': '5s1wmbdacezb',
            'ext': 'mp4',
            'title': 'Kat Wonders - Monthly May 2020',
            'description': 'Kat Wonders - Monthly May 2020 | DoodStream.com',
            'thumbnail': 'https://img.doodcdn.com/snaps/flyus84qgl2fsk4g.jpg',
        }
    }, {
        'url': 'https://dood.to/d/jzrxn12t2s7n',
        'md5': '3207e199426eca7c2aa23c2872e6728a',
        'info_dict': {
            'id': 'jzrxn12t2s7n',
            'ext': 'mp4',
            'title': 'Stacy Cruz Cute ALLWAYSWELL',
            'description': 'Stacy Cruz Cute ALLWAYSWELL | DoodStream.com',
            'thumbnail': 'https://img.doodcdn.com/snaps/8edqd5nppkac3x8u.jpg',
        }
    }, {
        'url': 'https://dood.wf/d/whnhimxle634njcagq70gbcemsxetnph',
        'md5': 'f5a091c30ae5420d31d1eac894979f9b',
        'info_dict': {
            'id': 'f3ivss8ct9woqkdbonbai1g5y06e7wpn',
            'ext': 'mp4',
            'title': 'Rick Astley - Never Gonna Give You Up - DoodStream',
            'description': 'Rick Astley - Never Gonna Give You Up - DoodStream',
            'thumbnail': 'https://img.doodcdn.co/splash/hsebus0la2mqtzdh.jpg',
        }
    }, {
        'url': 'https://dood.so/d/jzrxn12t2s7n',
        'only_matching': True
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        #type = self._match_valid_url(url).group('type')
        proto_domain = self._match_valid_url(url).group('domain')

        headers = {
            'User-Agent': 'curl',
            'Accept': '*/*',
        }
        webpage, urlh = self._download_webpage_handle(url, video_id, headers=headers)
        # sometimes we are redirected to another doodstream domain, so handle that...
        if urlh.url != url:
            self.report_warning(f'Redirected to {urlh.url}')
            url = urlh.url
            video_id = self._match_id(url)
            proto_domain = self._search_regex(r'(?P<proto_domain>https?://[^/]+)', url, 'proto_domain')

        title = self._html_extract_title(webpage)
        thumb = self._html_search_meta('og:image', webpage, 'thumbnail', fatal=False)

        hash = self._html_search_regex(r'[?&]hash=([a-z0-9-]+)[&\']', webpage, 'hash')
        token = self._html_search_regex(r'[?&]token=([a-z0-9]+)[&\']', webpage, 'token')
        # pass_md5 = self._html_search_regex(r'(/pass_md5.*?)\'', webpage, 'pass_md5')

        intermediate_url = f'{proto_domain}/pass_md5/{hash}/{token}'
        # intermediate_url = f'{proto_domain}{pass_md5}'
        # print(intermediate_url)

        headers = {
            'User-Agent': 'curl',
            'referer': url
        }
        final_url = ''.join((
            self._download_webpage(intermediate_url, video_id, headers=headers),
            *(random.choice(string.ascii_letters + string.digits) for _ in range(10)),
            f'?token={token}&expiry={int(time.time() * 1000)}',
        ))

        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumb,
            'url': final_url,
            'http_headers': headers,
            'ext': 'mp4',
        }
