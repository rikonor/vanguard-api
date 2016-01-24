from browser import Browser
import config

from base import Base
from browser import Converters

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

        return question

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

    def get_total_assets(self):
        self.go_to_balances_and_holdings()

        total_holder = self.browser.find_element_by_class("vgContainer").text

        end_of_num = total_holder.index(" ")
        # assume first char is $
        total = float(total_holder[1:end_of_num].replace(",", ""))

        return total

    def get_current_holdings(self):
        self.go_to_balances_and_holdings()

        holdings_table = self.browser.find_element_by_id("BHForm2:accountID:0:_id245")
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

            # Symbol
            holding_info["symbol"] = els[0].text

            # Name (needs to be trimmed of spaces)
            name = els[1].text
            holding_info["name"] = name.strip()

            # Expense Ratio (Convert to float ratio)
            holding_info["expense_ratio"] = Converters.percent(els[2].text)

            # Quantity (Convert to doller value)
            holding_info["quantity"] = Converters.dollar_amount(els[3].text)

            # Last Price (Convert to doller value)
            holding_info["last_price"] = Converters.dollar_amount(els[4].text)

            # Absolute Change Amount (Convert to doller value)
            holding_info["change_amount"] = Converters.dollar_amount(els[5].text)

            # Precentage Change (Convert to float ratio)
            holding_info["change_percent"] = Converters.percent(els[6].text)

            # Current Balance for this holding (Convert to dollar value)
            holding_info["current_balance"] = Converters.dollar_amount(els[7].text)

            holdings_info.append(holding_info)

        return holdings_info
