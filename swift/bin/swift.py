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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()


