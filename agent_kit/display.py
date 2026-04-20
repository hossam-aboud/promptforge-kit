"""Terminal display utilities: colors, spinner, formatting."""

import sys
import time
import threading
import itertools
from contextlib import contextmanager


class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    @staticmethod
    def strip_if(text: str, no_color: bool) -> str:
        if no_color:
            import re
            return re.sub(r"\033\[[0-9;]*m", "", text)
        return text


BANNER = r"""
   ██████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██╗  ██╗██╗████████╗
  ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ██║ ██╔╝██║╚══██╔══╝
  ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       █████╔╝ ██║   ██║   
  ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██╔═██╗ ██║   ██║   
  ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ██║  ██╗██║   ██║   
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═╝╚═╝   ╚═╝   
"""


def print_banner() -> None:
    print(f"{Colors.CYAN}{BANNER}{Colors.RESET}")
    print(f"  {Colors.DIM}Generate optimized prompts for every AI coding agent{Colors.RESET}\n")


def print_step(n: int, msg: str) -> None:
    print(f"  {Colors.CYAN}{Colors.BOLD}[{n}]{Colors.RESET} {msg}")


def print_section(title: str) -> None:
    bar = "═" * (len(title) + 4)
    print(f"  {Colors.BOLD}{Colors.BLUE}╔{bar}╗{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BLUE}║  {title}  ║{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BLUE}╚{bar}╝{Colors.RESET}")
    print()


def print_success(msg: str) -> None:
    print(f"\n  {Colors.GREEN}{Colors.BOLD}✅  {msg}{Colors.RESET}\n")


def print_error(msg: str) -> None:
    print(f"\n  {Colors.RED}{Colors.BOLD}✗  {msg}{Colors.RESET}\n", file=sys.stderr)


@contextmanager
def spinner(label: str):
    """Simple terminal spinner context manager."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    stop_event = threading.Event()

    def _spin():
        for frame in itertools.cycle(frames):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r  {Colors.CYAN}{frame}{Colors.RESET}  {label}...")
            sys.stdout.flush()
            time.sleep(0.08)

    thread = threading.Thread(target=_spin, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop_event.set()
        thread.join()
        sys.stdout.write(f"\r  {Colors.GREEN}✓{Colors.RESET}  {label}    \n")
        sys.stdout.flush()
