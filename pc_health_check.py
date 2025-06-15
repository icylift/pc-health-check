import psutil
import platform
import socket
from datetime import datetime
import os


# Get system info
def get_system_info():
  uname = platform.uname()
  return  {
    "System": uname.system,
    "Node Name": uname.node,
    "Release": uname.release,
    "Version": uname.version,
    "Machine": uname.machine,
    "Processor": uname.processor
  }



# Get cpu info/usage
def get_cpu_info():
  return{
    "Physical Cores": psutil.cpu_count(logical=False),
    "Total Cores": psutil.cpu_count(logical=True),
    "Cpu Usage (%)": psutil.cpu_percent(interval=1)
  }



# Get memory usage
def get_memory_info():
  svmem = psutil.virtual_memory()
  return {
    "Total": f"{svmem.total / (1024**3):.2f} GB",
    "Available": f"{svmem.available / (1024**3):.2f} GB",
    "Used": f"{svmem.used / (1024**3):.2f} GB",
    "Percentage": f"{svmem.percent} %"
  }


# Get disk usage
def get_disk_info():
  partitions = psutil.disk_partitions()
  usage_data = {}
  for partition in partitions:
    try:
      usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
      continue
    usage_data[partition.device] = {
      "Mountpoint": partition.mountpoint,
      "File System Type": partition.fstype,
      "Total Size": f"{usage.total / (1024**3):.2f} GB",
      "Used": f"{usage.used / (1024**3):.2f} GB",
      "Free": f"{usage.free / (1024**3):.2f} GB",
      "Percentage": f"{usage.percent} %"
    }
  return usage_data

  # Network info
def get_network_info():
  hostname = socket.gethostname()
  ip_address = socket.gethostbyname(hostname)
  return {
      "Hostname": hostname,
      "IP Address": ip_address
  }


  # System uptime
def get_uptime():
  boot_time = datetime.fromtimestamp(psutil.boot_time())
  return {
    "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
    "Uptime (hrs)": round((datetime.now() - boot_time).total_seconds() / 3600, 2)
  }
  
  # Disply / Print
def print_report():
  print("="*40, "PC Health Check Report", "="*40)
  print("\n[System Info]")
  for k, v in get_system_info().items():
      print(f"{k}: {v}")

  print("\n[CPU Info]")
  for k, v in get_cpu_info().items():
      print(f"{k}: {v}")

  print("\n[Memory Info]")
  for k, v in get_memory_info().items():
      print(f"{k}: {v}")

  print("\n[Disk Info]")
  for device, stats in get_disk_info().items():
      print(f"\nDevice: {device}")
      for k, v in stats.items():
          print(f"  {k}: {v}")

  print("\n[Network Info]")
  for k, v in get_network_info().items():
      print(f"{k}: {v}")

  print("\n[Uptime Info]")
  for k, v in get_uptime().items():
      print(f"{k}: {v}")

  print("="*100)

if __name__ == "__main__":
    print_report()

