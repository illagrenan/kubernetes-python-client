# -*- encoding: utf-8 -*-
# ! python3

import io
import logging
import os
import pprint

import click
import yaml
from kubernetes.client import AppsV1beta2Api, BatchV1Api

from cluster_credentials import ClusterCredentialsContextManager

logger = logging.getLogger(__name__)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def cli():
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('deployment', type=click.STRING)
@click.argument('container', type=click.STRING)
@click.argument('container2', type=click.STRING, default='')
@click.argument('image', type=click.STRING)
@click.option('--server', prompt=False, default=lambda: os.environ.get('KUBERNETES_SERVER'), type=click.STRING)
@click.option('--namespace', prompt=False, default=lambda: os.environ.get('KUBERNETES_NAMESPACE', 'default'), type=click.STRING)
@click.option('--user', prompt=False, default=lambda: os.environ.get('KUBERNETES_USER'), type=click.STRING)
@click.option('--password', prompt=False, default=lambda: os.environ.get('KUBERNETES_PASSWORD'), type=click.STRING)
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', count=True)
def set_image(deployment: str, container: str, container2: str, image: str, server: str, namespace: str, user: str, password: str, verbose: int, quiet: int):
    """
    Set image
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose,
                        format='[%(asctime)s] %(levelname)-7s [%(name)s:%(module)s - %(funcName)s:%(lineno)s] %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    logger.info("Running `set_image`.")

    with ClusterCredentialsContextManager(server=server, user=user, password=password):
        v2_beta = AppsV1beta2Api()

        if container2:
            image_ = [
                {"name": container, "image": image},
                {"name": container2, "image": image}
            ]
        else:
            image_ = [
                {"name": container, "image": image}
            ]

        body = {
            "spec":
                {
                    "template": {
                        "spec": {
                            "containers": image_
                        }
                    }
                }
        }
        api_response = v2_beta.patch_namespaced_deployment(deployment, namespace, body, pretty=True)
        pprint.pprint(api_response)

    logger.info("Done.")


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('manifest_file', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True))
@click.option('--server', prompt=False, default=lambda: os.environ.get('KUBERNETES_SERVER'), type=click.STRING)
@click.option('--namespace', prompt=False, default=lambda: os.environ.get('KUBERNETES_NAMESPACE', 'default'), type=click.STRING)
@click.option('--user', prompt=False, default=lambda: os.environ.get('KUBERNETES_USER'), type=click.STRING)
@click.option('--password', prompt=False, default=lambda: os.environ.get('KUBERNETES_PASSWORD'), type=click.STRING)
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', count=True)
def apply(manifest_file: str, server: str, namespace: str, user: str, password: str, verbose: int, quiet: int):
    """
    Apply manifest file
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose,
                        format='[%(asctime)s] %(levelname)-7s [%(name)s:%(module)s - %(funcName)s:%(lineno)s] %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    logger.info("Running `apply`.")

    with ClusterCredentialsContextManager(server=server, user=user, password=password):
        v1_batch = BatchV1Api()

        with io.open(manifest_file, 'r', encoding='utf-8') as the_file:
            yaml_gen = yaml.load_all(the_file.read())
            documents = list(yaml_gen)

        api_response = v1_batch.create_namespaced_job(namespace, documents[0], pretty=True)
        pprint.pprint(api_response)

    logger.info("Done.")


if __name__ == '__main__':
    logger.debug('Entering main section.')
    cli()
    logger.debug('Done.')
