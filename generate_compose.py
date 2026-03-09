import toml
import yaml

with open("a2a-scenario.toml") as f:
    scenario = toml.load(f)

services = {}

# participants
for participant in scenario.get("participants", []):
    name = participant["name"]
    services[name] = {
        "image": participant["image"],
        "networks": ["agentnet"]
    }

# judge
judge_image = scenario["judge"]["image"]

participant_name = scenario["participants"][0]["name"]

services["judge"] = {
    "image": judge_image,
    "ports": ["9009:9009"],
    "depends_on": [participant_name],
    "networks": ["agentnet"]
}

compose = {
    "services": services,
    "networks": {
        "agentnet": {}
    }
}

with open("docker-compose.yml", "w") as f:
    yaml.dump(compose, f)
