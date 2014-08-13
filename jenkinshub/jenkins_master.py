import json
import utils
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import jsonpickle

import pdb

def orm2dict(orm_obj):
    orm_dict = orm_obj.__dict__
    for orm_key in orm_dict.keys():
        if orm_key.startswith("_") or orm_key == 'jenkinsapi.job.Job' or orm_key == 'slave':
            orm_dict.pop(orm_key)
    return orm_dict

class JenkinsJob(object):
    def __init__(self, job):
        self._initialize_fields(job)
        
    def _initialize_fields(self, job):
        self.name = job.name
        self.url = job.baseurl
        
    def to_JSON(self):
        return json.dumps(self.__dict__, skipkeys=True)
        
class JenkinsSlave(object):
    def __init__(self, slave):
        self._initialize_fields(slave)
        
    def _initialize_fields(self, slave):
        self.name = slave.name
        self.url = slave.baseurl
        
    def to_JSON(self):
        return json.dumps(orm2dict(self))

class JenkinsMaster(object):
    
    def __init__(self, jenkins):
        # self.jenkins = jenkins
        self._initialize_fields(jenkins)
        
    def _initialize_fields(self, jenkins):
        self.jobs = {}
        self.slaves = {}
        
        self.url = jenkins.baseurl
        self.version = jenkins.version
        
        self._initialize_jobs(jenkins)
        self._initialize_slaves(jenkins)
        
    def _initialize_jobs(self, jenkins):
        for key in jenkins.jobs.keys():
            self.jobs[key] = JenkinsJob(jenkins.jobs[key])
            
    def _initialize_slaves(self, jenkins):
        for key in jenkins.get_nodes().keys():
            self.slaves[key] = JenkinsSlave(jenkins.get_nodes()[key])
            
    def to_JSON(self):
        raw = json.loads(jsonpickle.encode(self))
    
    def __getstate__(self):
        state = self.__dict__.copy()
        # del state['__class__']
        return state
    
if __name__ == '__main__':
    config = utils.load_config(file_name='config/config.yml')
    jenkins = Jenkins(config[0]['jenkins']['url'])
    jm = JenkinsMaster(jenkins)
    # pdb.set_trace()
    print jm.to_JSON()  
