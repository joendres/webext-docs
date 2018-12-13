#!/usr/bin/python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse, glob, json, os, re

DEST_DIR = os.path.dirname(__file__)
OVERLAY_DIR = os.path.join(DEST_DIR, "overlay")

current_namespace_name = None
unique_id = 1


def merge_objects(a, b):
    if isinstance(a, list):
        for c in a:
            name = c.get("namespace", c.get("name"))
            if name is None:
                b.append(c)
                continue
            for d in b:
                if d.get("namespace", d.get("name")) == name:
                    merge_objects(c, d)
    elif isinstance(a, dict):
        for [e, f] in a.iteritems():
            if e not in b:
                b[e] = f
                continue
            if e not in ["namespace", "name"]:
                merge_objects(f, b[e])
    else:
        print "Unexpected item:", a


def replace_code(string):
    string = string.replace("<em>", "*").replace("</em>", "*")
    string = string.replace("<b>", "**").replace("</b>", "**")
    string = string.replace("<code>", "``").replace("</code>", "``")
    string = string.replace("<var>", "``").replace("</var>", "``")
    return string


def get_type(obj, name):
    if "type" in obj:
        if obj.get("enum") is not None:
            return "`%s <enum_%s_%d_>`_" % (obj["type"], name, unique_id)
        elif obj["type"] == "array":
            if "items" in obj:
                return "array of %s" % get_type(obj["items"], name)
            else:
                return "array"
        else:
            return obj["type"]

    elif "$ref" in obj:
        return link_ref(obj["$ref"])


def link_ref(ref):
    if "." in ref or current_namespace_name is None:
        return ":ref:`%s`" % ref
    else:
        return ":ref:`%s.%s`" % (current_namespace_name, ref)


def format_member(name, value):
    parts = []

    if name:
        type_string = "(%s)"
        if value.get("optional", False):
            parts.append("[``%s``]" % name)
        else:
            parts.append("``%s``" % name)
    else:
        type_string = "%s"

    if "type" in value or "$ref" in value:
        parts.append(type_string % get_type(value, name))

    elif "choices" in value:
        choices = []
        for choice in value["choices"]:
            choices.append(get_type(choice, name))
        parts.append(type_string % " or ".join(choices))

    if "description" in value:
        parts.append(replace_code(value["description"]))
    
    return " ".join(parts)


def format_enum(name, value):
    if value.get("enum") is None:
        return []

    enum_lines = [
        ".. _enum_%s_%d:" % (name, unique_id),
        "",
        "Values for %s:" % name,
        "",
    ]
    for enum_value in value.get("enum"):
        enum_lines.append("- ``%s``" % enum_value)
    enum_lines.append("")
    return enum_lines


def format_object(name, obj):
    global unique_id

    if name is None:
        lines = []
    else:
        lines = ["- %s" % format_member(name, obj)]
    enum_lines = []

    if obj.get("type") == "object" and "properties" in obj:
        lines.append("")
        items = sorted(obj["properties"].items())
        for [key, value] in items:
            if not value.get("optional", False):
                lines.append("  - %s" % format_member(key, value))
                enum_lines.extend(format_enum(key, value))
                unique_id += 1

        for [key, value] in items:
            if value.get("optional", False):
                lines.append("  - %s" % format_member(key, value))
                enum_lines.extend(format_enum(key, value))
                unique_id += 1

        lines.append("")

    lines.extend(enum_lines)
    return lines


def format_params(function, callback=None):
    params = []
    for param in function["parameters"]:
        if param["name"] == callback:
            continue
        if param.get("optional", False):
            params.append("[%s]" % param["name"])
        else:
            params.append(param["name"])
    return ", ".join(params)


def format_permissions(obj):
    if "permissions" not in obj:
        return []

    lines = []
    name = obj.get("namespace", obj.get("name"))
    for permission in obj["permissions"]:
        lines.extend([
            "",
            ".. note::",
            "",
            "  The permission ``%s`` is required to use ``%s``." % (permission, name),
            "",
        ])
    return lines


def header_1(string):
    return [
        "=" * len(string),
        string,
        "=" * len(string),
        "",
    ]


def header_2(string):
    return [
        string,
        "=" * len(string),
        "",
    ]


def header_3(string):
    return [
        string,
        "-" * len(string),
        "",
    ]


