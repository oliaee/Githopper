"""Deletes the selected branch
    Inputs:
        branch: The name of the branch to be deleted
        force: Determines whether the delete operation should be forced (Toggle)
        delete: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"


from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Delete Branch", "Branch -", """Deletes the selected branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("7969bfdf-6b54-42ea-ae60-3b84b9bed134")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The name of the branch to be deleted")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "delete", "delete", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHXSURBVEhLrdU9SBxBGMbxjUYRjY2KnRBFMKCkMmBqgyBGBImFH1FbEbsQUIS0osFCSAKKnYXYBVNJmlQJEcUP7BRsYqKIiKImRNT/s3uz7p17t6PuAz+Y2Zubmb3bfccJSTYqUeL2Yk4zfuEyYQJZiCVPoUnn0Yg3if4YYsk0fntNP+9wgQK3dx39jH2Yw3tUIDJfsOQ1/byC7qLY7XnJxVfo+hqO8BfPkDG90Jca3J7jFGEdy3igC4kMQOOeuz3v7rSxDQTH3Yg+nIW+/BM72EM1glnAd6/px9ypNpUxOTiABks3UjOJXa/pZxT/kOf2MiQff2AW6ERqqvAfetpaMQyNHUJkHkG7Mwu8RljqYcbIR1jFdgG9fPp/zLiXsIrtAqU4gxmnCmAV2wX6YcbIE1glaoEyvIVeLDNmFdb1KnWBDigjWMQJzGdGC6yTukAXFD3jwUmNQdwqeu3DfqJDmGvnUC16gVtH5WIfZrJ2KD/wCT3Qi3bnfIAm3sQxtvAYDxEWVVbddRiVnaS0wexa9V4Tb+Mb0mUcKtdhdF4k5TNWvKYfLaZF01XJGjSlUY6kzEA7DsYcm4Vu756pgybT0VkLPaLqTyG26FQ7hSYWHUCRNT59HOcKPV2S9nGltHoAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, delete):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def delete_branch(branch_name):
            """
            deletes the selected branch
            """
            
            db_msg = executor(["git", "branch", "-D", str(branch_name)])
            
            return db_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if branch != "master":
            if delete and branch != None:
                r = delete_branch(branch)
        else:
            r = "master branch can't be deleted"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the delete button to delete the selected branch\n"
        if not branch: help +="\n* You need to enter a branch name first\n"
        help += "\n* You can use the 'select Branch' component to choose a branch\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_10"]
        except:
            rsc.sticky["Githopper_10"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_10"] == None:
            rsc.sticky["Githopper_10"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_10"]
            rsc.sticky["Githopper_10"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Delete Branch"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("286111c4-f3ac-4be9-bca7-42f463db8a83")