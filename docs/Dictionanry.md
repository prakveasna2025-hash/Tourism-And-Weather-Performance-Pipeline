# What does mount mean!
In the context of software development, Docker, and data pipelines (like your project setup on Day 5 shown in your roadmap), mounting (or a volume mount) means linking a folder or file from your physical computer (the host machine) directly into a running Docker container.

How It Works
Normally, everything inside a Docker container is isolated—it lives inside its own virtual file system. If you write code on your computer, the container cannot see it by default.

When you mount a folder (like your dags/ or include/ folders):

You create a bridge between your local Windows machine and the Linux container.

Any changes you save on your local machine instantly appear inside the container without needing to rebuild or restart the whole Docker image.

Why It Matters for Airflow (Day 5)
In your project roadmap, mounting the dags/ folder means Airflow can automatically read and execute the Python DAG files you write in your local code editor (like Visual Studio Code) without you having to manually copy-paste them into the container every time.



