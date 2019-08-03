"""Selects a git commit
    Inputs:
        index: index of the selected commit inside the commits list (int)
    Output:
        commit: The selected commit
        commits: List of all commits inside the local git repository"""

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
            "Select Commit", "Select Commit", """Selects a git commit""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("e875c5e4-7cf5-4157-b2cc-c9e1fd85921e")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "index", "index", "index of the selected commit inside the commits list (int)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commit", "commit", "The selected commit")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commits", "commits", "List of all commits inside the local git repository")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAE7SURBVEhL7dS/K0ZRHMfxKyGlLGKRH4tFdqNSssmvklI2kz/AxIBBSsTKYvEXyCIDVokYGCzKoPwIk/D+nOd+67gdj9znGJR3vbq/zj33eU63m/z3Z2rFPA5whn3MohklN4oHvAfcYRi560Fo4qwu5OoSNskJ+tGOQWip7No5ilYFLcW4R2tsE1yjDn4NuIGNmYF//wgq4NLNNjBkEaFWEBovr6iF67sHTCPUHELj5dMDarCGDc8ObPARQp3CxmzDv1//rhpfVol72ASbaEI5WrAFu3YLnf9xk7BJ5BkXePHOyQRytwR/sqwFlNwA9vCIt3S7iz5ETe9+W7ot1hQ6C7vxG4KWrsMdRU5fXU2uh0SpG72FXfeaXmHVHUVqDPrFjVjHMaK3jCfow1evE7/RIaK/sn5l6TZTknwApul7qilH2ZIAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, index):
        
        commit = None
        commits = None
        
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
        
        def log():
            """
            This function provides a log of commits
            """
        
            log_msg = executor(["git", "log", "--oneline"])
        
            return log_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        try:
            commits = log()
            
            if not len(commits):
                commits = "nothing has been commited yet"
            
            raw = commits.strip("\n")
            raw = raw.split("\n")
            
            commits = []
            for i in range(len(raw)):
                raw[i] = raw[i].split(" ")
                if i == index:
                    commits.append("> " + " ".join(raw[i][1:]))
                    commit = raw[i][0]
                else:
                    commits.append("  " + " ".join(raw[i][1:]))
        except:
            commit = "No commit has been selected"
        
        return (commit, commits)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Select Commit"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("64e6e185-6903-4364-ab2b-b5efd91f0192")