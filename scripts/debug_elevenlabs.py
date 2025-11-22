import requests

API_KEY = "f0e2bdbab499ce82cc5ab7641783aa51cb118e594bef3e8d5b8ea7be03e73e2c"
VOICE_ID = "lxZLq5dcyw12UangGJgN"
URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

print(f"Testing Voice ID: {VOICE_ID}")
print(f"Using Key: {API_KEY[:5]}...{API_KEY[-5:]}")

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}
data = {
    "text": "Merhaba, bu bir testtir.",
    "model_id": "eleven_multilingual_v2"
}

response = requests.post(URL, json=data, headers=headers)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("SUCCESS! Audio generated.")
else:
    print("FAILURE!")
    print(response.text)
