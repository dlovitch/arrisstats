import requests
import bs4
import json

hostname = '192.168.100.1'

class Cli:
    def __init__(self, hostname):
        self.debug = False
        self.hostname = hostname

    def process_stream_table(self, stream_data_table):
        stream_data = {}
        headers = [ td.text for td in stream_data_table[0].findAll("td") ]
        for tr in stream_data_table[1:]:
            data_row = [ td.text for td in tr.findAll("td")]
            data_stream = {}
            for i in range(1,len(headers)):
                data_stream[headers[i]] = data_row[i]
            if self.debug: print(data_stream)
            stream_data[data_row[0]] = data_stream
        return stream_data

    def get_status(self):
        status = {}
        r = requests.get("http://{}/cgi-bin/status_cgi".format(self.hostname))
        if r.status_code == 200:
            #print(r.content)
            souped = bs4.BeautifulSoup(r.content, 'html.parser')
            #print(souped.prettify())
            for h4 in souped.findAll("h4"):
                if h4.string.strip() == "Downstream":
                    status["downstream"] = self.process_stream_table(h4.findNext("table").findAll("tr"))
                if h4.string.strip() == "Upstream":
                    status["upstream"] = self.process_stream_table(h4.findNext("table").findAll("tr"))
            #print(json.dumps(status["downstream"]))
            #print(json.dumps(status["upstream"]))
            print(json.dumps(status))


if __name__ == "__main__":
    cli = Cli(hostname)
    cli.get_status()