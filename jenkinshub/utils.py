import yaml
import logging
import os

logging.info('creating logger')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_config(file_name=None):
    if not file_name:
        cfg_file = 'config/config.yml'
    else:
        cfg_file = file_name
    
    logger.info('Load config from %s' % cfg_file)
    
    if not os.path.exists(cfg_file):
        logger.error('The config file %s does not exist' % cfg_file)
        return None
    
    f_cfg = open(cfg_file)
    config = yaml.load(f_cfg)
    f_cfg.close()
    
    for jenkins in config:
        logger.info('%s: %s' % (jenkins['jenkins']['name'], jenkins['jenkins']['url']))
    
    return config

