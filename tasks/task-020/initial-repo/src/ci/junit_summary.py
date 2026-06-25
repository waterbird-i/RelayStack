import xml.etree.ElementTree as ET


def summarize(xml_text):
    root = ET.fromstring(xml_text)
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        return {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    return {
        "tests": int(suite.attrib.get("tests", 0)),
        "failures": int(suite.attrib.get("failures", 0)),
        "errors": int(suite.attrib.get("errors", 0)),
        "skipped": int(suite.attrib.get("skipped", 0)),
    }
