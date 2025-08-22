from bcc import BPF

bpf_code = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

TRACEPOINT_PROBE(syscalls, sys_enter_openat) {
    char comm[16] = {};
    char fname[256] = {};

    bpf_get_current_comm(&comm, sizeof(comm));
    int ret = bpf_probe_read_user_str(&fname, sizeof(fname), args->filename);

    bpf_trace_printk("[.env READ] Process: %s\\n", comm);
    bpf_trace_printk("             File: %s\\n", fname);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_enter_openat2) {
    char comm[16] = {};
    char fname[256] = {};

    bpf_get_current_comm(&comm, sizeof(comm));
    int ret = bpf_probe_read_user_str(&fname, sizeof(fname), args->filename);

    bpf_trace_printk("[.env READ] Process: %s\\n", comm);
    bpf_trace_printk("             File: %s\\n", fname);

    return 0;
}
"""

b = BPF(text=bpf_code)
print("Tracing ONLY .env file opens (openat & openat2 tracepoints)... Ctrl+C to stop.")
b.trace_print()
