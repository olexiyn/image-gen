#!/usr/bin/env python
import click
from app import app, init_app

init_app(app)

@click.command(help="Run image-gen server")
@click.option('--host', help='Server host, default 0.0.0.0', default='0.0.0.0')
@click.option('--port', help='Server port, default 8872', type=int, default='8872')
@click.option('--workers', help='Server workers, default 1', type=int, default=1)
@click.option('--debug', help='Debug mode', is_flag=True)
@click.option('--accesslog', help='Access log', is_flag=True)
def srv(host, port, workers, debug, accesslog):
    app.run(
        host=host,
        port=port,
        workers=workers,
        debug=debug,
        auto_reload=debug,
        access_log=accesslog
    )

@click.group()
def cli():
    pass

cli.add_command(srv)
if __name__ == '__main__':
    cli()
