# -*- encoding: utf-8 -*-
# ! python3

import logging

import click

logger = logging.getLogger(__name__)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def cli():
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('deployment', type=click.STRING)
@click.argument('container', type=click.STRING)
@click.argument('image', type=click.STRING)
@click.option('--namespace', type=click.STRING, default='default')
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', count=True)
def set_image(deployment: str, container: str, image: str, namespace: str, verbose: int, quiet: int):
    """
    Set image
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose,
                        format='[%(asctime)s] %(levelname)-7s [%(name)s:%(module)s - %(funcName)s:%(lineno)s] %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    logger.info("Running `set_image`.")

    # TODO

    logger.info("Done.")


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('manifest_file', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True))
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', count=True)
def apply(manifest_file: str, verbose: int, quiet: int):
    """
    Apply manifest file
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose,
                        format='[%(asctime)s] %(levelname)-7s [%(name)s:%(module)s - %(funcName)s:%(lineno)s] %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    logger.info("Running `apply`.")

    # TODO

    logger.info("Done.")


if __name__ == '__main__':
    logger.debug('Entering main section.')
    cli()
    logger.debug('Done.')