def format_namespace(namespace, manifest_namespace=None):
    global current_namespace_name, unique_id

    current_namespace_name = namespace["namespace"]
    unique_id = 1
    preamble = os.path.join(OVERLAY_DIR, current_namespace_name + ".rst")
    if os.path.exists(preamble):
        with open(preamble) as fp_preamble:
            lines = map(lambda l: l.rstrip("\n").decode("utf-8"), fp_preamble.readlines())
            lines.append("")
    else:
        lines = header_1(current_namespace_name)

    if "description" in namespace:
        lines.append(replace_code(namespace["description"]))
        lines.append("")

    if manifest_namespace is not None:
        lines.extend(manifest_namespace)

    lines.extend(format_permissions(namespace))

    if "functions" in namespace:
        lines.extend(header_2("Functions"))
        for function in namespace["functions"]:
            async = function.get("async")
            lines.extend([
                ".. _%s.%s:" % (current_namespace_name, function["name"]),
                "",
            ])
            lines.extend(header_3("%s(%s)" % (function["name"], format_params(function, callback=async))))
            enum_lines = []

            if "description" in function:
                lines.append(replace_code(function["description"]))
                lines.append("")

            if len(function["parameters"]):
                for param in function["parameters"]:
                    if async == param["name"]:
                        if len(param["parameters"]) > 0:
                            function["returns"] = param["parameters"][0]
                    else:
                        lines.extend(format_object(param["name"], param))
                        enum_lines.extend(format_enum(param["name"], param))
                        unique_id += 1

                lines.append("")

            if "returns" in function:
                lines.extend([
                    "Returns a `Promise`_ fulfilled with:",
                    "",
                ])
                lines.extend(format_object("", function["returns"]))
                lines.append("")

            lines.extend(format_permissions(function))
            lines.extend(enum_lines)

        lines.extend([
            ".. _Promise: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise",
            "",
        ])

    if "events" in namespace:
        lines.append("")
        lines.extend(header_2("Events"))
        for event in namespace["events"]:
            lines.extend([
                ".. _%s.%s:" % (current_namespace_name, event["name"]),
                "",
            ])
            lines.extend(header_3("%s(%s)" % (event["name"], format_params(event))))

            if "description" in event:
                lines.append(replace_code(event["description"]))
                lines.append("")

            if len(event["parameters"]):
                for param in event["parameters"]:
                    lines.extend(format_object(param["name"], param))
                lines.append("")

            if "returns" in event:
                lines.extend([
                    "Event listeners should return:",
                    "",
                ])
                lines.extend(format_object("", event["returns"]))
                lines.append("")

            lines.extend(format_permissions(event))

    if "types" in namespace:
        lines.extend(header_2("Types"))

        for type_ in sorted(namespace["types"], key=lambda t: t["id"]):
            enum_lines = []
            lines.extend([
                ".. _%s.%s:" % (current_namespace_name, type_["id"]),
                "",
            ])
            lines.extend(header_3(type_["id"]))

            if "description" in type_:
                lines.append(replace_code(type_["description"]))
                lines.append("")

            if "type" in type_:
                lines.append("%s:" % type_["type"])
                lines.append("")

            elif "choices" in type_:
                first = True
                for choice in type_["choices"]:
                    if first:
                        first = False
                    else:
                        lines.extend(["", "OR", ""])
                    lines.append("%s: %s" % (choice["type"], choice.get("description", "")))
                    if choice["type"] == "object":
                        lines.extend(format_object(None, choice))

            if "properties" in type_:
                items = sorted(type_["properties"].items())
                for [key, value] in items:
                    if not value.get("optional", False):
                        lines.extend(format_object(key, value))
                        enum_lines.extend(format_enum(key, value))
                        unique_id += 1

                for [key, value] in items:
                    if value.get("optional", False):
                        lines.extend(format_object(key, value))
                        enum_lines.extend(format_enum(key, value))
                        unique_id += 1
                lines.append("")

            lines.extend(enum_lines)

    index = 0
    previous = ""
    while index < len(lines):
        if lines[index] == "" and previous == "":
            del lines[index]
        else:
            previous = lines[index]
            index += 1

    if lines[-1] != "":
        lines.append("")

    return "\n".join(lines).encode("utf-8")


def format_manifest_namespace(manifest):
    global current_namespace_name, unique_id
    current_namespace_name = None
    unique_id = 1

    if "types" not in manifest:
        return

    lines = []
    property_lines = []
    permission_lines = []
    for type_ in manifest["types"]:
        if type_.get("$extend", None) == "WebExtensionManifest":
            for [name, value] in type_["properties"].items():
                property_lines.extend(format_object(name, value))
        if type_.get("$extend", None) == "OptionalPermission":
            for choice in type_["choices"]:
                for value in choice["enum"]:
                    permission_lines.append("- %s" % value)
            permission_lines.append("")

    if len(property_lines) > 0:
        lines = header_2("Manifest file properties") + property_lines

    if len(permission_lines) > 0:
        lines.extend(header_2("Permissions"))
        lines.extend(permission_lines)

    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create WebExtensions documentation from schema files"
    )
    parser.add_argument("path", help="""Path to comm-central""")
    parser.add_argument("file", nargs="*",
                        help="""The name of an API to document, which corresponds
                        to a .json file in the schemas directory""")
    args = parser.parse_args()

    src_dir = os.path.join(args.path, "mail/components/extensions/schemas")

    files = []
    if len(args.file) == 0:
        # Do all files.
        for filename in glob.glob(os.path.join(src_dir, "*.json")):
            files.append(os.path.basename(filename)[:-5])
    else:
        for filename in args.file:
            if os.path.exists(os.path.join(src_dir, filename + ".json")):
                files.append(filename)

    if len(files) == 0:
        print "No files found"

    for filename in sorted(files):
        with open(os.path.join(src_dir, filename + ".json")) as fp_input:
            content = fp_input.read()
            content = re.sub(r"(^|\n)//.*", "", content)
            document = json.loads(content)

        if os.path.exists(os.path.join(OVERLAY_DIR, filename + ".json")):
            with open(os.path.join(OVERLAY_DIR, filename + ".json")) as fp_overlay:
                overlay = json.load(fp_overlay)
                merge_objects(overlay, document)

        manifest_namespace = None
        for namespace in document:
            if namespace["namespace"] == "manifest":
                manifest_namespace = format_manifest_namespace(namespace)
                continue

            with open(os.path.join(DEST_DIR, namespace["namespace"] + ".rst"), "w") as fp_output:
                fp_output.write(format_namespace(namespace, manifest_namespace=manifest_namespace))
                manifest_namespace = None

        if manifest_namespace is not None:
            namespace = {
                "namespace": filename
            }
            with open(os.path.join(DEST_DIR, namespace["namespace"] + ".rst"), "w") as fp_output:
                fp_output.write(format_namespace(namespace, manifest_namespace=manifest_namespace))
