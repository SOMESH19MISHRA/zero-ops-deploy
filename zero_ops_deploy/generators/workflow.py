def generate_workflow(docker_username, image_name):
    return f"""name: Docker Build and Push

on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Login
        uses: docker/login-action@v4
        with:
          username: ${{{{ secrets.DOCKER_USERNAME }}}}
          password: ${{{{ secrets.DOCKER_TOKEN }}}}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: {docker_username}/{image_name}:latest
"""
