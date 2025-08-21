# 🧑‍💻 Rootconf 2025 Workshop: **Detecting Supply Chain Attacks at Runtime with eBPF**

Welcome! In this workshop, you’ll learn how to detect **supply chain attacks** at runtime using **eBPF** — tracing behaviors like secret access, outbound exfiltration, and suspicious process execution.

No kernel or eBPF experience needed. Everything runs in **GitHub Actions (`ubuntu-latest`)**.

---

## ✅ What You'll Do

* Detect sensitive file access (`.env`, `.aws`, `.pem`)
* Trace outbound network connections
* Catch binaries executed from `/tmp` (backdoor style)
* Simulate a real exfiltration attack
* Run detections inside a CI pipeline
* Extend workflows to add custom detections & alerts

---

## 🗂 Repo Structure

```
rootconf25-training-lab/
├── .github/workflows/hello-world.yml  # Main GitHub Actions workflow
├── connect_tracer.py                  # Outbound connections tracer
├── execve_tracer.py                   # Suspicious binary execution tracer
├── openat_tracer.py                   # File access tracer
├── simulate_exfil.sh                  # Simulates secret exfiltration
├── troubleshoot.md                    # Common issues & solutions
```

---

## 📝 Prerequisites

* GitHub account
* Fork this repository

That’s it. Everything else runs inside GitHub Actions.

---

## 🏁 Step 1: Fork & Trigger Workflow

1. Fork this repo into your GitHub account
2. Go to **Actions** tab → enable workflows
3. Trigger with a dummy commit:

   ```bash
   git commit --allow-empty -m "Trigger workflow"
   git push
   ```

You’ll see the workflow run in **Actions**.

---

## 🔍 Step 2: Detect Sensitive File Access

The workflow runs `openat_tracer.py`, which monitors access to `.env`, `.aws`, and `.pem` files.

When the workflow creates and reads a `.env` file, you’ll see log entries in **Actions output**.

🎯 **Goal:** Understand syscall tracing and how attackers leak secrets.

---

## 🌐 Step 3: Detect Outbound Connections

Next, the workflow runs `connect_tracer.py`.

It makes a `curl https://google.com` request, and the tracer logs the outbound connection attempt.

🎯 **Goal:** Catch suspicious network activity in CI.

---

## 🏴‍☠️ Step 4: Simulate Supply Chain Exfiltration

The workflow then runs:

```bash
bash simulate_exfil.sh
```

This simulates an attacker stealing secrets. Your tracers will flag both secret file access and the outbound exfil attempt.

🎯 **Goal:** Visualize a full supply chain attack path.

---

## 🗡️ Step 5: Detect Suspicious Binary Execution

Finally, the workflow runs `execve_tracer.py`.

It copies `/bin/ls` into `/tmp` and executes it. You’ll see alerts for binaries executed from `/tmp`.

🎯 **Goal:** Detect malware-style process execution.

---

## 🤖 Step 6: CI Integration with eBPF

All detectors are tied together in **`.github/workflows/hello-world.yml`**:

* Start tracers inside GitHub Actions
* Run attack simulation
* Log detections in Actions console
* Optionally fail the build on detection

Trigger again with:

```bash
git commit --allow-empty -m "Rerun workflow"
git push
```

🎯 **Goal:** See runtime detection working inside CI/CD.

---

## 🛠️ Step 7: Hack Time — Customize Detections

Edit **`.github/workflows/hello-world.yml`** to extend detectors:

* [ ] Add a Slack alert step on detection
* [ ] Ignore outbound connections to `github.com`
* [ ] Add `.pem` and `.aws` files to sensitive detection
* [ ] Detect if a `/tmp` binary spawns `curl`
* [ ] Bonus: modify [`supplychain-detect.py`](https://github.com/rohitcoder/rootconf-25-supplychain) and rebuild the Docker image

🎯 **Goal:** Adapt detectors to real attacker behaviors.

---

## 🔄 Step 8: Beyond GitHub Actions

We’ll close with how this approach extends to:

* Self-hosted runners
* Jenkins, GitLab, Azure Pipelines
* Sidecar-based monitoring in production

👉 Docs for self-hosted runners: [GitHub Runner Guide](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)

