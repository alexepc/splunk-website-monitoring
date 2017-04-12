import splunk.admin as admin
import splunk.entity as entity
import splunk
import logging
import logging.handlers
import os
import re
import copy

from website_monitoring_app.rest_handler import RestHandler, setup_logger, BooleanFieldValidator, IntegerFieldValidator, StandardFieldValidator, HostFieldValidator

class ProxyTypeFieldValidator(StandardFieldValidator):
    """
    Validates proxy types.
    """

    def to_python(self, name, value):

        if value is None:
            return None

        # Prepare the string so that the proxy type can be matched more reliably
        t = value.strip().lower()

        if t not in ["socks4", "socks5", "http", ""]:
            raise admin.ArgValidationException("The value of '%s' for the '%s' parameter is not a valid proxy type" % ( str(value), name))

        return t

# Setup the handler
logger = setup_logger(logging.DEBUG, "WebsiteMonitoringRestHandler", "website_monitoring_rest_handler.log")

class WebsiteMonitoringRestHandler(RestHandler):
    """
    The REST handler provides configuration management for web ping.
    """

    # Below is the name of the conf file
    conf_file = 'website_monitoring'

    # Below are the list of parameters that are accepted
    PARAM_DEBUG = 'debug'
    PARAM_PROXY_SERVER = 'proxy_server'
    PARAM_PROXY_PORT = 'proxy_port'
    PARAM_PROXY_USER = 'proxy_user'
    PARAM_PROXY_PASSWORD = 'proxy_password'
    PARAM_PROXY_TYPE = 'proxy_type'

    # Below are the list of valid and required parameters
    valid_params = [PARAM_DEBUG, PARAM_PROXY_SERVER, PARAM_PROXY_PORT, PARAM_PROXY_USER, PARAM_PROXY_PASSWORD, PARAM_PROXY_TYPE]

    # List of fields and how they will be validated
    field_validators = {
        PARAM_DEBUG            : BooleanFieldValidator(),
        PARAM_PROXY_SERVER     : HostFieldValidator(),
        PARAM_PROXY_PORT       : IntegerFieldValidator(0, 65535),
        PARAM_PROXY_TYPE       : ProxyTypeFieldValidator()
    }

    # General variables
    app_name = "website_monitoring"

# initialize the handler
if __name__ == "__main__":
    
    admin.init(WebsiteMonitoringRestHandler, admin.CONTEXT_NONE)
