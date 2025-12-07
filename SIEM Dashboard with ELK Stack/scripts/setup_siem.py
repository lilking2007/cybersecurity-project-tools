import requests
import time
import json
import sys

ES_HOST = "http://localhost:9200"

def wait_for_es():
    print("Waiting for Elasticsearch...")
    retries = 30
    for i in range(retries):
        try:
            r = requests.get(ES_HOST)
            if r.status_code == 200:
                print("Elasticsearch is up!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
        print(f"Retrying... ({i+1}/{retries})")
    return False

def create_ilm_policy():
    url = f"{ES_HOST}/_ilm/policy/siem-policy"
    # Blueprint: Hot, Warm, Cold/Frozen.
    # We simulate this by moving data to 'warm' phase after 1 day (for demo purposes)
    payload = {
        "policy": {
            "phases": {
                "hot": {
                    "min_age": "0ms",
                    "actions": {
                        "rollover": {
                            "max_size": "50GB",
                            "max_age": "1d"
                        }
                    }
                },
                "warm": {
                    "min_age": "1d",
                    "actions": {
                        "shrink": {
                            "number_of_shards": 1
                        },
                        "forcemerge": {
                            "max_num_segments": 1
                        }
                    }
                },
                "delete": {
                    "min_age": "30d",
                    "actions": {
                        "delete": {}
                    }
                }
            }
        }
    }
    r = requests.put(url, json=payload, headers={"Content-Type": "application/json"})
    print(f"ILM Policy creation: {r.status_code} - {r.text}")

def create_index_template():
    # Component for settings
    settings_url = f"{ES_HOST}/_component_template/siem-settings"
    settings_payload = {
        "template": {
            "settings": {
                "index.lifecycle.name": "siem-policy",
                "index.lifecycle.rollover_alias": "siem-logs",
                "number_of_shards": 1,
                "number_of_replicas": 0 
            }
        }
    }
    r = requests.put(settings_url, json=settings_payload, headers={"Content-Type": "application/json"})
    print(f"Component Template creation: {r.status_code} - {r.text}")

    # Index template
    template_url = f"{ES_HOST}/_index_template/siem-template"
    template_payload = {
        "index_patterns": ["siem-logs-*"],
        "composed_of": ["siem-settings"],
        "priority": 100,
        "template": {
            "mappings": {
                "properties": {
                    "@timestamp": { "type": "date" },
                    "source.ip": { "type": "ip" },
                    "geoip.location": { "type": "geo_point" },
                    "host.hostname": { "type": "keyword" },
                    "event.dataset": { "type": "keyword" }
                }
            }
        }
    }
    r = requests.put(template_url, json=template_payload, headers={"Content-Type": "application/json"})
    print(f"Index Template creation: {r.status_code} - {r.text}")

if __name__ == "__main__":
    if wait_for_es():
        create_ilm_policy()
        create_index_template()
        print("SIEM Setup complete. You can now start Logstash.")
    else:
        print("Could not connect to Elasticsearch.")
