# lauzhack-gina

# Bring up API

- `docker-compose up` 
    - brings up all the services
    - `docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) && docker-compose up --build`
    - force kill all: `killall Docker && open /Applications/Docker.app` and then `docker-compose down`
- `cloudflared tunnel --config ./tunnel_config.yaml run gina`
    - main site on `gina.henrybear327.com`
    - kibana on `kibana.henrybear.327`
        - Search for `Data/Index Management` to see all index
<!-- - `./start.sh` (for demo use `start_henry.sh` on Henry's machine)
    - brings up the tunnel, look for `Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):`, and use the url there
        - issues with https has been solved by registering a tunnel with a domain name, but due to security concerns I won't upload it here -->

# Note

- Hot reload `touch api/uwsgi.ini`
- Test insertion 
    - `curl -i -H "Content-Type: application/json" -X POST -d '{"metadata":"{}", "fullBodyText": "full body text"}' https://gina.henrybear327.com/api/es/insert`
- Within docker container, we need to use the docker compose's container name as URL to access others
- [Multiple file uploaded](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)

## Cloudflare tunnel

- [Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/local/)

## [Virtual Env](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

- `python3 -m venv env`
- `source env/bin/activate`
- `python3 -m pip install -r requirements.txt`
- `python3 -m pip install elasticsearch`
- `python3 -m pip freeze > requirements.txt`

## ES
- `./elastic_search.sh`
    - Setup password for elastic search and test the curl
    - It's for the original setup
- Index, and adjust type
```
# Click the Variables button, above, to create your own variables.
PUT corpus
{
  "mappings": {
    "properties": {
      "course_title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "filetype": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "full_text": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "text"
          }
        }
      },
      "inserted_at": {
        "type": "date"
      },
      "timestamp": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "timestamped_text": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "url": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}
```

# Using Parser for videos:

- `python3 parser.py {api-key} {course_id_from_browser} ./downloads`