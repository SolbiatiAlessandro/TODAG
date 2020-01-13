# Access a database using the URL of the database page or the inline block
from notion.client import NotionClient

PAGE_ADDRESS = "https://www.notion.so/4b9cd4b1ad0247b796d1f8f19cb2d004?v=c8aa693b5ce54db2ab792883e9dc4228"
TOKEN = "5f89078c39cc72fa9f988358d645b5b4bdcf533e78dcafff6db58cccd13497d0b79d5d5c7c5a1f8d775ee318b05d97686c86dc9e6a0a0266cc937dbb69eb418304862b81c62ff0ffc9886edcf8d9"

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
client = NotionClient(token_v2=TOKEN)

# Replace this URL with the URL of the page you want to edit
page = client.get_block(PAGE_ADDRESS)

print("The page title is:", page.title)

cv = client.get_collection_view(PAGE_ADDRESS)

for row in cv.collection.get_rows():
    print("ITEM: '{}'".format(row.name))
    if(hasattr(row, "estimated_value")):
        print(row.estimated_value)
    print("CONTENT:")
    for child in row.children:
        if(hasattr(child, "title")):
            print(child.title)
        if(hasattr(child, "type")):
            print(child.type)
        print("----")

    row.children[0].title = "This comes from TODAG 2"
