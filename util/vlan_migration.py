# Used to migrate old VLANs from the old YAML format to the new format.

# read 3 yaml files into individual dicts
import yaml


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


mocVLANs = read_yaml_file("moc/vlans.yaml")
nercVLANs = read_yaml_file("nerc/vlans.yaml")
octVLANs = read_yaml_file("oct/vlans.yaml")

mocVLANs = mocVLANs["vlans"]
nercVLANs = nercVLANs["vlans"]
octVLANs = octVLANs["vlans"]

# combine the dicts into a single dict, throw out duplicates in a single line
vlans = {**mocVLANs, **nercVLANs, **octVLANs}

# sort vlans by id
vlans = dict(sorted(vlans.items(), key=lambda item: item[0]))

newVLANs = []

# Loop through each vlan
for vlan in vlans:
    # make a yaml like
    # - id: 84
    # name: "UMA-84"
    # description: "UMass VLAN 84 Public IPs for CloudLab"
    # fabrics:
    #  - "oct"

    # for each
    newObj = {
        "id": vlan,
        "name": vlans[vlan]["name"],
        "description": vlans[vlan]["description"],
        "fabrics": [],
    }

    # if the fabric is oct, add it to the fabrics list
    if vlan in octVLANs:
        newObj["fabrics"].append("oct")
    # if the fabric is nerc, add it to the fabrics list
    if vlan in nercVLANs:
        newObj["fabrics"].append("nerc")
    # if the fabric is moc, add it to the fabrics list
    if vlan in mocVLANs:
        newObj["fabrics"].append("moc")
    # set managed if set
    if "managed" in vlans[vlan]:
        newObj["managed"] = vlans[vlan]["managed"]

    # add as object to newVLANs
    newVLANs.append(newObj)

# output to yaml
with open("outvlans.yaml", "w") as file:
    yaml.dump({"vlans": newVLANs}, file, default_flow_style=False, sort_keys=False)
