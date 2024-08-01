from schema import Schema, SchemaError, Optional, Regex, Or
import yaml

# Need two schemas - one for the full schema, another for partial schema
# In the partial schema validation, all elements optional?
oucb_schema_ = {
    "version": int,
    "module": {
        "code": Regex(r"[A-M]{1,5}\d{3}$"),
        "presentation": Regex(r"^\d{2}[A-M]$"),
    },
    "image": {"base": str, "user": str},
    "packs": {
        Optional("jupyterlab"): dict,
        Optional("notebook"): dict,
        Optional("ipykernel"): dict,
        Optional("irkernel"): dict,
        Optional("code_server"): dict,
        Optional("xfce4"): dict,
    },
    Optional("sources"): {
        Optional("apt"): [
            {
                "name": str,
                "key_url": str,
                "dearmor": bool,
                "deb": {"url": str, "distribution": str, "component": str},
            }
        ]
    },
    Optional("server"): {"access_token": str, "default_path": str},
    Optional("packages"): {
        Optional("apt"): {Optional("build"): list, Optional("deploy"): list},
        Optional("pip"): {Optional("system"): list, Optional("user"): list},
    },
    Optional("content"): [
        {"source": str, "target": str, "overwrite": Or("always", "never")}
    ],
    Optional("environment"): [{"name": str, "value": str}],
    Optional("scripts"): [{"stage": Or("build", "deploy"), "commands": str}],
    Optional("output_blocks"): {
        Optional("build"): [{"block": str, "weight": int}],
        Optional("deploy"): [{"block": str, "weight": int}],
    },
    Optional("web_apps"): [
        {
            "path": str,
            "options": {"command": list, "timeout": Or(str, int)},
            Optional("launcher"): {
                Optional("title"): str,
                Optional("icon_path"): str,
                Optional("enabled"): bool,
            },
        }
    ],
    Optional("services"): list,
}

oucb_schema = Schema(oucb_schema_)

"""
# Example usage:

full_test_yaml = "version: 3"

configuration = yaml.safe_load(full_test_yaml)

try:
    oucb_schema.validate(configuration)
    print("Configuration is valid.")
except SchemaError as se:
    # raise se
    print(se)
"""

