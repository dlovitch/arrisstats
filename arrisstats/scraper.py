# -*- coding: utf-8 -*-

import requests
import bs4

class Scraper:
    def __init__(self, verbose, host):
        self.verbose = verbose
        self.host = host

    def process_table(self, table, unique_key=True):
        if unique_key:
            data = {}
            range_start = 1
        else:
            data = []
            range_start = 0
        headers = [td.text for td in table[0].findAll("td")]
        if self.verbose >= 2: print("process_table/headers: {}".format(headers))
        for tr in table[1:]:
            if tr.findAll("td"):
                row = [td.text for td in tr.findAll("td")]
                if self.verbose >= 2: print("process_table/row: {}".format(row))
                processed_row = {}
                for i in range(range_start, len(headers)):
                    processed_row[headers[i]] = row[i]
                if self.verbose >= 2: print("process_table/processed_row: {}".format(processed_row))
                if unique_key:
                    data[row[0]] = processed_row
                else:
                    data.append(processed_row)
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
        r = requests.get("http://{}/cgi-bin/status_cgi".format(self.host))
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
        return status

    def get_events(self):
        events = {}
        r = requests.get("http://{}/cgi-bin/event_cgi".format(self.host))
        if r.status_code == 200:
            souped = bs4.BeautifulSoup(r.content, "lxml")
            for table in souped.findAll("table"):
                # DOCSIS(CM) Events
                if table.findNext("tbody").findNext("tr").findNext("td").text.strip() == "DOCSIS(CM) Events":
                    events = self.process_table(table.findNext("table").findNext("tbody").findAll("tr"), unique_key=False)
        return events