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



## Understanding Syscall Symbols, Kprobes, and Tracepoints

When we write eBPF programs, we need to know where to attach them. These attachment points are called hooks. The two most common ways are **kprobes** (on kernel functions) and **tracepoints** (on predefined kernel events).

### Syscall Symbols (via Kprobes)

A syscall is how a program asks the Linux kernel to do something, like open a file or start a process. For example, when you run `ls`, under the hood it calls the `execve` syscall to create a new process.

Kprobes let us attach eBPF programs to kernel functions directly. You can discover available functions by looking in `/proc/kallsyms`. For example:

```
ffffffff8118c920 T __x64_sys_execve
ffffffff8118c930 T __x64_sys_openat
```

* `__x64_sys_execve` is the function called when a new process is created.
* `__x64_sys_openat` is the function used when opening files.

With a kprobe, you can attach to these functions. For instance, to detect whenever a new process starts:

```c
int kprobe____x64_sys_execve(struct pt_regs *ctx) {
    bpf_trace_printk("Process started (kprobe)\n");
    return 0;
}
```

The drawback is that these function names can vary between kernel versions, so kprobes can break if you upgrade the kernel.

---

### Tracepoints

Tracepoints are predefined events added by kernel developers for observability. They are stable across kernel versions and safer to use long-term. You can find them under:

```
/sys/kernel/debug/tracing/events/
```

For process execution, common tracepoints are:

```
syscalls/sys_enter_execve
syscalls/sys_exit_execve
```

Using a tracepoint, you can log every command that gets executed:

```c
TRACEPOINT_PROBE(syscalls, sys_enter_execve) {
    bpf_trace_printk("Command executed (tracepoint): %s\n", args->filename);
    return 0;
}
```

Tracepoints don’t give you access to every kernel function like kprobes do, but they are stable and portable.

---

### Putting It Together

If malware drops a file into `/tmp` and runs it:

* A **kprobe** on `__x64_sys_execve` would catch the raw function call that launches the process.
* A **tracepoint** on `syscalls:sys_enter_execve` would catch the stable event that indicates a process execution.

Both approaches can detect the behavior, but the choice depends on your needs.

* Use kprobes when you need flexibility and access to low-level kernel internals.
* Use tracepoints when you need reliability across different Linux versions.

Here’s a simple text diagram you can drop directly into your workshop docs. It shows how syscalls work, and where **kprobes** and **tracepoints** hook in:

---

## Where Kprobes and Tracepoints Hook

```
+-------------------------+        User space
|   User program (ls)     |
+-------------------------+
              |
              |   makes a syscall (execve)
              v
+-------------------------+        Kernel entry
|   Syscall interface     |  <---- Tracepoint: sys_enter_execve
+-------------------------+
              |
              v
+-------------------------+        Kernel space
|  __x64_sys_execve()     |  <---- Kprobe hooks here
+-------------------------+
              |
              v
+-------------------------+        
|   Kernel does the work  |
+-------------------------+
```

* The user program runs `ls`.
* This calls the syscall **execve** to start a process.
* **Tracepoint** (`sys_enter_execve`) is triggered at the syscall entry.
* **Kprobe** can attach directly to the kernel function (`__x64_sys_execve`).

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

## 🔍 Step 7: Exploring Available Hooks

Want to go beyond the examples? You can discover which kernel functions are available to attach eBPF programs to.

### 1. List Kernel Functions (for kprobes)

```bash
cat /proc/kallsyms | grep ' sys_'
```

This shows all kernel syscalls (like `sys_openat`, `sys_execve`, `sys_connect`).
➡️ These are the same hooks we used for file, process, and network tracing.

### 2. Check Tracepoints

```bash
ls /sys/kernel/debug/tracing/events
```

Tracepoints are stable kernel events (e.g., `syscalls/sys_enter_openat`).
➡️ They’re safer for long-term use than raw function names.

### 3. Explore BCC Tool Examples

```bash
git clone https://github.com/iovisor/bcc.git
cd bcc/tools
ls
```

You’ll see ready-to-use examples like `execsnoop`, `opensnoop`, `tcpconnect`.
➡️ These are great starting points for your own detectors.

## 🛠️ Step 8: Hack Time — Customize Detections

Edit **`.github/workflows/hello-world.yml`** to extend detectors:

* [ ] Add a Slack alert step on detection
* [ ] Ignore outbound connections to `github.com`
* [ ] Add `.pem` and `.aws` files to sensitive detection
* [ ] Detect if a `/tmp` binary spawns `curl`
* [ ] Bonus: modify [`supplychain-detect.py`](https://github.com/rohitcoder/rootconf-25-supplychain) and rebuild the Docker image

🎯 **Goal:** Adapt detectors to real attacker behaviors.

## 🔄 Step 9: Beyond GitHub Actions

We’ll close with how this approach extends to:

* Self-hosted runners
* Jenkins, GitLab, Azure Pipelines
* Sidecar-based monitoring in production

👉 Docs for self-hosted runners: [GitHub Runner Guide](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)

