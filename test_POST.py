import requests

url = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7C35e0550e-953a-41b5-ba97-cacaa4a44160%7C46c7b53b-f027-4a85-a685-04d8613dec77"

payload = "{\r\n    \"userId\": \"f6aa8e63-4d55-4e6a-a37e-0b388a2cf382\",\r\n    \"officeId\": \"9b122c05-e7d6-4ce4-9936-0d3a8cfcc6c8\",\r\n    \"zoneId\": \"35e0550e-953a-41b5-ba97-cacaa4a44160\",\r\n    \"vehicle\": {\r\n        \"id\": \"28eb114a-2fc2-4e74-a1c9-e5de83c135b8\",\r\n        \"objectType\": \"OM.Vehicle\",\r\n        \"schemaVersion\": 0.1,\r\n        \"createdBy\": \"OM.Api\",\r\n        \"createdAtUtc\": \"2024-01-09T07:00:07.7880889Z\",\r\n        \"modifiedBy\": \"OM.Api\",\r\n        \"modifiedAtUtc\": \"\",\r\n        \"type\": \"Car\",\r\n        \"engine\": \"Fuel\",\r\n        \"licensePlate\": \"5827LCN\"\r\n    },\r\n    \"bookingType\": \"Day\",\r\n    \"turn\": \"AllDay\",\r\n    \"date\": \"2023-02-16\",   \r\n    \"seatId\": [],\r\n    \"isGroupReservation\": false,\r\n    \"isCarSharing\": false\r\n}"
headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InpWVjNyd2hYSlRZRVRnWlczeG9BSnBia0Vienl0T01TWjctS3U2SHZISzAiLCJ0eXAiOiJKV1QifQ.eyJ0aWQiOiIzMDU1ZmE3Zi1hOTQ0LTQ5MjctODAxZS1hNjJiNjMxMTllNDMiLCJuYW1lIjoiSMOpY3RvciBHb256w6FsZXogRGUgbGEgVmVyYSIsImVtYWlsIjoiaGVjdG9yLmdvbnphbGV6QHNlY3VyaXRhc2RpcmVjdC5lcyIsImlkcCI6Im1hbmFnZXJvZmZpY2UiLCJzdWIiOiJmNmFhOGU2My00ZDU1LTRlNmEtYTM3ZS0wYjM4OGEyY2YzODIiLCJPTVRlbmFudElkIjoiN2E5MDNhYzYtYWViNS00Y2Y4LTg3OWMtYzQ4ZjAyZmMzNmU3IiwiT01TdWJzY3JpcHRpb25FbmFibGVkIjp0cnVlLCJPTVN1YnNjcmlwdGlvbkV4cGlyYXRpb25EYXRlIjoxNzQ2MDg2NDAwLCJPTVVzZXJFbmFibGVkIjp0cnVlLCJPTUdyb3VwcyI6ImZmNTBjNzU3LTczYTktNDZiZC05OTFlLTVkYmVlMTIwNDAwYjthODNhYWM4ZC0xNGU5LTQwNzAtYmU3Zi02YmE0NWE4ZjQzN2EiLCJPTVJvbGVzIjoiUGFya2luZ0FwcFVzZXI7Um9vbUFwcFVzZXIiLCJwYXNzd29yZEV4cGlyZWQiOmZhbHNlLCJub25jZSI6IjgwMWU1NjllLTYwMzUtNDYzMS04NWUwLTk4ZTQwYmViZjM0NCIsInNjcCI6ImFjY2Vzc19hc191c2VyIiwiYXpwIjoiNTM0MTZhOTItODVhYS00Yzg2LWJkZTAtM2MwNmE3ZmQ4YzAwIiwidmVyIjoiMS4wIiwiaWF0IjoxNzA3NzQ5NDk5LCJhdWQiOiI2ZDc3NDkzYS0yNGYwLTQ1YmMtYjYxZC0zNDE5YjU5MTAzNWQiLCJleHAiOjE3MDc3NTMwOTksImlzcyI6Imh0dHBzOi8vbWFuYWdlcm9mZmljZS5iMmNsb2dpbi5jb20vNDU4NDkyZWItZjI4Yi00MTRkLTk4ZGQtMWJmMzFhN2I0NTNmL3YyLjAvIiwibmJmIjoxNzA3NzQ5NDk5fQ.QWIaplXzX3bTc8Lx8gOlByfGo2-hr_2CTbrBYpU0mP-Pf37YWmAdZsNunoE2PlVrgnUURzis4F29PxxIrdjoHLH0UBJPHSvAl3X1YxzBSHFsGAkaSLOykW-X3D_fAvVXkLQKbXsZbwbz10mo5JvARCQqbXE84axfbUrzfgov45KaDG1mzRLHzIW8ek2Uv6c-j6hI1EGq0779r7B94G5s0-yH2c11MwkyH2vzk7nREONgKg2pCGs-c904M202ODEdbENnYmxH7Jo3b-TkM1C7VO50Mc38Hbzc37o91s1wr8wvzycY9XbKoZTX05eFcDOk8X9f3AoxbgqpoC7m_G3l5A',
    'Cookie': 'ARRAffinity=7d1904e779b5d7cce2a9049d3258cb7573c139d3dd3c9d3796f805a81e3f77bb; ARRAffinitySameSite=7d1904e779b5d7cce2a9049d3258cb7573c139d3dd3c9d3796f805a81e3f77bb; TiPMix=17.900988809341676; x-ms-routing-name=self',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://app-officemanager.raona.com',
    'Referer': 'https://app-officemanager.raona.com/'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
