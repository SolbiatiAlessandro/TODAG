from  notion_wrapper import NotionBlock
import logging

def test_set_get():
    block = NotionBlock("https://www.notion.so/4b9cd4b1ad0247b796d1f8f19cb2d004?v=c8aa693b5ce54db2ab792883e9dc4228&p=33e512b6c51349f4aecd688e993f85e7")
    old_field = block.get_TODAG_field()
    assert old_field
    assert type(old_field) == str
    logging.info(old_field)

    block.set_TODAG_field("come from TODAG 3")
