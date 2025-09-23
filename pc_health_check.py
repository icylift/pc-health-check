import psutil
import platform
import socket
from datetime import datetime
import os
import GPUtil
import argparse
import json


# --------------------------------------------------------------------------------------- Data Collection Functions --------------------------------------------------------------------------------------------------------------
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

# Get GPU info
def get_gpu_info():
   gpus = GPUtil.getGPUs()
   gpu_data = {}
   for gpu in gpus:
      gpu_data[gpu.id] = {
         "Name": gpu.name,
         "Driver Version": gpu.driver,
         "Load (%)": f"{gpu.load * 100:.2f}",
         "Memory Total": f"{gpu.memoryTotal} MB",
         "Memory Used": f"{gpu.memoryUsed} MB",
         "Memory Free": f"{gpu.memoryFree} MB",
         "Temperature (°C)": gpu.temperature
      }
   return gpu_data

  

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


  # Get battery info
def get_battery_info():
   battery = psutil.sensors_battery()
   if battery is None:
      return{"Battery": "No battery detected"}
   
   # Convert seconds to hours:minutes 
   if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
      time_left = "Charging(time not available)"
   elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
      time_left = "Uknown"
   else:
      hours, remainder = divmod(battery.secsleft, 3600)
      minutes, _ = divmod(remainder, 60)
      time_left = f"{hours}h {minutes}m"
   
   return {
      "Battery Percantage": f"{battery.percent} %",
      "Power plugged": "Yes" if battery.pwer_plugged else "No",
      "Time Left": time_left
   }
  
# ------------------------------------------------------------------------------------------ Reporting & Format helpers --------------------------------------------------------------------------------------


def parse_args():
   parser = argparse.ArgumentsParser(description="PC Health Checker")
   parser.add_argument(
      "--format",
      choices=["text", "json", "csv"],
      default="text",
      help="Choose the output format (text, json, csv). Default is text."
   )
   return parser.parse.args()



def generate_report():
  lines = []
  lines.append("="*40 + " PC Health Check Report" + "="*40)

  lines.append("\n[System Info]")
  for k, v in get_system_info().items():
      lines.append(f"{k}: {v}")

  lines.append("\n[CPU Info]")
  for k, v in get_cpu_info().items():
      lines.append(f"{k}: {v}")

  lines.append("\n[Memory Info]")
  for k, v in get_memory_info().items():
      lines.append(f"{k}: {v}")

  lines.append("\n[Disk Info]")
  for device, stats in get_disk_info().items():
        lines.append(f"\nDevice: {device}")
        for k, v in stats.items():
            lines.append(f"  {k}: {v}")

  lines.append("\n[Network Info]")
  for k, v in get_network_info().items():
        lines.append(f"{k}: {v}")

  lines.append("\n[Uptime Info]")
  for k, v in get_uptime().items():
        lines.append(f"{k}: {v}")

  lines.append("\n[Uptime Info]")
  for k, v in get_uptime().items():
      lines.append(f"{k}: {v}")
  
  lines.append("\n[Battery Info]")
  for k, v in get_battery_info().items():
     lines.append(f"{k}: {v}")  

  lines.append("="*100)

  return "\n".join(lines)

def generate_json_report():
   report = {
      "System": get_system_info(),
      "Cpu": get_cpu_info(),
      "Memory": get_memory_info(),
      "Disk": get_disk_info(),
      "GPU": get_gpu_info(),
      "Network": get_network_info(),
      "Uptime": get_uptime(),
      "Battery": get_battery_info()
   }
   return json.dumps(report, indent=4) # this indent 4 is for better formatting

# ---------------------------------------------------------------------------------------- File Saving --------------------------------------------------------------------------------------------

def save_report(report_text):
   
   #Make a "reports" folder if it doesnt exist
  os.makedirs("reports", exist_ok=True)

  #create a file with current date and time
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  filename = f"reports/health_report_{timestamp}.txt"

  # Save the report
  with open(filename, "w") as f:
     f.write(report_text)

  print(f"Report saved to: {filename}")

if __name__ == "__main__":
    report_text = generate_report()
    print(report_text)
    save_report(report_text)








