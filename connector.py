import json
class Connector:
    def __init__(self):
        self.apps = []
        self.global_config = {"standardConfig": 0, "securedConfig": 0}

    def setApps(self, apps):
        for app in apps:
            if not isinstance(app, dict):
                raise ValueError("Each app must be a dictionary")
            required_keys = ["standardConfig", "securedConfig", "applicationType", "applicationName"]
            for key in required_keys:
                if key not in app:
                    raise ValueError(f"Missing required key: {key}")
                if key in ["standardConfig", "securedConfig"] and not isinstance(app[key], int):
                    raise ValueError(f"{key} must be an integer")
                if key in ["applicationType", "applicationName"] and not isinstance(app[key], str):
                    raise ValueError(f"{key} must be a string")
        
        self.apps = apps
        return self
    def setGlobalConfig(self, config):
        if not isinstance(config, dict):
            raise ValueError("Each global config must be a dictionary")
        required_keys = ["standardConfig", "securedConfig"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required key in global config: {key}")
            if key in ["standardConfig", "securedConfig"] and not isinstance(config[key], int):
                raise ValueError(f"{key} must be an integer in global config")        
        self.global_config = config
        return self
    def build(self):
        data = {
            "id": "f6c77ff0-b82b-48cb-baa9-3c353e2ff4af",
            "key": "connector-from-proxy",
            "version": 88888888,
            "name": "Connector from proxy",
            "description": "connector returned from proxy",
            "creator": {
                "id": "europe-west1.gcp:connect_qa",
                "name": "Harm Meijer from proxy",
                "email": "harm.meijer@commercetools.com",
                "company": "commercetools",
                "title": "Mr",
                "logoUrl": None,
                "noOfContributors": 1,
                "supportUrl": None
            },
            "repository": {
                "tag": "global-config-1",
                "url": "git@github.com:harm-meijer/test-connect-app.git"
            },
            "configurations": [self.map_app(app) for app in self.apps],
            "apiClient": {"scopes": ["manage_orders"] },
            "globalConfiguration": self.map_global(self.global_config),
            "private": False,
            "allowedProjects"	:[],
            "privateProjects": [],
            "integrationTypes": [],
            "supportedRegions": ["europe-west1.gcp"],
            "hasChanges": False,
            "status": "Draft",
            "alreadyListed": False,
            "certified": True,
            "publishingReport": None,
            "isPreviewable": "true",
            "previewableReport": {
                "entries": []
            },
            "documentationUrl": None,
            "requiresCertification": False
            }
        return json.dumps(data, indent=2)
    def generate_config_objects(self, config, config_type, prefix=""):
        if config == 0:
            return []
        return [
            {
                "key": f"{prefix}{config_type.upper()}_CONFIG_{i+1}",
                "description": f"{config_type} description {i+1}",
                "required": True
            }
            for i in range(config)
        ]
    def map_global(self, global_config):
        return {
            "standardConfiguration": self.generate_config_objects(global_config["standardConfig"], "standard","GLOBAL_"),
            "securedConfiguration": self.generate_config_objects(global_config["securedConfig"], "secured","GLOBAL_")
        }

    def map_app(self, app):
        return {
            "standardConfiguration": self.generate_config_objects(app["standardConfig"], "standard"),
            "securedConfiguration": self.generate_config_objects(app["securedConfig"], "secured"),
            "applicationType": app["applicationType"],
            "applicationName": app["applicationName"]
        }
