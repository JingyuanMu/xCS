import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

import click

@click.command('init-db')
def init_db_command():
    """清空现有数据并创建新表格"""
    init_db()
    click.echo('已初始化数据库。')

def get_table_names():
    """返回数据库中的所有表名"""
    db = get_db()
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    return [row['name'] for row in db.execute(query).fetchall()]


@click.command('list-tables')
def list_tables_command():
    """列出数据库中的所有表名"""
    tables = get_table_names()
    click.echo("现有表格:")
    for table in tables:
        click.echo(f"- {table}")