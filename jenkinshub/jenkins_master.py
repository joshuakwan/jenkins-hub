import json
import utils
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import jsonpickle

import pdb

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
        self._tailor_json(raw)
        return str(raw)
    
    def _tailor_json(self, j):
        if 'keys' in dir(j):
            if j.has_key('py/object'):
                j.pop('py/object')
            for key in j.keys():
                self._tailor_json(j[key])
        else:
            return         
    
    
if __name__ == '__main__':
    config = utils.load_config(file_name='config/config.yml')
    jenkins = Jenkins(config[0]['jenkins']['url'])
    jm = JenkinsMaster(jenkins)
    # pdb.set_trace()
    print jm.to_JSON()
    
   
