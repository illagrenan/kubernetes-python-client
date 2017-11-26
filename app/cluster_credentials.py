# -*- encoding: utf-8 -*-
# ! python3

import logging
from contextlib import ContextDecorator

from kubernetes.client import Configuration
from kubernetes.config.kube_config import KubeConfigLoader

logger = logging.getLogger(__name__)


def cluster_login_config_template(server, user, password):
    cluster_local_name = "k8s"

    return {
        "clusters": [
            {
                "cluster": {
                    "insecure-skip-tls-verify": True,
                    "server": server
                },
                "name": cluster_local_name
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": cluster_local_name,
                    "user": cluster_local_name,
                    "namespace": "default"
                },
                "name": cluster_local_name
            }
        ],
        "current-context": cluster_local_name,
        "kind": "Config",
        "apiVersion": "v1",
        "preferences": {},
        "users": [
            {
                "name": cluster_local_name,
                "user": {
                    "password": password,
                    "username": user
                }
            }
        ]
    }


def load_kube_config_from_dict(config_dict):
    """
    Loads authentication and cluster information from dict.
    """

    config_loader = KubeConfigLoader(config_dict=config_dict)

    client_configuration = Configuration()
    config_loader.load_and_set(client_configuration=client_configuration)
    Configuration.set_default(client_configuration)

    return config_loader


class ClientConfiguration:
    api_key = {
        'authorization': None
    }
    verify_ssl = False


class ClusterCredentialsContextManager(ContextDecorator):
    def __init__(self, server, user, password):
        self._server = server
        self._config_dict = cluster_login_config_template(server=server, user=user, password=password)

    def __str__(self) -> str:
        """
        “informal” or nicely printable string representation of an object
        """
        return "Cluster {}".format(self.__repr__())

    def __repr__(self) -> str:
        """
        “official” string representation of an object.
        """
        return str(self._server)

    def __enter__(self) -> 'ClusterCredentialsContextManager':
        self._loaded_config = load_kube_config_from_dict(config_dict=self._config_dict)
        return self

    def __exit__(self, *arg):
        del self._loaded_config
