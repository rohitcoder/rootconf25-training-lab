name: Test eBPF openat

on:
  workflow_dispatch:   # run manually from GitHub Actions tab

jobs:
  ebpf-test-openat:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies (BCC, Python, kernel headers)
        run: |
          sudo apt-get update
          sudo apt-get install -y bpfcc-tools python3-bpfcc linux-headers-$(uname -r)

      - name: Run eBPF script (trace openat/openat2)
        run: |
          cat > openat_probe.py <<'EOF'
          from bcc import BPF

          bpf_code = """
          #include <uapi/linux/ptrace.h>
          #include <linux/sched.h>
          #include <linux/limits.h>

          TRACEPOINT_PROBE(syscalls, sys_enter_openat) {
              char comm[TASK_COMM_LEN] = {};
              char fname[PATH_MAX] = {};

              bpf_get_current_comm(&comm, sizeof(comm));
              int ret = bpf_probe_read_user_str(&fname, sizeof(fname), args->filename);

              if (ret > 0) {
                  bpf_trace_printk("[OPENAT] %s opened %s\\n", comm, fname);
              }
              return 0;
          }

          TRACEPOINT_PROBE(syscalls, sys_enter_openat2) {
              char comm[TASK_COMM_LEN] = {};
              char fname[PATH_MAX] = {};

              bpf_get_current_comm(&comm, sizeof(comm));
              int ret = bpf_probe_read_user_str(&fname, sizeof(fname), args->filename);

              if (ret > 0) {
                  bpf_trace_printk("[OPENAT2] %s opened %s\\n", comm, fname);
              }
              return 0;
          }
          """

          b = BPF(text=bpf_code)
          print("Tracing ALL openat/openat2 file opens... Ctrl+C to stop.")

          # Run for 20 seconds to capture events
          try:
              b.trace_print(duration=20)
          except KeyboardInterrupt:
              pass
          EOF

          sudo python3 openat_probe.py
