import sys
import logging


# Setting up loggin for splunkd
logging.root
logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)


# Splunk Requires a Introspection scheme, setting a var for this for now
SCHEME = """<scheme>
    <title>Openstack Swift</title>
    <description>Get data from Openstack Swift Storage deployments, such as Rackspaces' Cloud Files.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <endpoint>
        <args>
            <arg name="name">
                <title>Resource name</title>
                <description>An Swfit resource name without the leading swift://.  
                   For example, for swift://container/file.txt specify container/file.txt.  
                   You can also monitor a whole container (for example by specifying 'container'),
                   or files within a sub-directory of a container
                   (for example 'container/some/directory/'; note the trailing slash).
                </description>
            </arg>

            <arg name="api_id">
                <title>API ID</title>
                <description>Your API ID (username).</description>
            </arg>

            <arg name="api_key">
                <title>API key</title>
                <description>Your API key.</description>
            </arg>

            <arg name="api_endpoint">
                <title>API endpoint</title>
                <description>Your API AUTH Endpoint (for example lon.auth.rackspacecloud.com).</description>
            </arg>


        </args>
    </endpoint>
</scheme>
"""


def do_scheme():
    print SCHEME

def get_config():
    config = {}

    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))

        checkpnt_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpnt_node and checkpnt_node.firstChild and \
           checkpnt_node.firstChild.nodeType == checkpnt_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpnt_node.firstChild.data

        if not config:
            raise Exception, "Invalid configuration received from Splunk."

        # just some validation: make sure these keys are present (required)
        validate_conf(config, "name")
        validate_conf(config, "key_id")
        validate_conf(config, "secret_key")
        validate_conf(config, "checkpoint_dir")
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()


