import requests
import config
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Kong:

    services = None
    routes = None
    plugins = None

    """
    Helper function to pull all the current services in kong
    """
    def __update_services(self):
        req = requests.get("{0}/{1}".format(config.KONG_URL, 'services'))
        response = req.json()
        self.services = list(map(lambda x: x['name'], response.get('data')))

    """
    Helper function to pull all the current routes in kong
    """
    def __update_routes(self):
        req = requests.get("{0}/{1}".format(config.KONG_URL, 'routes'))
        response = req.json()
        self.routes = list(map(lambda x: x['name'], response.get('data')))

    """
    Helper function to pull all the current plugins in kong
    """
    def __update_plugins(self):
        req = requests.get("{0}/{1}".format(config.KONG_URL, 'plugins'))
        response = req.json()
        self.routes = list(map(lambda x: x['name'], response.get('data')))

    @staticmethod
    def update_service(service_config):
        request = requests.put('{0}/services/{1}'.format(config.KONG_URL, service_config.get('name')),
                               json=service_config)
        logging.debug(request.json())
        return request.json()

    def add_service(self, service_config, update=True):
        self.__update_services()
        if service_config.get('name') in self.services and update:
            logging.debug("Service already exists. Updating it")
            return Kong.update_service(service_config)
        logging.debug("Adding service to Kong")
        request = requests.post('{0}/services'.format(config.KONG_URL), json=service_config)
        logging.debug(request.json())
        return request.json()

    @staticmethod
    def update_route(route_config):
        request = requests.put('{0}/routes/{1}'.format(config.KONG_URL, route_config.get('name')),
                               json=route_config)
        logging.debug(request.json())
        return request.json()

    def add_route(self, route_config, update=True):
        self.__update_routes()
        if route_config.get('name') in self.routes and update:
            logging.debug("Route service exists in Kong. Updating it")
            return Kong.update_route(route_config)

        logging.debug("Adding route to Kong")
        request = requests.post('{0}/routes'.format(config.KONG_URL), json=route_config)
        logging.debug(request.json())
        return request.json()


    @staticmethod
    def update_plugin(plugin_config):
        request = requests.put('{0}/routes/{1}'.format(config.KONG_URL, plugin_config.get('name')),
                               json=plugin_config)
        logging.debug(request.json())
        return request.json()

    def add_plugin(self, plugin_config, update=True):
        self.__update_routes()
        if plugin_config.get('name') in self.plugins and update:
            logging.debug("Plugin exists in Kong. Updating it")
            return Kong.update_route(plugin_config)

        logging.debug("Adding plugin to Kong")
        request = requests.post('{0}/routes'.format(config.KONG_URL), json=plugin_config)
        logging.debug(request.json())
        return request.json()