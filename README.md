# Admin Panel for [OutlineVPN](https://getoutline.org/en-GB/) Server

## Description

This project is a proxy wrapper around the [OutlineVPN API](https://github.com/jadolg/outline-vpn-api). It allows to manage VPN keys, set data limits, and monitor usage.

## Installation
Ensure that this container uses the same network as the OutlineVPN server.  
  
Use docker-compose:
```bash
version: '3.8'
services:
  outline_vpn_admin:
    image: dmitrymenshikov/outline_vpn_admin:latest
    ports:
      - "8004:8000"
    environment:
      - API_URL=https://192.168.0.2:5858/api # URL of the outline API endpoint
      - API_TOKEN=<SECRET_TOKEN> # cert_sha256 for outline API access
      - HOSTNAME=localhost # hostname of this service. needed for the Frontend to know where to connect to
      - PORT=8004 # port of this service
```
## Contributing

Contributions are welcome. Please open an issue to discuss your idea before making a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.