import socket
import requests

def get_ip_address():
  """Get the public IP address of the current machine"""
  try:
    response = requests.get("https://api.ipify.org?format=json")
    return response.json().get('ip')
  except Exception as e:
    return f"Error retrieving IP: {e}"

def get_provider_info(ip_address):
  """Get the ISP and location details for the given IP address."""
  try:
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    provider = data.get("org", "Unknown Provider")
    city = data.get("city", "Unknown City")
    region = data.get("region", "Unknown Region")
    country = data.get("country", "Unknown Country")
    return {
        "ip": ip_address,
        "provider": provider,
        "city": city,
        "region": region,
        "country": country
    }
  except Exception as e:
    return {"error": f"Failed to get provider info: {e}"}

def detect_and_log_provider():
  ip = get_ip_address()
  info = get_provider_info(ip)
  print("Provider Detection Report:")
  for key, value in info.items():
      print(f"{key}: {value}")
  # optional: log to a file or backend
  # with open('provider_log.txt', 'a') as file:
  #     file.write(f"{info}\n")
  return info

if __name__ == "__main__":
    detect_and_log_provider()
               
  
