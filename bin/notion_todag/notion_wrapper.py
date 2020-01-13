# Access a database using the URL of the database page or the inline block
from notion.client import NotionClient
import logging

PAGE_ADDRESS = "https://www.notion.so/4b9cd4b1ad0247b796d1f8f19cb2d004?v=c8aa693b5ce54db2ab792883e9dc4228"
TOKEN = "5f89078c39cc72fa9f988358d645b5b4bdcf533e78dcafff6db58cccd13497d0b79d5d5c7c5a1f8d775ee318b05d97686c86dc9e6a0a0266cc937dbb69eb418304862b81c62ff0ffc9886edcf8d9"

class NotionBlock():
    def __init__(self, notionURL):
        """
        notionURL is a string like
        https://www.notion.so/4b9cd4b1ad0247b796d1f8f19cb2d004?v=c8aa693b5ce54db2ab792883e9dc4228&p=33e512b6c51349f4aecd688e993f85e7
        """
        # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
        client = NotionClient(token_v2=TOKEN)
        self.page = client.get_block(notionURL)
        logging.warning(
               "Reading Notion page with title: "+self.page.title if hasattr(self.page, "title") else\
                       "No title found for page with url: "+notionURL
                       )

    def get_TODAG_field(self):
        """
        TODAG field is the first children of a page, page should always
        have the first children (should build a template later)
        """
        if not self.page.children:
            logging.warning("Notion APIs failure: Page has no children, quitting")
            return None
        if self.page.children[0].type != "text":
            logging.warning("Notion APIs failure: TODAG field on notion is not text")
            return None
        return self.page.children[0].title

    def set_TODAG_field(self, text):
        """
        TODAG field is the first children of a page, page should always
        have the first children (should build a template later)
        """
        if not self.page.children:
            logging.warning("Notion APIs failure: Page has no children, quitting")
            return None
        if self.page.children[0].type != "text":
            logging.warning("Notion APIs failure: TODAG field on notion is not text")
            return None
        self.page.children[0].title = text
