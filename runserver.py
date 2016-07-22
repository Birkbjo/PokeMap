#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import time

from threading import Thread

from pogom import config
from pogom.app import Pogom
from pogom.utils import get_args, insert_mock_data, load_credentials,load_locs
from pogom.search import search_loop
from pogom.models import create_tables, Pokemon, Pokestop, Gym

from pogom.pgoapi.utilities import get_pos_by_name

log = logging.getLogger(__name__)

def start_locator_thread(argz):
    num_t = 1
    for i in range(0,num_t):

        search_thread = Thread(target=search_loop, args=(argz,num_t,i))
        search_thread.daemon = True
        search_thread.name = 'search_thread {}'.format(i)
        search_thread.start()
        time.sleep(1)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(module)11s] %(threadName)s [%(levelname)7s] %(message)s')

    logging.getLogger("peewee").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pogom.pgoapi.pgoapi").setLevel(logging.WARNING)
    logging.getLogger("pogom.pgoapi.rpc_api").setLevel(logging.INFO)

    args = get_args()
    config['ARGS'] = args
    if args.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    create_tables()

    locs = load_locs(os.path.dirname(os.path.realpath(__file__)))['locs']
    creds = load_credentials(os.path.dirname(os.path.realpath(__file__)))

    if args.location:
        pos = get_pos_by_name(args.location)
        config['locs'].append(pos)

    for l in locs:
        pos = get_pos_by_name(l)
        config['locs'].append(pos)

    config['steps'] = args.step_limit
    config['LOCALE'] = args.locale

    if not args.username or not args.password:
        user1 = creds['users'][0]
        args.username = user1['name']
        args.auth_service = user1['type']
        args.password = user1['pass']
        log.debug("Loaded user {} from file".format(user1['name']))

    if args.mock:
        insert_mock_data()
    if not args.no_search:
        start_locator_thread(args)

    app = Pogom(__name__)
    config['ROOT_PATH'] = app.root_path
    if args.gmaps_key is not None:
        config['GMAPS_KEY'] = args.gmaps_key
    else:
        config['GMAPS_KEY'] = creds['gmaps_key']
    log.info("Server started")
    app.run(threaded=True, debug=args.debug, host=args.host, port=args.port)
