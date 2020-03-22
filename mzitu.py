import requests, re


class Mzitu_spider:
    def __init__(self, url, num=1):
        self.url = url
        self.url_list = []
        self.mzitu_list = []
        self.num = num


    def get_url(self):
        for i in range(self.num):
            params = 'page/' + str(i+1)
            self.url_list.append(self.url + params)


    def save_url(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
            }
        p1 = r'<li>(.+)</a><span>'
        p2 = r'<a href="(.+)"'
        p3 = r"alt='(.+)'"
        for url in self.url_list:
            html = requests.get(url, headers=headers).text
            for text in re.findall(p1, html):
                addr = re.search(p2, text).group().split('"')[1]
                title = re.search(p3, text).group().split('\'')[1]
                if [addr, title] not in self.mzitu_list:
                    self.mzitu_list.append([addr, title])


    def save_img(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
            }
        p1 = r"<a href=(.+?)</span></a>"
        p2 = r'<img src="(.+?)"'
        for url in self.mzitu_list:
            html = requests.get(url[0], headers=headers).text
            page = int(re.findall(p1, html)[-2].split('>')[-1])
            img_url = re.search(p2, html).group().split('"')[-2][:-6]
            print(url[1], '[共{}张]'.format(page), '({}/{})'.format(self.mzitu_list.index(url)+1, len(self.mzitu_list)))
            for i in range(page):
                if i < 9:
                    i = '0' + str(i+1)
                else:
                    i = str(i+1)
                img = img_url + i + '.jpg'
                try:
                    with open(url[1]+i+'.jpg', 'rb') as f:
                        pass
                except FileNotFoundError:
                    with open(url[1]+i+'.jpg', 'wb') as f:
                        f.write(requests.get(img, headers=headers).content)


    def run(self):
        self.get_url()
        self.save_url()
        self.save_img()


if __name__ == '__main__':
    url = 'https://mzitu.com/'
    num = input('请问需要几页？:')
    mzitu = Mzitu_spider(url, int(num))
    mzitu.run()
