"""Selects the a git branch
    Inputs:
        index: index of the selected branch inside the branches list (int)
    Output:
        branch: The selected branch
        branches: List of all branches inside the local git repository"""

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
            "Select Branch", "Select Branch", """Selects the a git branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("f53dcd2c-23be-4e85-8f7f-68b93957fdf7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "index", "index", "index of the selected branch inside the branches list (int)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branch", "branch", "The selected branch")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branches", "branches", "List of all branches inside the local git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH2SURBVEhLrdVNSBVRGMbxsTSij01Jq4KKICFsVVBrIxSKQGqR5cc2wp0IRdA2so3SByS6chHtolbixk1FkWjRTsGNn0SIpRZJ9X/Oue84jjN3jnAf+ME5M2fOO3PvnDNRRnbiBGpdr8K5jBn8K+nDDlQkp6FJX6MJXaV+DyqSAcz5Zpz7+Iu9rrcR/Yy38BKPcByFeYNPvhnnKvQUB13PZxdGoOOfsYxfOIuy6YAuuuh6UXQAXzCGKh0opRMad971/NPpxr4iOW5LdPIFdPEHzGIRp5DMMN75Zhx7Ut1U2dTgOzRY2pDOcyz4ZpyH+I3drlcmezAPK3AD6ZzEH+hta8Y9aOxdFGYfdHdWoBVZaYCNkacISmgBLT79PzbuEoISWuAQ1mDjtAMEJbTAbdgYqUNQigocQTe0sGzMBIL3q3SBFigP8BErsHPmCoKTLnATit7x5KTmDrYVLfusn2gJdmwd2osuIC8qfM43N0fbxTfYZNehvMcztEMLrVxs26h3vVSeQCcn8QNTOIpqhOQYdL2KbMk12F1rv9fE0xhFXrSiG33TXaPxj10vI68w7ptxVExF83ZJ/Uc6fxiD0CubmyHoDpKxz+Z+18tOL35Cm6RWeG70r2syfTrPQK+o+v0oylsErQd91VahiUUfoMI9nuR8yaLoPykulh6mcBQtAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, index):
        
        branch = None
        branches = None
        
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
        
        
        def branch_list():
            """
            Returns a list of existing branches
            """
            
            branch_list_msg = executor(["git", "branch"])
            
            return branch_list_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        branches = branch_list()
        
        raw = branches.strip("\n")
        raw = raw.split("\n")
        branch = None
        branches = []
        for i in range(len(raw)):
            raw[i] = raw[i].strip("*")
            raw[i] = raw[i].strip(" ")
        
            if i == index:
                branches.append( "> " + raw[i])
                branch = raw[i]
            else:
                branches.append( "  " + raw[i])
        
        return (branch, branches)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Select Branch"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("1ac81acd-96fd-407f-8110-01a755748efd")