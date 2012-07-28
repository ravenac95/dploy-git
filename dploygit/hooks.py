class GitReceiveUpdate(object):
    pass


class GitRepository(object):
    pass


class GitoliteEnv(object):
    pass


class PreReceiveHook(object):
    def __init__(self,  git_repository, env):
        self._git_repository = git_repository
        self._env = env

    def run(self):
        """Run the hook"""
        # Connect to the dploy center
        for line in self._stdin:
            update = GitReceiveUpdate.from_line(line, self._git_repository)
            current_branch = update.branch
            if current_branch == 'master':
                filename = update.export_to_temp_file()
                self._dploy_center_client.make_deploy_order(
                    self._env.user,
                    self._env.repository,
                    filename,
                    update.new_commit
                )
