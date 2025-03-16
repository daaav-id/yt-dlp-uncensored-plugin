# https://github.com/Mastaaa1987/vxparser/blob/main/vxparser/helper/resolveurl/plugins/vidguard.py

from yt_dlp.extractor.common import InfoExtractor

import base64
import binascii
import json
import re


class VidGuardIE(InfoExtractor):
    _VALID_URL = r'https?://((?:vid-?guard|vgfplay|fslinks|moflix-stream|listeamed|go-streamer|gsfjzmqu|v?[g6b]?embedv?)\.(?:to|com|day|xyz|org|net|sbs))/(?:e|v|d)/(?P<id>[0-9a-zA-Z]+)'
    _TESTS = []

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        #print(webpage)

        r = re.search(r'eval\("window\.ADBLOCKER\s*=\s*false;\\n(.+?);"\);</script', webpage)
        #print(r)
        if r:
            r = r.group(1).replace('\\u002b', '+')
            r = r.replace('\\u0027', "'")
            r = r.replace('\\u0022', '"')
            r = r.replace('\\/', '/')
            r = r.replace('\\\\', '\\')
            r = r.replace('\\"', '"')
            aa_decoded = decode(r, alt=True)
            #print(aa_decoded)
            stream_url = json.loads(aa_decoded[11:]).get('stream')
            #print(stream_url)
            hls = sig_decode(stream_url)
            #print(hls)
            formats = self._extract_m3u8_formats(hls, video_id, ext="mp4", entry_protocol='m3u8_native', m3u8_id="hls")

        return {
            #'type': 'url_transparent',
            'type': 'video',
            'id': video_id,
            'title': self._generic_title(url) or video_id,
            'formats': formats,
        }


def decode(text, alt=False):
    text = re.sub(r"\s+|/\*.*?\*/", "", str(text))
    if alt:
        data = text.split("+(ﾟɆﾟ)[ﾟoﾟ]")[1]
        chars = data.split("+(ﾟɆﾟ)[ﾟεﾟ]+")[1:]
        char1 = "ღ"
        char2 = "(ﾟɆﾟ)[ﾟΘﾟ]"
    else:
        data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
        chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]
        char1 = "c"
        char2 = "(ﾟДﾟ)['0']"

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)", "u") \
            .replace(char1, "0") \
            .replace(char2, "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = ""
        subchar = ""
        for v in char:
            c += v
            try:
                x = c
                subchar += str(eval(x))
                c = ""
            except:
                pass
        if subchar != '':
            txt += subchar + "|"
    txt = txt[:-1].replace('+', '')

    txt_result = "".join([chr(int(n, 8)) for n in txt.split('|')])

    return toStringCases(txt_result)


def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in txt_result:
            m3 = True
            try:
                sum_base = "+" + re.search(r".toString...(\d+).", txt_result, re.DOTALL).groups(1)
            except:
                sum_base = ""
            txt_pre_temp = re.findall(r"..(\d),(\d+).", txt_result, re.DOTALL)
            txt_temp = [(n, b) for b, n in txt_pre_temp]
        else:
            txt_temp = re.findall(r'(\d+)\.0.\w+.([^\)]+).', txt_result, re.DOTALL)
        for numero, base in txt_temp:
            code = toString(int(numero), eval(base + sum_base))
            if m3:
                txt_result = re.sub(r'"|\+', '', txt_result.replace("(" + base + "," + numero + ")", code))
            else:
                txt_result = re.sub(r"'|\+", '', txt_result.replace(numero + ".0.toString(" + base + ")", code))
    return txt_result


def toString(number, base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number // base, base) + string[number % base]


def sig_decode(url):
    """Decode the signature-protected URL."""
    sig = url.split('sig=')[1].split('&')[0]
    decoded_sig = ''.join(
        chr((v if isinstance(v, int) else ord(str(v))) ^ 2)
        for v in binascii.unhexlify(sig)
    )
    t = list(base64.b64decode(decoded_sig + '==')[:-5][::-1])

    for i in range(0, len(t) - 1, 2):
        t[i + 1], t[i] = t[i], t[i + 1]
    return url.replace(sig, ''.join(chr(c) for c in t)[:-5])
