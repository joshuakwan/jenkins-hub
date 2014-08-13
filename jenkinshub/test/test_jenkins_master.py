from jenkinshub import jenkins_master
from jenkinshub import utils
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

import json

class TestJenkinsMaster():
    def setUp(self):
        config = utils.load_config(file_name='config.yml')
        self.jenkins = Jenkins(config[0]['jenkins']['url'])
        self.jm = jenkins_master.JenkinsMaster(self.jenkins)
        
    def testUrl(self):
        assert self.jm.url == self.jenkins.baseurl
        
    def testVersion(self):
        assert self.jm.version == self.jenkins.version
        
    def testJobs(self):
        jobs = self.jm.jobs
        
        for key in jobs.keys():
            assert key in self.jenkins.jobs.keys()
            
            job = jobs[key]
            job_o = self.jenkins.jobs[key]
            
            assert job.name == job_o.name
            assert job.url == job_o.baseurl
            
            json_o = json.loads(job.to_JSON())
            
            assert json_o.has_key('name')
            assert json_o.has_key('url')
            
    def testSlaves(self):
        slaves = self.jm.slaves
        
        for key in slaves.keys():
            assert key in self.jenkins.get_nodes().keys()
            
            slave = slaves[key]
            slave_o = self.jenkins.get_nodes()[key]
            
            assert slave.name == slave_o.name
            assert slave.url == slave_o.baseurl
            
            json_o = json.loads(slave.to_JSON())
            
            assert json_o.has_key('name')
            assert json_o.has_key('url')
            
