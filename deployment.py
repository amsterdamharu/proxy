import json
class Deployment:
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
            "id": "ed54a36c-5191-44ab-abee-35379d7fd413",
            "key": None,
            "version": 888888,
            "projectId": "europe-west1.gcp:harm-sandbox-3",
            "connector": {
                "id": "ecba03f6-854b-4108-81d0-b110b19efab6",
                "key": "harm-connector-9",
                "version": 8888888,
                "name": "Global config example",
                "description": "Harm test connector 2",
                "creator": {
                    "name": "Harm Meijer",
                    "title": "Mr",
                    "email": "harm.meijer@commercetools.com",
                    "company": "commercetools",
                    "noOfContributors": 1,
                    "supportUrl": None,
                    "logoUrl": None
                },
                "repository": {
                "url": "git@github.com:harm-meijer/test-connect-app.git",
                "tag": "global-config-1"
                },
                "configurations": [self.map_app(app) for app in self.apps],
                "apiClient": {"scopes": ["manage_orders"] },
                "globalConfiguration": self.map_global(self.global_config),
                "supportedRegions": ["europe-west1.gcp"],
                "integrationTypes": [],
                "certified": False,
                "documentationUrl": None
            },
            "deployedRegion": "europe-west1.gcp",
            "applications": [self.map_app_values(app) for app in self.apps],
            "globalConfiguration": self.map_global_values(self.global_config),
            "details": {
                "build": {
                "id": "61505009-e162-4662-86db-244a795e3dfe",
                "report": {
                    "entries": [
                    {
                        "title": "Script for postDeploy not defined",
                        "type": "Information",
                        "application": "service",
                        "message": None,
                        "createdAt": "2024-10-03T09:30:24.801Z"
                    }
                    ]
                }
                }
            },
            "preview": True,
            "status": "Deployed",
            "createdAt": "2024-10-03T09:27:32.121Z"
        }
        return json.dumps(data, indent=2)
    def generate_config_values(self, config, config_type, prefix=""):
        if config == 0:
            return []
        return [
            {
                "key": f"{prefix}{config_type.upper()}_CONFIG_{i+1}",
                "value": f"{prefix}{config_type.upper()}_CONFIG_{i+1}",
            }
            for i in range(config)
        ]
    def map_global_values(self, global_config):
        return {
            "standardConfiguration": self.generate_config_values(global_config["standardConfig"], "standard","GLOBAL_"),
            "securedConfiguration": self.generate_config_values(global_config["securedConfig"], "secured","GLOBAL_")
        }
    def map_app_values(self, app):
        return {
            "standardConfiguration": self.generate_config_values(app["standardConfig"], "standard"),
            "securedConfiguration": self.generate_config_values(app["securedConfig"], "secured"),
            "applicationType": app["applicationType"],
            "applicationName": app["applicationName"]
        }
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
