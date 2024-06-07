import os
import yaml

metadata_path = "metadata/databases/listsync.io/tables"
session_variable = "X-Hasura-Tenant-Id"


def update_permissions(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    if "permissions" not in data:
        data["permissions"] = {}

    roles = ["select", "insert", "update", "delete"]

    for role in roles:
        if role not in data["permissions"]:
            data["permissions"][role] = {}
        if "filter" not in data["permissions"][role]:
            data["permissions"][role]["filter"] = {}
        if "check" not in data["permissions"][role]:
            data["permissions"][role]["check"] = {}
        if "set" not in data["permissions"][role]:
            data["permissions"][role]["set"] = {}

        data["permissions"][role]["filter"]["tenant_id"] = {"_eq": session_variable}
        data["permissions"][role]["check"]["tenant_id"] = {"_eq": session_variable}
        data["permissions"][role]["set"]["tenant_id"] = session_variable

    with open(file_path, "w") as file:
        yaml.safe_dump(data, file, default_flow_style=False)


def main():
    for root, dirs, files in os.walk(metadata_path):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = yaml.safe_load(f)
                    if "columns" in content:
                        import pdb

                        pdb.set_trace()
                        columns = [column["name"] for column in content["columns"]]
                        if "tenant_id" in columns:
                            update_permissions(file_path)
                            print(f"Updated permissions for {file_path}")


if __name__ == "__main__":
    main()
