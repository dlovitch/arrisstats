import requests
import bs4
import json

hostname = '192.168.100.1'

class Cli:
    def __init__(self, hostname):
        self.debug = False
        self.verbose = 0
        self.hostname = hostname

    def process_table(self, table):
        data = {}
        headers = [td.text for td in table[0].findAll("td")]
        for tr in table[1:]:
            if tr.findAll("td"):
                row = [td.text for td in tr.findAll("td")]
                processed_row = {}
                for i in range(1, len(headers)):
                    processed_row[headers[i]] = row[i]
                if self.debug: print(processed_row)
                data[row[0]] = processed_row
        return data

    def process_kv_table(self, table):
        data = {}
        #print(table)
        for tr in table:
            if tr.findAll("td"):
                data[tr.findNext("td").text.strip()[:-1]] = tr.findNext("td").findNext("td").text.strip()
        return data

    def get_status(self):
        status = {}
        r = requests.get("http://{}/cgi-bin/status_cgi".format(self.hostname))
        if r.status_code == 200:
            if self.verbose > 2: print(r.content)
            # Using lxml parser instead of html.parser because of
            #   extraneous <tr> opening or closing tags
            souped = bs4.BeautifulSoup(r.content, "lxml")
            if self.verbose > 2: print(souped.prettify())

            # RF Parameters
            for h4 in souped.findAll("h4"):
                if h4.string.strip() == "Downstream":
                    status["Downstream"] = self.process_table(h4.findNext("table").findAll("tr"))
                if h4.string.strip() == "Upstream":
                    status["Upstream"] = self.process_table(h4.findNext("table").findAll("tr"))

            for table in souped.findAll("table"):
                # Status
                if table.findNext("tbody").findNext("tr").findNext("td").text.strip() == "Status":
                    status["Status"] = self.process_kv_table(table.findNext("table").findNext("tbody").findAll("tr"))

                # Interface Parameters
                if table.findNext("tbody").findNext("tr").findNext("td").text.strip() == "Interface Parameters":
                    status["Interface Parameters"] = self.process_table(table.findNext("table").findNext("tbody").findAll("tr"))
            print(json.dumps(status, sort_keys=True, indent=4))
if __name__ == "__main__":
    cli = Cli(hostname)
    cli.get_status()
