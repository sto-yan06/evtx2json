import argparse
import json
import sys
import re
from datetime import datetime
import Evtx.Evtx as evtx
import xmltodict

# Regex to catch non-printable/control characters that break XML parsers
ILLEGAL_XML_CHARS = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufdd0-\ufdef\ufffe\uffff]"
)

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def sanitize_xml(xml_str):
    """Removes characters that are illegal in XML 1.0."""
    return ILLEGAL_XML_CHARS.sub('', xml_str)

def convert_evtx_to_json(evtx_path, output_path=None):
    records_count = 0
    error_count = 0
    
    try:
        with evtx.Evtx(evtx_path) as log:
            # Prepare output file if path is provided
            out_file = open(output_path, 'w', encoding='utf-8') if output_path else None
            
            # If saving to file, we'll write as a JSON list start
            if out_file:
                out_file.write("[\n")

            for record in log.records():
                try:
                    # 1. Get raw XML and sanitize encoding
                    raw_xml = record.xml()
                    clean_xml = sanitize_xml(raw_xml)
                    
                    # 2. Parse to dict
                    entry = xmltodict.parse(clean_xml)
                    
                    # 3. Output logic
                    json_str = json.dumps(entry, default=json_serial)
                    
                    if out_file:
                        # Handle comma separation for valid JSON list
                        separator = ",\n" if records_count > 0 else ""
                        out_file.write(f"{separator}    {json_str}")
                    else:
                        print(json_str)
                    
                    records_count += 1

                except Exception:
                    error_count += 1
                    continue

            # Close JSON list and file
            if out_file:
                out_file.write("\n]")
                out_file.close()
                print(f"Done! Processed: {records_count} | Skipped: {error_count}")
                print(f"File saved to: {output_path}")

    except Exception as e:
        print(f"Critical File Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Robust EVTX to JSON converter.")
    parser.add_argument("input", help="Path to .evtx file")
    parser.add_argument("-o", "--output", help="Output .json file")

    args = parser.parse_args()
    convert_evtx_to_json(args.input, args.output)

if __name__ == "__main__":
    main()