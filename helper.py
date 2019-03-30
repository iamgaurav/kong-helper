import config as settings
import json
from kong import Kong
import logging
logger = logging.getLogger()
logger.setLevel(settings.DEBUG_LEVEL)


try:
    config = open('config.json', 'r')
    services = json.load(config)
except json.JSONDecodeError:
    logging.critical("Invalid Json")
    exit(1)
except FileNotFoundError:
    logger.critical("Config.json not found")
    exit(1)

if __name__ == "__main__":
    kong = Kong()
    for service in services.get('services'):
        service_name = service
        service_config = services.get('services').get(service_name)

        # Service Config
        service = {
            'name': service_name,
            'protocol': service_config.get('protocol', "http"),
            'host': service_config.get('upstream'),
            'port': service_config.get('port'),
        }
        logging.info("Updating service {}".format(service.get('name')))
        logging.debug(service)

        service_request = kong.add_service(service)

        # Route Config
        route = {
            'name': service_name,
            'protocols': [service_config.get('protocol', "http")],
            'hosts': service_config.get('hostname'),
            'paths': service_config.get('path'),
            'service': {
                'id': service_request.get('id')
            },
            'methods': service_config.get('methods')
        }
        logging.info("Updating route {}".format(route.get('name')))
        logging.debug(route)
        route_request = kong.add_route(route)

        # Plugins

        plugins = service_config.get("plugins", [])
        for plugin in plugins:
            plugin['service'] = {'id': service_request.get('id')}
            plugin['route'] = {'id':route_request.get('id')}
            logging.info("Updating Plugin {}".format(plugin))
            plugin_request = kong.add_plugin(plugin, service_request.get('id'))
