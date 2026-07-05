def generate_dockerfile(stack):
    if stack == "flask":
        return """FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
"""

    elif stack == "express":
        return """FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm","start"]
"""

    elif stack == "python-script":
        return """FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","app.py"]
"""

    elif stack == "static":
        return """FROM nginx:alpine
COPY . /usr/share/nginx/html
"""
