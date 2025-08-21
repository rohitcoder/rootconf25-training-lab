# 🧑‍💻 Rootconf 2025 Workshop: **Detecting Supply Chain Attacks at Runtime with eBPF**

Welcome! In this workshop, you’ll learn how to detect **supply chain attacks** using **eBPF** — by tracing runtime behaviors that static scanners miss.

No kernel or eBPF experience needed. Just follow along.

---

## ✅ What You'll Do

* Trace file access, network connections, and suspicious process behavior
* Simulate real-world supply chain exfiltration
* Integrate eBPF detection into CI pipelines (GitHub Actions)
* Customize detections to match attacker behaviors
* Add Slack alerts & fail builds on runtime threats

---

## 🗂 Repo Structure

```
rootconf25-training-lab/
├── .github/workflows/hello-world.yml  # Main CI workflow for detectors
├── connect_tracer.py                  # Outbound connections tracer
├── execve_tracer.py                   # Suspicious binary execution tracer
├── openat_tracer.py                   # File access tracer (.env etc)
├── simulate_exfil.sh                  # Simulates secret exfiltration
├── troubleshoot.md                    # Common issues & solutions
```

---

## 📝 Prerequisites

* GitHub account
* Fork this repository into your own GitHub account

That’s it — no VM setup, no Docker install. Everything runs in **GitHub Actions (`ubuntu-latest`)**.

---

## 🏁 Step 1: Fork & Trigger Workflow (5 mins)

1. Fork this repo to your GitHub account
2. Clone it locally (optional):

   ```bash
   git clone https://github.com/<your-username>/rootconf25-training-lab.git
   cd rootconf25-training-lab
   ```
3. Push a dummy commit to trigger the workflow:

   ```bash
   git commit --allow-empty -m "Trigger CI"
   git push
   ```

Open the **Actions** tab in your repo to see the workflow run.

---

## 🔍 Step 2: Detect Sensitive File Access (.env) (15 mins)

We’ll use `openat_tracer.py` to catch access to sensitive files like `.env`.

Check **hello-world.yml** → it already runs this tracer. Logs will show whenever `.env` or `.aws` files are accessed.

🎯 **Goal:** Understand syscalls, tracepoints, and live observability.

---

## 🌐 Step 3: Detect Outbound Connections (15 mins)

Next, the workflow runs `connect_tracer.py` to trace outbound connections.

When the workflow makes a `curl https://google.com` request, you’ll see the tracer log it.

🎯 **Goal:** Catch suspicious outbound traffic in real time.

---

## 🏴‍☠️ Step 4: Simulate Supply Chain Exfiltration (15 mins)

The workflow will automatically run:

```bash
bash simulate_exfil.sh
```

This simulates an attacker stealing secrets. The tracers from earlier steps will catch both file access and the exfil attempt.

🎯 **Goal:** Visualize a full supply chain attack flow.

---

## 🗡️ Step 5: Detect Suspicious Binary Execution (15 mins)

The workflow also runs `execve_tracer.py`.

It copies `/bin/ls` into `/tmp` and executes it. Logs will show alerts for binaries executed from `/tmp`.

🎯 **Goal:** Understand process execution tracing for malware detection.

---

## 🤖 Step 6: CI Integration with eBPF Detection (30 mins)

Now you’ll see everything tied together in **hello-world.yml**:

* Starts tracers inside GitHub Actions
* Simulates an attack
* Logs detections in the Actions console
* Can optionally **fail the build** on detection

Trigger again with:

```bash
git commit --allow-empty -m "Rerun workflow"
git push
```

🎯 **Goal:** See runtime detection inside CI pipelines.

---

## 🛠️ Step 7: Hack Time — Customize Detections (30 mins)

Your turn to extend the detectors by editing `.github/workflows/hello-world.yml`.

### Challenges

* [ ] Add a step to send a Slack alert when detection happens
* [ ] Ignore outbound connections to `github.com`
* [ ] Extend sensitive file list to include `.pem` and `.aws`
* [ ] Detect if a binary from `/tmp` spawns `curl` (process chain)
* [ ] Bonus: tweak `supplychain-detect.py` and rebuild the image

🎯 **Goal:** Adapt detectors to real attacker behaviors.

---

## 🔄 Step 8: Extending Beyond GitHub (10 mins)

Quick discussion on:

* Using self-hosted runners in GitHub Actions
* Reusing the same detectors in Jenkins, GitLab, Azure Pipelines
* Sidecar pattern for runtime monitoring

👉 Docs if you want to try self-hosted: [GitHub Runner Guide](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)

Do you want me to also prep a **ready-to-run `hello-world.yml`** that already includes all steps (file access, connect, exec, simulate) so participants just fork and push to see detections?
