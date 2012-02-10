# This has been tested against Mercurial version 2.0.1
from mercurial import hg, ui, commands

class Hg(object):
    def __init__(self, root_path):
        self.hgui=ui.ui()
        self.repo=hg.repository(self.hgui, root_path)

    def log(self, filename):
        self.hgui.pushbuffer()
        commands.log(self.hgui, self.repo, filename, follow=True, date="", rev="", user="")
        _log=self.hgui.popbuffer()

        changesets=[_c for _c in _log.split('\n\n') if _c not in ('')]
        history=[]
        for changeset in changesets:
            _dict={}
            for _f in changeset.split("\n"):
                kkk, vvv=_f.split(": ")
                _dict[kkk.strip()]=vvv.strip()
            history.append(_dict)
        return history
