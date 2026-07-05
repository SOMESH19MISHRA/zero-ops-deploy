import click
import os
from zero_ops_deploy.detector import detect_stack
from zero_ops_deploy.generators.dockerfile import generate_dockerfile
from zero_ops_deploy.generators.workflow import generate_workflow
from zero_ops_deploy.generators.deploy_script import generate_deploy_script

@click.command()
@click.option('--path', default='.')
@click.option('--docker-username', required=True)
@click.option('--image-name', required=True)
def init(path, docker_username, image_name):
    detected_stack = detect_stack(path)

    if detected_stack == "unknown":
        print("Not a supported stack. Kindly use a stack that is available in the tool's list")
        return

    dockerfile = generate_dockerfile(detected_stack)
    workflow = generate_workflow(docker_username, image_name)
    deploy_script = generate_deploy_script(docker_username, image_name, 5000)

    # write Dockerfile
    with open(os.path.join(path, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    # write workflow YAML — needs its own folder
    os.makedirs(os.path.join(path, ".github", "workflows"), exist_ok=True)
    with open(os.path.join(path, ".github", "workflows", "docker-build-push.yml"), "w") as f:
        f.write(workflow)

    # write deploy script
    with open(os.path.join(path, "deploy.sh"), "w") as f:
        f.write(deploy_script)

    print(f"Detected stack: {detected_stack}")
    print("Generated: Dockerfile, .github/workflows/docker-build-push.yml, deploy.sh")

if __name__ == "__main__":
    init()
