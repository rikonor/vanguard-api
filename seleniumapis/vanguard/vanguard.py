#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import Browser
import config

from base import Base
from browser import Converters
from browser.converters import TextType

class Vanguard(Base):
    def ensure_logged_in(self):
        if self.logged_in is not True:
            raise RuntimeError("You are not logged in")

    def go_to_login(self):
        self.browser.get(config.LOGIN_PATH)

    def login(self, user, password):
        if self.logged_in is True:
            print "Already logged in"
            return

        self.go_to_login()

        form_id = "LoginForm"
        user_input_id = "USER"
        password_input_id = "PASSWORD"
        submit_id = "login"

        form_info = dict()
        form_info[user_input_id] = user
        form_info[password_input_id] = password

        self.browser.fill_form(form_id, form_info)

        self.logged_in = True

    def get_security_question(self):
        """
        Check whether we are currently being asked a security question
        And if so return it
        """
        # Check if there is a securit question present
        if not self.browser.contains_text("Answer your security question"):
            return None

        # get the summary table
        table = self.browser.find_element_by_id("LoginForm:summaryTable")

        # Get the question text
        question = table.find_elements_by_tag_name("td")[3].text

        return question.replace("'","")

    def answer_security_question(self, answer):
        # get the summary table
        table = self.browser.find_element_by_id("LoginForm:summaryTable")

        # get the answer input
        inputs = table.find_elements_by_tag_name("input")
        inputs[0].send_keys(answer)

        # Set the client as a public computer
        inputs[2].click()

        # Click the continue button
        inputs[4].click()

    def go_to_home(self):
        self.ensure_logged_in()
        self.browser.get(config.HOME_PATH)

    def go_to_balances_and_holdings(self):
        self.ensure_logged_in()
        self.browser.get(config.BALANCES_AND_HOLDINGS_PATH)

    def go_to_cost_basis(self):
        self.ensure_logged_in()
        self.browser.get(config.COST_BASIS_PATH)

    def get_total_assets(self):
        self.go_to_balances_and_holdings()

        total_holder = self.browser.find_element_by_class("vgContainer").text

        end_of_num = total_holder.index(" ")
        # assume first char is $
        total = float(total_holder[1:end_of_num].replace(",", ""))

        return total

    def get_current_holdings(self):
        self.go_to_balances_and_holdings()

        holdings_tables = self.browser.find_elements_by_xpath("//table[starts-with(@id,'BHForm2:accountID:')]")
        accounts = {}
        account_num = 0

        data_headers = []
        data_headers.append( ("symbol",TextType.plain) )
        data_headers.append( ("name",TextType.plain) )
        data_headers.append( ("expense_ratio",TextType.percent) )
        data_headers.append( ("quantity",TextType.plain) )
        data_headers.append( ("last_price",TextType.dollar) )
        data_headers.append( ("change_amount",TextType.dollar) )
        data_headers.append( ("change_percent",TextType.percent) )
        data_headers.append( ("current_balance",TextType.dollar) )

        for holdings_table in holdings_tables:
            if  len( holdings_table.find_elements_by_tag_name("th") ) == 0:
                continue

            rows = holdings_table.find_elements_by_tag_name("tr")

            # First row is Tables Headers
            # Second row simply says "ETFs"
            rows = rows[2:]

            # Row before last simply says "Buy Sell"
            # Last row is Total Assets
            rows = rows[:-2]

            # Remaining rows are actual ETFs
            holdings_info = []
            for row in rows:
                holding_info = {}
                els = row.find_elements_by_tag_name("td")
                if len(els) < 8:
                    continue

                for el_num in xrange( len(els) ):
                    if el_num >= len( data_headers ):
                        continue
                    headerName,textType = data_headers[el_num]
                    holding_info[ headerName ] = Converters.convert( els[el_num].text , textType )

                holdings_info.append(holding_info)
            account_num += 1
            accounts["Account %s" % account_num] = holdings_info
        return accounts

    def get_cost_basis(self, instrument):
        self.go_to_cost_basis()

        holding_table_xpath = "//table[starts-with(@id,'unrealizedTabForm')]"

        # We need to wait since the information is loaded after pageload
        self.browser.wait_until_visible(holding_table_xpath)
        holding_table = self.browser.find_elements_by_xpath(holding_table_xpath)[0]

        rows = holding_table.find_elements_by_tag_name("tr")
        instrument_id = None

        for row in rows:
            tds = row.find_elements_by_tag_name("td")

            # This is a header
            if len(tds) == 9:
                if  instrument == tds[0].text:
                    a = tds[8].find_elements_by_xpath(".//span[contains(@class, 'noPipe firstLink')]/a")
                    url = a[0].get_attribute('href')
                    instrument_id = url.split('HldId=')[1]

            elif instrument_id and "Show details" in row.text:
                row.click()
                break

        lots_table_xpath = "//table[contains(@id, '%s')]" % instrument_id
        self.browser.wait_until_visible(lots_table_xpath)
        lots_table = self.browser.find_elements_by_xpath(lots_table_xpath)[0]
        lots_rows = lots_table.find_elements_by_tag_name("tr")
        lots_info = []

        data_headers = []
        data_headers.append( ("date", TextType.plain) )
        data_headers.append( ("quantity",TextType.plain) )
        data_headers.append( ("cost_per_share",TextType.dollar) )
        data_headers.append( ("total_cost",TextType.dollar) )
        data_headers.append( ("market_value",TextType.dollar) )
        data_headers.append( ("short_term",TextType.dollar) )
        data_headers.append( ("long_term",TextType.dollar) )
        data_headers.append( ("total_gain_lost",TextType.dollar) )

        for row in lots_rows:
            tds = row.find_elements_by_tag_name("td")
            if len(tds) == 8:
                lot = {}
                for index in xrange(len(tds)):
                    headerName,textType = data_headers[index]
                    lot[headerName] = Converters.convert(tds[index].text, textType)

                lots_info.append(lot)

        return lots_info


    def _cleanText(self, text):
        #Removed nonprintable characters as well as newlines/tabs
        new_text = ""
        for char in text:
            if ord(char) < 32 or ord(char) > 126:
                new_text += " "
            else:
                new_text += char
        return new_text
