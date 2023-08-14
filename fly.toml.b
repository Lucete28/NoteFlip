# fly.toml app configuration file generated for fastapi-jhy-app on 2023-08-14T12:16:47+09:00
#
# See https://fly.io/docs/reference/configuration/ for information about how to use this file.
#

app = "fastapi-jhy-app"
primary_region = "nrt"

[build]
  image = "lucete28/fastapi:0.0.1"

[env]
  PORT = "80"
