# Evaluating Energy-Reduction Techniques in RAG Systems: A Controlled Experiment

This project presents a controlled experiment assessing the effectiveness of various techniques for reducing energy consumption in Retrieval-Augmented Generation (RAG) systems. The study provides empirical evidence on how these optimizations impact energy usage while maintaining system performance.

## Experiment Overview

[Brief description of experiment design, techniques being tested, and evaluation metrics]

## Running the Experiment

### Prerequisites
- Kubernetes (via `kind`)
- Helm
- Docker
- AWS ECR access permissions

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone git@github.com:KafkaOtto/thesis_intern.git
   ```
2. **Create Kubernetes cluster:**
```bash
kind create cluster pp
```
3. **Import the Dataset into Docker**

Since kind relies on Docker, you'll need to mount the dataset into a Docker container:
```bash
docker run -v /path/on/host:/mnt/data my-image
```
Expected directory structure inside the container:
```bash
root@pp-control-plane:/# ls /mnt/data/
crag_task_1_and_2_dev_v4.jsonl	output	reference_uris.json
6:00
root@pp-control-plane:/# ls /mnt/data/output/ | head
00089066-b0f2-43aa-88a4-08c74fbfbe05_0.md
00089066-b0f2-43aa-88a4-08c74fbfbe05_1.md
```
4. **Configure Access to AWS ECR (if applicable)**

If you are pulling Docker images from AWS ECR, ensure that you have the proper credentials and access rights.
5. **Export Required Environment Variables**

Before running the experiment, export the following environment variables:
```bash
export BASE_DIR=/path/to/your/repository
export ECR_REGISTRY=<your-ecr-registry>
export DOCKER_EMAIL=<your-docker-email>
```
6. **Initialize and Run the Experiment**

Run the setup scripts:
```bash
bash db_init.sh
bash install.sh
```
To run the experiment in the background, use nohup.
