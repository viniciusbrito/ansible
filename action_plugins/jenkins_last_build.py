from ansible.plugins.action import ActionBase
from jenkinsapi import jenkins

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}
        
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        # Extract necessary parameters from task variables
        jenkins_url = module_args.get('url')
        username = module_args.get('username')
        password = module_args.get('password')
        job_name = module_args.get('job_name')

        # Debug messages
        self._display.v("Jenkins URL: %s" % jenkins_url)
        self._display.v("Username: %s" % username)
        self._display.v("Password: %s" % password)
        self._display.v("Job Name: %s" % job_name)

        try:
            jenkins_server = jenkins.Jenkins(jenkins_url, username=username, password=password)
            job = jenkins_server[job_name]
            build = job.get_last_build()
            last_build = {
                "number": build.get_number(),
                "revision": build.get_revision(),
                "status": build.get_status(),
                "date": build.get_timestamp().isoformat(),
                "build_url": build.get_build_url()
            }
            result['last_build'] = last_build
        except Exception as e:
            result['failed'] = True
            result['msg'] = str(e)

        return result
