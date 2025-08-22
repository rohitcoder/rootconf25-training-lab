from bcc import BPF

bpf_program = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

TRACEPOINT_PROBE(syscalls, sys_enter_execve) {
    char fname[256];
    char comm[16];
    u32 pid = bpf_get_current_pid_tgid() >> 32;

    bpf_get_current_comm(&comm, sizeof(comm));
    bpf_probe_read_user_str(&fname, sizeof(fname), (void *)args->filename);

    bpf_trace_printk("[ALERT] Exec: %s (PID %d)\\n", fname, pid);

    return 0;
}
"""

b = BPF(text=bpf_program)
print("🚀 Tracing execve (process executions from /tmp)... (Ctrl+C to stop)")

try:
    b.trace_print()
except KeyboardInterrupt:
    print("\n🛑 Stopped tracing.")
