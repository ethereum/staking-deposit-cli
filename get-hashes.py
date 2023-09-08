#!/usr/bin/env python3
import requests
import sys
import argparse
from typing import List
try:
    import argcomplete
except ImportError:
    argcomplete = None

MIN_VERSION = 38

def filter_versions(urls, min_version):
    # Filter cp and pp versions
    cp_versions = [int(url['python_version'].replace('cp', '')) for url in urls if 'cp' in url['python_version']]
    pp_versions = [int(url['python_version'].replace('pp', '')) for url in urls if 'pp' in url['python_version']]

    # Get the maximum versions below the min_version
    max_cp_below_min = max([ver for ver in cp_versions if ver < min_version], default=None)
    max_pp_below_min = max([ver for ver in pp_versions if ver < min_version], default=None)

    # Decide which versions to include based on the given conditions
    cp_to_include = [ver for ver in cp_versions if ver >= min_version] or [max_cp_below_min]
    pp_to_include = [ver for ver in pp_versions if ver >= min_version] or [max_pp_below_min]

    # Filter the urls based on the final cp and pp versions to include, as well as sdist, py3, and py2.py3
    filtered_urls = [url for url in urls if (
                    any('cp' + str(ver) == url['python_version'] for ver in cp_to_include) or
                    any('pp' + str(ver) == url['python_version'] for ver in pp_to_include) or
                    url['python_version'] in ['py3', 'py2.py3'] or
                    url['packagetype'] == 'sdist'
                    )]

    return filtered_urls

def get_hashes_for_package(package: str, version: str, only_binary: bool) -> List[str]:
    response = requests.get(f"https://pypi.org/pypi/{package}/{version}/json")
    data = response.json()

    if only_binary:
        urls = [url for url in data['urls'] if url['packagetype'] == 'bdist_wheel']
    else:
        urls = data['urls']

    urls = filter_versions(urls, MIN_VERSION)

    valid_hashes = [url_info["digests"]["sha256"] for url_info in urls]

    return valid_hashes


def main(requirements_file: str, only_binary: bool):
    with open(requirements_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        stripped_line = line.strip()

        # If the line is a comment or an empty line, print it as-is
        if not stripped_line or stripped_line.startswith('#'):
            print(line, end='')
            continue

        # Ignore lines that start with '--hash' after stripping
        if stripped_line.startswith("--hash"):
            continue

        # Process lines with packages and versions
        if '==' in stripped_line and not stripped_line.startswith("--hash"):
            package, version = stripped_line.split("==")
            version = version.strip("\\").strip()  # Remove any continuation characters and spaces
            hashes = get_hashes_for_package(package, version, only_binary)
            print(f"{package}=={version} \\")
            for i, h in enumerate(hashes):
                ending = " \\" if i < len(hashes) - 1 else ""
                print(f"    --hash=sha256:{h}{ending}")
        else:
            # For any other kind of line, print it as-is
            print(line, end='')

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fully hashed requirements.txt")
    parser.add_argument("requirements_file", type=str, nargs='?', default="requirements.txt",
                        help="Path to the requirements file. Defaults to 'requirements.txt'.")
    parser.add_argument("--only-binary", action="store_true",
                        help="Fetch hashes only for binary distributions.")
    
    # Use argcomplete to autocomplete arguments only if it's imported
    if argcomplete:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()
    main(args.requirements_file, args.only_binary)
