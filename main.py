#!/usr/bin/env python3

import asyncio
import json
import os
from typing import Any, Dict, List

import aiohttp
from bs4 import BeautifulSoup
from typing_extensions import Final

GODOT_QA_URL: Final = "https://godotengine.org/qa"


# Example of expected JSON output:
# {
#     "data": {
#         "questions": [
#             {
#                 "title": "Hello world",
#                 "author": "Someone",
#                 "date_posted": "Nov 19, 2020",
#                 "category": "Engine",
#                 "answers": 2,
#                 "score": -1
#             }
#         ]
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
                    questions: List[Dict[str, Any]] = []

                    for question in soup.select(".qa-q-list .qa-q-list-item"):
                        questions.append(
                            {
                                "title": question.select(".qa-q-item-title")[0]
                                .get_text()
                                .strip(),
                                "author": question.select(".qa-user-link")[0]
                                .get_text()
                                .strip(),
                                "date_posted": question.select(".qa-q-item-when-data")[
                                    0
                                ]
                                .get_text()
                                .strip(),
                                "category": question.select(".qa-category-link")[0]
                                .get_text()
                                .strip(),
                                "answers": int(
                                    question.select(".qa-a-count-data")[0]
                                    .get_text()
                                    .strip()
                                ),
                                "score": int(
                                    question.select(".qa-netvote-count-data")[0]
                                    .get_text()
                                    .replace(
                                        "–", "-"
                                    )  # Use ASCII minus symbol so the number can be parsed as an integer.
                                    .strip()
                                ),
                            }
                        )

                    output_path = f"output/{tag}.json"
                    with open(output_path, "w") as output_file:
                        output_file.write(
                            json.dumps(
                                {
                                    "data": {
                                        "questions": questions,
                                    },
                                }
                            )
                        )
                        print(f'Successfully generated JSON for "{tag}": {output_path}')

    print("Finished generating all JSON files.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
