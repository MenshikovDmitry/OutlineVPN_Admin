# Admin Panel for [OutlineVPN](https://getoutline.org/en-GB/) Server

## Description

This project is a proxy wrapper around the [OutlineVPN API](https://github.com/jadolg/outline-vpn-api). It allows to manage VPN keys, set data limits, and monitor usage.  
At this point it is very basic admin panel.
 
 **!!WARNING!!: This application is not secured and should not be exposed to the Internet directly. It must be placed behind a reverse proxy that handles authentication. Failure to do so can expose sensitive information and potentially allow unauthorized access.**

## Installation
Ensure that this container uses the same network as the OutlineVPN server.  
  
Use docker-compose:
```bash
version: '3.8'
services:
  outline_vpn_admin:
    image: dmitrymenshikov/outline_vpn_admin:latest
    container_name: outline_vpn_admin
    ports:
      - "8004:8000"
    environment:
      - API_URL=https://192.168.0.2:5858/api # URL of the outline API endpoint
      - API_TOKEN=<SECRET_TOKEN> # cert_sha256 for outline API access
      - HOSTNAME=http://localhost # hostname of this service. needed for the Frontend to know where to connect to
      - PORT=8004 # port of this service
```
## Environmental Variables:
- `API_URL` - URL of the Outline API endpoint. It must be visible in the network where the service runs (docker container)
- `API_TOKEN` - cert_sha256 for Outline API access
- `HOSTNAME` - hostname of this service. Must be visible from the network you are going to use this service. If you want to access it from the Internet, you must set it to the public IP or domain name of the server where this service runs. Authentication must be sorted by SWAG / NGINX + Authentik/Authelia or similar.

## Recommended setup:
First, I do recommend [SWAG](https://hub.docker.com/r/linuxserver/swag) as a reverse proxy. It is easy to set up and has a lot of features.  
Second, I like [Authentik](https://goauthentik.io/) to handle authentication and SSO.

**docker-compose.yaml**
```bash
version: '3.8'
services:
  outline_vpn_admin:
    image: dmitrymenshikov/outline_vpn_admin:latest
    container_name: outline_vpn_admin
# We do not expose the service to the internal network
#    ports:
#      - "8004:8000"
    environment:
      - API_URL=https://192.168.0.2:5858/api # URL of the outline API endpoint. Could be a name of the container
      - API_TOKEN=<SECRET_TOKEN> # cert_sha256 for outline API access
      - HOSTNAME=https://outline_vpn_admin.mydomain.com # hostname of this service. needed for the Frontend to know where to connect to
#      - PORT=8004 # port of this service. not needed if default protocol port is used
```

Example of NGINX config (for SWAG):
```nginx
## Version 2024/05/12
# make sure that your container is named outline_vpn_admin
# make sure that your dns has a cname set for outline_vpn_admin

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name outline_vpn_admin.*;

    include /config/nginx/ssl.conf;

    client_max_body_size 0;

    # enable for ldap auth (requires ldap-location.conf in the location block)
    #include /config/nginx/ldap-server.conf;

    # enable for Authelia (requires authelia-location.conf in the location block)
    #include /config/nginx/authelia-server.conf;

    # enable for Authentik (requires authentik-location.conf in the location block)
    include /config/nginx/authentik-server.conf;

    location / {
        # enable the next two lines for http auth
        #auth_basic "Restricted";
        #auth_basic_user_file /config/nginx/.htpasswd;

        # enable for ldap auth (requires ldap-server.conf in the server block)
        #include /config/nginx/ldap-location.conf;

        # enable for Authelia (requires authelia-server.conf in the server block)
        #include /config/nginx/authelia-location.conf;

        # enable for Authentik (requires authentik-server.conf in the server block)
        include /config/nginx/authentik-location.conf;

        include /config/nginx/proxy.conf;
        include /config/nginx/resolver.conf;
        set $upstream_app outline_vpn_admin;
        set $upstream_port 8000;
        set $upstream_proto http;
        proxy_pass $upstream_proto://$upstream_app:$upstream_port;

    }

}

```
## Contributing

Contributions are welcome. Please open an issue to discuss your idea before making a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.