#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann <stefan.st.lehmann@gmail.com>

"""
from fabric.api import local, settings, run, cd, env, get
from time import localtime, strftime

lt = localtime()

env.app_dir = '/var/www/flaskhab'
env.backup_dir = '/home/apps/backup'
env.backup_dir_local = '/Users/stefan/Documents/python/projects/flaskhab/backup'
env.data_dir = '/var/www/flaskhab/app/static/images'
env.date = strftime('%Y-%m-%d', lt)
env.hosts = ['root@31.170.105.247']


def backup():
    backup_filename = '{backup_dir}/{date}-backup.tar'.format(**env)

    # backup database
    run(
        'tar -cvpf {backup_filename} {app_dir}/*.sqlite --exclude=cache'
        .format(backup_filename=backup_filename, app_dir=env.app_dir)
    )

    # backup user file
    run(
        'tar -rvpf {backup_filename} {data_dir} --exclude=cache'
        .format(backup_filename=backup_filename, data_dir=env.data_dir)
    )

    # compress
    run('gzip -f {}'.format(backup_filename))

    # get files
    get(remote_path=env.backup_dir + '/' + env.date + '-backup.tar.gz',
        local_path=env.backup_dir_local)


def commit():
    with settings(warn_only=True):
        local('git add -i && git commit')


def push():
    local('git push')


def prepare_deploy():
    commit()
    push()


def deploy():
    commit()
    push()

    with cd(env.app_dir):
        # Pull repository
        run('git pull')

        # install packages
        run('./venv/bin/pip install -r requirements/base.txt')

        # Change the access rights to apps user
        run('chown -R apps:www-data .')

        # Upgrade database
        run('./venv/bin/python manage.py db upgrade')

        # Restart app
        run('supervisorctl restart flaskhab')
