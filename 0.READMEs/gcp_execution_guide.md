# GCP Execution Guide: Full MVP Smoke Test

This guide provides the end-to-end commands to execute the complete, refactored 9-stage pipeline MVP on a fresh Google Cloud Platform VM.

---

## 1. Local Preparation: Push to GitHub

Before starting, ensure all the changes we have made are pushed to your GitHub repository.

```bash
# Run these on your local machine
git add .
git commit -m "feat: Complete 1-to-1 refactor"
git push
```

---

## 2. GCP VM Setup and Connection

Follow the steps in the original `gcp_execution_guide.md` to create, connect to, and set up the basic tools (git, python) on your VM instance.

---

## 3. Clone and Run the MVP Pipeline

Once you are connected to the VM via SSH, execute the following commands.

```bash
# Clone your repository using SSH
# Replace with your actual SSH clone URL
git clone git@github.com:your-username/master_thesis.git

# Navigate into the project directory
cd master_thesis

# Make the setup script executable
chmod +x scripts/setup_and_run.sh

# Run the entire setup and MVP pipeline execution with a single command
bash scripts/setup_and_run.sh --smoke-test
```

This single command will:

1. Create a clean Python virtual environment.
2. Install all the correct, upgraded dependencies from `requirements.txt`.
3. Install your `thesis_pipeline` code as a proper package.
4. Run the `main.py` orchestrator with the `--smoke-test` flag, which executes all 9 stages using the minimal `smoke_test_config.yaml`.

---

## 4. Package and Download Results

After the script finishes, all MVP artifacts will be in the `outputs_smoke_test/` directory.

#### 4a. Package the Results (inside the VM)

```bash
# Create a zip file of the smoke test results
zip -r mvp_results.zip outputs_smoke_test/
```

#### 4b. Download the Results (from your local machine)

Disconnect from the VM by typing `exit`. Then, run the following `gcloud` command on your local terminal.

```bash
# Disconnect from the VM
exit

# Command to download the file (replace with your instance details)
gcloud compute scp YOUR_INSTANCE_NAME:/home/YOUR_USERNAME/master_thesis/mvp_results.zip . --zone=YOUR_ZONE
```

---

## 5. Verification

You will now have a `mvp_results.zip` file on your local machine. You can inspect its contents to verify that every stage (1 through 9) ran and produced the expected (minimal) output artifacts. This will provide the final validation of our new architecture.
