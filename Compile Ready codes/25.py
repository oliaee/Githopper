"""Executes the given custom git command
    Inputs:
        command: The custom git command to run
        execute: Triggers the git command (Button)
    Output:
        help: Output of the git operation / Helpful tips"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from subprocess import check_output, Popen
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
            "Execute Git Command", "Execute", """Executes the given custom git command""", "Githopper", "Utility")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("fcac3693-d9ca-4079-ba22-9e0af7fb162a")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "command", "command", "The custom git command to run")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "execute", "execute", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFLSURBVEhL7dW9L0NRHMbx6y06WoxsIhGTrYnRZjH7E4xiI14Soki8bGxC4m1CCEHSKrGI0WixYjAb+D4596Zu3F97brWLeJJPek7b3Kc99+UEfyr9mMFyDUwji1j0wScKOMQVjnAZzou48aTj5BDLGk7RgnF0YQzdmECa6McsuWEpKjhGM1bQg3n0YhVpco0fBbN4wQ7WsY0NbIXz/RReMYlYooI97OIA+rJeNdf7GldiFmiJLtzw10k8B1rnE+jk3qIPUe4x6oZeucOiG5aignO04QkfWEA7NjEM35gFeTcMRqBrWYaQgS5f35gFWqJO6MAPGEAD3qCLwDdmwRk6oPVuQhTNBzEH3SNT0P1ixSzQDWKlFc94x2M4t2IW6DlULo3QP9NruVRd4Jv/gopJLNCzSJtMLZL4LIp2tO87U7USd7S678l1SBB8AUE7jhoNEhJvAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, command, execute):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/K"] + cmd)
            except:
                pass
        
        def parser(cmd):
            def index_finder(text,char):
                out_put = []
                b = 0
                
                for i in range(50):
                    try:
                        b = text.index(char, b+1)
                        out_put.append(b)
                    except:
                        break
                
                return out_put
            
            a = sorted(index_finder(cmd, "'") + index_finder(cmd, "\""))
            slices = [cmd[a[i]+1:a[i+1]] for i in range(0,len(a),2)]
            for i in slices: cmd = cmd.replace(i, "<>")
            cmd = cmd.split(" ")
            
            out_put = []
            for i in cmd:
                if  "<>" in i:
                    out_put.append(slices.pop(0))
                else:
                    out_put.append(i)
            
            return out_put
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area & help ------------------------------------------------
        
        try:
            command_lst = command.split(" ")
            
            if command_lst[0] == "git" and execute:
                executor(parser(command))
            elif command_lst[0] != "git":
                help = "Invalid command (Please only use git commands)"
            else:
                help = ("Press execute button to run the command"
                          "\n\n* make sure to put file names in quotation or double quotation"
                          "\nExample:\ngit checkout HEAD~1 'some file.txt'")
        
        except:
            help = "You haven't entered a git command"
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Execute Git Command"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("9184ee38-d815-4351-a353-c42ac7fca4b6")