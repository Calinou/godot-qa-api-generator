#!/usr/bin/env python3

import asyncio
import json
import os

import aiohttp
from bs4 import BeautifulSoup
from typing_extensions import Final

GODOT_QA_URL: Final = "https://godotengine.org/qa"


# Example of expected JSON output:
# {
#     "data": {
#         "questions": {
#             "title": "Hello world",
#             "author": "Someone",
#             "date_posted": "2020-12-30T13:00:00Z",
#             "category": "Engine",
#             "score": 4
#         }
#     }
# }


async def main() -> None:
    # Change to the directory where the script is located,
    # so that the script can be run from any location.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    with open("tags.conf") as tags_file:
        print("Generating JSON for Q&A tags from `tags.conf`...")
        for tag_unstripped in tags_file:
            # A newline is included at the end of the tag, strip it.
            tag = tag_unstripped.strip()
            if tag == "" or tag.startswith("#"):
                continue

            async with aiohttp.ClientSession() as session:
                print(f'Fetching HTML page for "{tag}"...')
                async with session.get(f"{GODOT_QA_URL}/search?q={tag}") as response:
                    print(f'Parsing HTML for "{tag}"...')
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    # print(soup.get_text())
                    output_path = f"output/{tag}.json"
                    with open(output_path, "w") as output_file:
                        output_file.write(json.dumps({"hello": 123}))
                        # End the file with a blank line just in case.
                        output_file.write("\n")
                        print(f'Successfully generated JSON for "{tag}": {output_path}')

    print("Finished generating all JSON files.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
