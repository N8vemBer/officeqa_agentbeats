import os
import tomllib
import yaml


def load_scenario():
    # Support both filenames just in case
    if os.path.exists("scenario.toml"):
        path = "scenario.toml"
    else:
        path = "a2a-scenario.toml"

    with open(path, "rb") as f:
        return tomllib.load(f)


def resolve_env(env_dict):
    resolved = {}
    for key, value in env_dict.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            resolved[key] = os.environ.get(env_var, "")
        else:
            resolved[key] = value
    return resolved


def generate_compose(scenario):
    services = {}

    # Green agent / judge
    green = scenario.get("green_agent", {})
    green_image = green.get("image", "ghcr.io/arnavsinghvi11/officeqa-judge:latest")
    green_env = resolve_env(green.get("env", {}))

    participants = scenario.get("participants", [])

    participant_names = []
    for i, participant in enumerate(participants):
        p_name = participant.get("name") or participant.get("role") or f"participant_{i}"
        p_image = participant.get("image", "ghcr.io/n8vember/officeqa-purple:latest")
        p_env = resolve_env(participant.get("env", {}))

        services[p_name] = {
            "image": p_image,
            "ports": [f"{9019 + i}:9009"],
            "environment": p_env,
            "networks": ["agentnet"],
        }
        participant_names.append(p_name)

    services["judge"] = {
        "image": green_image,
        "ports": ["9009:9009"],
        "environment": green_env,
        "networks": ["agentnet"],
        "depends_on": participant_names,
    }

    compose = {
        "version": "3.8",
        "services": services,
        "networks": {
            "agentnet": {"driver": "bridge"}
        },
    }

    with open("docker-compose.yml", "w") as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)

    print("Generated docker-compose.yml")


if __name__ == "__main__":
    scenario = load_scenario()
    generate_compose(scenario)
